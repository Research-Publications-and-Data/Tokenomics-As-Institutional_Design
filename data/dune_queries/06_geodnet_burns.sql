-- Dune Query 7541498 v2: GEODNET Foundation buy-and-burn (Polygon)
-- https://dune.com/queries/7541498
-- GEOD Polygon ERC-20: 0xac0f66379a6d7801d7726d5a943356a172549adb
-- Burn sink (dead address): 0x000000000000000000000000000000000000dEaD
--
-- This is the construct-correct burn flow for the GEODNET S2R numerator.
-- The GEODNET Foundation collects fiat subscription revenue off-chain, buys GEOD
-- on the open market, and burns it by sending to the Polygon dead address. This
-- series (not the Solana SPL burn series) is the Foundation buy-and-burn; it
-- reproduces the issuer-reported (Messari) burn totals and the companion B2
-- paper's on-chain GEOD revenue measurement to within 0.2%.
--
-- NOTE (correction history): the prior version of this query measured Solana SPL
-- burn instructions on mint 7JA5eZdCzztSfQbJvS8aVVxMFfd81Rs9VvwnocV1mKHu. A
-- 2026-06 reconciliation against the Blockworks dashboard established that those
-- SPL burns predominantly reflect Wormhole NTT bridge outflow (cross-chain
-- transfers), not the Foundation buy-and-burn, and so are not a valid S2R
-- numerator. See CHANGELOG 1.6.0.

SELECT
    date_trunc('month', evt_block_time) AS month,
    COUNT(*)                            AS burn_tx_count,
    SUM(CAST(value AS DOUBLE) / 1e18)   AS geod_burned
FROM erc20_polygon.evt_Transfer
WHERE contract_address = 0xac0f66379a6d7801d7726d5a943356a172549adb
  AND "to" = 0x000000000000000000000000000000000000dEaD
  AND evt_block_time >= TIMESTAMP '2024-09-01'
GROUP BY 1
ORDER BY 1
