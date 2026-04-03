-- ============================================================
-- Query: Livepeer Fee Concentration by Broadcaster (Arbitrum)
-- Paper: Paper 2 ("GeoDePIN: Design Patterns")
-- Section: Exhibit 4 — Demand HHI (if applicable)
-- Chain: Arbitrum
-- Time Range: Jan 2024 to Apr 2026
-- Dune Query ID: 6942646
-- Author: Zach Zukowski
-- Notes:
--   - Livepeer has NO burn mechanism; fees route to orchestrators/delegators
--   - Demand HHI measured by who PAYS for transcoding (broadcasters)
--   - RESULT: HHI = 0.3059, N=28, top-2=75.5%, top-5=96.5%
--   - Only 28 unique broadcasters in 2 years — highly concentrated demand
--   - Top broadcaster 0xc3c7... = 41.2% ($168 ETH), 0xca33... = 34.3% ($140 ETH)
--   - These are likely AI/ML inference gateways using Livepeer for video processing
-- ============================================================

-- Option A: Use decoded Livepeer tables (if available)
SELECT
    sender AS broadcaster,
    SUM(CAST(faceValue AS DOUBLE) / 1e18) AS total_eth_paid,
    COUNT(*) AS ticket_count,
    MIN(evt_block_time) AS first_txn,
    MAX(evt_block_time) AS last_txn
FROM livepeer_arbitrum.TicketBroker_evt_WinningTicketRedeemed
WHERE evt_block_time >= TIMESTAMP '2024-01-01'
  AND evt_block_time < TIMESTAMP '2026-04-01'
GROUP BY sender
ORDER BY total_eth_paid DESC
LIMIT 100

-- Option B: If decoded tables unavailable, use raw approach:
-- SELECT * FROM arbitrum.logs
-- WHERE contract_address = 0x... -- Livepeer TicketBroker on Arbitrum
--   AND topic0 = 0x... -- WinningTicketRedeemed event signature
-- LIMIT 10
