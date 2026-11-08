-- ============================================================
-- Query: DIMO null-address flow, per-transfer detail with call context
-- Paper: B3 "Who Burns the Tokens" (DIMO leg)
-- Purpose: establish WHAT the S2R numerator in data/dune_queries/03_dimo_s2r.sql
--          actually measures. That query counts every ERC-20 transfer of DIMO to
--          the null address or 0x...dEaD on Polygon and calls the total
--          "Developer License burns". This query returns the same transfers one
--          row at a time, carrying the transaction's entry-point contract and
--          method selector, so each transfer can be attributed to the contract
--          path that produced it rather than assumed.
-- Chain: Polygon
-- Time range: 2024-01-01 to 2026-03-01 (identical bounds to 03_dimo_s2r.sql)
-- Companion rows: mint (issuance) side aggregated per month per recipient, so the
--          denominator's composition is visible without a second execution.
-- Dependencies: Dune Analytics account
-- ============================================================

WITH burn_tf AS (
    SELECT
        t.evt_block_time                    AS block_time,
        t.evt_tx_hash                       AS tx_hash,
        CAST(t.evt_index AS BIGINT)         AS idx_or_count,
        t."from"                            AS counterparty,
        t."to"                              AS sink,
        CAST(t.value AS DOUBLE) / 1e18      AS amount
    FROM erc20_polygon.evt_Transfer t
    WHERE t.contract_address = 0xE261D618a959aFfFd53168Cd07D12E37B26761db
      AND t."to" IN (
          0x0000000000000000000000000000000000000000,
          0x000000000000000000000000000000000000dEaD
      )
      AND t.evt_block_time >= TIMESTAMP '2024-01-01'
      AND t.evt_block_time <  TIMESTAMP '2026-03-01'
),

burn_tx AS (
    SELECT
        x.hash                              AS tx_hash,
        x."from"                            AS tx_from,
        x."to"                              AS tx_to,
        bytearray_substring(x.data, 1, 4)   AS method_id
    FROM polygon.transactions x
    WHERE x.block_time >= TIMESTAMP '2024-01-01'
      AND x.block_time <  TIMESTAMP '2026-03-01'
      AND x.hash IN (SELECT tx_hash FROM burn_tf)
),

mint_agg AS (
    SELECT
        DATE_TRUNC('month', t.evt_block_time) AS block_time,
        t."to"                                AS counterparty,
        CAST(COUNT(*) AS BIGINT)              AS idx_or_count,
        SUM(CAST(t.value AS DOUBLE) / 1e18)   AS amount
    FROM erc20_polygon.evt_Transfer t
    WHERE t.contract_address = 0xE261D618a959aFfFd53168Cd07D12E37B26761db
      AND t."from" = 0x0000000000000000000000000000000000000000
      AND t.evt_block_time >= TIMESTAMP '2024-01-01'
      AND t.evt_block_time <  TIMESTAMP '2026-03-01'
    GROUP BY 1, 2
)

SELECT
    'burn'              AS row_kind,
    b.block_time        AS block_time,
    b.tx_hash           AS tx_hash,
    b.idx_or_count      AS idx_or_count,
    b.counterparty      AS counterparty,
    b.sink              AS sink,
    b.amount            AS amount,
    x.tx_from           AS tx_from,
    x.tx_to             AS tx_to,
    x.method_id         AS method_id
FROM burn_tf b
LEFT JOIN burn_tx x ON x.tx_hash = b.tx_hash

UNION ALL

SELECT
    'mint_month_agg'            AS row_kind,
    m.block_time                AS block_time,
    CAST(NULL AS VARBINARY)     AS tx_hash,
    m.idx_or_count              AS idx_or_count,
    m.counterparty              AS counterparty,
    CAST(NULL AS VARBINARY)     AS sink,
    m.amount                    AS amount,
    CAST(NULL AS VARBINARY)     AS tx_from,
    CAST(NULL AS VARBINARY)     AS tx_to,
    CAST(NULL AS VARBINARY)     AS method_id
FROM mint_agg m

ORDER BY 1, 2, 4;
