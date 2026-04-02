-- Dune Query 6917159: GEODNET Monthly Burns (Solana)
-- https://dune.com/queries/6917159
-- GEOD Token Mint: 7JA5eZdCzztSfQbJvS8aVVxMFfd81Rs9VvwnocV1mKHu

WITH burns AS (
    SELECT
        call_block_date,
        call_block_time,
        call_tx_signer,
        call_tx_id,
        CAST(amount AS DOUBLE) as raw_amount,
        'burn' as burn_type
    FROM spl_token_solana.spl_token_call_burn
    WHERE account_mint = '7JA5eZdCzztSfQbJvS8aVVxMFfd81Rs9VvwnocV1mKHu'
        AND call_block_date >= DATE '2024-01-01'

    UNION ALL

    SELECT
        call_block_date,
        call_block_time,
        call_tx_signer,
        call_tx_id,
        CAST(amount AS DOUBLE) as raw_amount,
        'burnChecked' as burn_type
    FROM spl_token_solana.spl_token_call_burnchecked
    WHERE account_mint = '7JA5eZdCzztSfQbJvS8aVVxMFfd81Rs9VvwnocV1mKHu'
        AND call_block_date >= DATE '2024-01-01'
)

SELECT
    date_trunc('month', call_block_time) as month,
    COUNT(*) as burn_tx_count,
    SUM(raw_amount / 1e9) as geod_burned,
    COUNT(DISTINCT call_tx_signer) as unique_signers
FROM burns
GROUP BY 1
ORDER BY 1
