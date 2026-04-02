-- Dune Query 6917162: GEODNET Burn Signer Concentration (Solana)
-- https://dune.com/queries/6917162
-- GEOD Token Mint: 7JA5eZdCzztSfQbJvS8aVVxMFfd81Rs9VvwnocV1mKHu

WITH burns AS (
    SELECT
        call_tx_signer,
        CAST(amount AS DOUBLE) as raw_amount
    FROM spl_token_solana.spl_token_call_burn
    WHERE account_mint = '7JA5eZdCzztSfQbJvS8aVVxMFfd81Rs9VvwnocV1mKHu'
        AND call_block_date >= DATE '2024-01-01'

    UNION ALL

    SELECT
        call_tx_signer,
        CAST(amount AS DOUBLE) as raw_amount
    FROM spl_token_solana.spl_token_call_burnchecked
    WHERE account_mint = '7JA5eZdCzztSfQbJvS8aVVxMFfd81Rs9VvwnocV1mKHu'
        AND call_block_date >= DATE '2024-01-01'
),

total AS (
    SELECT SUM(raw_amount) as total_burned
    FROM burns
),

by_signer AS (
    SELECT
        call_tx_signer,
        COUNT(*) as burn_tx_count,
        SUM(raw_amount) as signer_burned
    FROM burns
    GROUP BY 1
)

SELECT
    s.call_tx_signer,
    s.burn_tx_count,
    s.signer_burned / 1e9 as geod_burned,
    s.signer_burned / t.total_burned * 100 as pct_of_total,
    SUM(s.signer_burned) OVER (ORDER BY s.signer_burned DESC) / t.total_burned * 100 as cumulative_pct
FROM by_signer s
CROSS JOIN total t
ORDER BY s.signer_burned DESC
LIMIT 20
