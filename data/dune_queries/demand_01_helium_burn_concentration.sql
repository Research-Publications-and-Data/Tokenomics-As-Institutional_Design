-- ============================================================
-- Query: Helium DC Burn Concentration — Full HHI
-- Paper: Paper 2 ("GeoDePIN: Design Patterns")
-- Section: Exhibit 4 — Demand HHI
-- Chain: Solana
-- Time Range: May 2023 to March 2026
-- Dune Query ID: 6942532
-- Author: Zach Zukowski
-- Notes:
--   - Uses tx_signer (transaction initiator) as demand actor
--   - amount_display is pre-scaled (HNT with 8 decimals)
--   - block_date filter enables partition pruning (cheaper)
--   - Returns ALL signers (no LIMIT) for accurate HHI
-- Post-processing (Python):
--   hhi = sum(hhi_contribution)   # sum of share^2
--   top5 = pct_of_total for top 5 rows / 100
-- ============================================================

WITH burn_by_address AS (
    SELECT
        tx_signer AS burn_address,
        SUM(amount_display) AS total_burned,
        COUNT(*) AS burn_count,
        MIN(block_time) AS first_burn,
        MAX(block_time) AS last_burn
    FROM tokens_solana.transfers
    WHERE token_mint_address = 'hntyVP6YFm1Hg25TN9WGLqM12b8TQmcknKrdu1oxWux'
      AND action = 'burn'
      AND block_time >= TIMESTAMP '2023-05-01'
      AND block_time < TIMESTAMP '2026-03-01'
      AND block_date >= DATE '2023-05-01'
      AND block_date < DATE '2026-03-01'
    GROUP BY tx_signer
),
totals AS (
    SELECT SUM(total_burned) AS grand_total FROM burn_by_address
),
shares AS (
    SELECT
        b.burn_address,
        b.total_burned,
        b.burn_count,
        b.first_burn,
        b.last_burn,
        b.total_burned / t.grand_total AS share
    FROM burn_by_address b
    CROSS JOIN totals t
)
SELECT
    burn_address,
    total_burned,
    burn_count,
    first_burn,
    last_burn,
    ROUND(share * 100, 4) AS pct_of_total,
    ROUND(POWER(share, 2), 8) AS hhi_contribution
FROM shares
ORDER BY total_burned DESC
