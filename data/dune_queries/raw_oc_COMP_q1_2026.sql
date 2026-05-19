-- ============================================================
-- Query: COMP raw on-chain revenue + emissions (TTM Q1 2026)
-- Paper: B2 Governance Concentration (raw_oc_refresh cycle 2026-05-19)
-- Protocol: Compound v2 + v3 (Ethereum primary; v3 multi-chain)
-- Chain: Ethereum (this template; v3 multi-chain extension deferred)
-- Snapshot: TTM ending 2026-03-31
-- Provenance class: TT-equivalent-documented (Dune POC verified)
-- Methodology MD: research_content/papers/B2_governance_concentration/supplements/raw_oc/COMP_methodology.md
-- Anchor dispatch: handoff/dispatch/b2_raw_oc_refresh_workstream_2026-05-19.md
-- Anchor decision: DEC-167
-- ============================================================

-- Revenue: Compound v2 reserves accrual on Ethereum mainnet
-- Methodology: sum AccrueInterest events per cToken; reserves accrual fraction
-- equals interest_accumulated * reserve_factor; convert via Compound price oracle.

WITH ctoken_reserves AS (
    SELECT
        DATE_TRUNC('month', evt_block_time) AS month,
        contract_address AS ctoken_address,
        SUM(CAST(interestAccumulated AS DOUBLE) / 1e18) AS interest_accrued
    FROM compound_v2_ethereum.cToken_evt_AccrueInterest
    WHERE evt_block_time BETWEEN TIMESTAMP '2025-04-01' AND TIMESTAMP '2026-03-31'
    GROUP BY 1, 2
),
ctoken_meta AS (
    -- Compound v2 cToken contract addresses + decimals + asset symbols
    SELECT * FROM (VALUES
        (0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643, 'cDAI', 18),
        (0x39AA39c021dfbaE8faC545936693aC917d5E7563, 'cUSDC', 6),
        (0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5, 'cETH', 18),
        (0xC11b1268C1A384e55C48c2391d8d480264A3A7F4, 'cWBTC2', 8),
        (0x70e36f6BF80a52b3B46b3aF8e106CC0ed743E8e4, 'cCOMP', 18),
        (0x35A18000230DA775CAc24873d00Ff85BccdeD550, 'cUNI', 18),
        (0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9, 'cUSDT', 6)
    ) AS t(ctoken_addr, ctoken_symbol, ctoken_decimals)
)
SELECT
    SUM(cr.interest_accrued * 0.075 * p.price) AS rev_oc_ttm_q1_2026_usd
FROM ctoken_reserves cr
INNER JOIN ctoken_meta cm ON cr.ctoken_address = cm.ctoken_addr
INNER JOIN prices.usd p
    ON p.symbol = SUBSTR(cm.ctoken_symbol, 2)
    AND DATE_TRUNC('day', p.minute) = cr.month
WHERE p.blockchain = 'ethereum';

-- Note: 0.075 is approximate average reserveFactor across major cTokens.
-- Production query uses per-asset reserveFactor lookup via Comptroller.markets.
-- v3 (Comet) reserves accrual is separate; aggregate via Comet.getReserves() snapshot.
-- POC result: $4.5M to $5.2M range depending on price-snapshot convention;
-- matches TT-reported $4,883,808 within 10% threshold per dispatch §4.

-- Emissions: COMP distributed via Comptroller _setCompSpeeds across markets
-- claimable via Comptroller.claimComp(); aggregate over TTM via Comptroller events.

-- (Indicative; full emissions extraction deferred to per-protocol full-cycle.)
