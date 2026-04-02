-- Dune Query 6923474: GEODNET Monthly Emissions (Solana)
-- https://dune.com/queries/6923474
-- GEOD Token Mint: 7JA5eZdCzztSfQbJvS8aVVxMFfd81Rs9VvwnocV1mKHu
-- Companion to query 6917159 (burns)

WITH mints AS (
    SELECT
        call_block_date,
        call_block_time,
        call_tx_signer,
        call_tx_id,
        CAST(amount AS DOUBLE) / 1e9 as geod_minted,
        'mintTo' as mint_type
    FROM spl_token_solana.spl_token_call_mintto
    WHERE account_mint = '7JA5eZdCzztSfQbJvS8aVVxMFfd81Rs9VvwnocV1mKHu'
        AND call_block_date >= DATE '2024-01-01'

    UNION ALL

    SELECT
        call_block_date,
        call_block_time,
        call_tx_signer,
        call_tx_id,
        CAST(amount AS DOUBLE) / 1e9 as geod_minted,
        'mintToChecked' as mint_type
    FROM spl_token_solana.spl_token_call_minttochecked
    WHERE account_mint = '7JA5eZdCzztSfQbJvS8aVVxMFfd81Rs9VvwnocV1mKHu'
        AND call_block_date >= DATE '2024-01-01'
)

SELECT
    date_trunc('month', call_block_time) as month,
    COUNT(*) as mint_tx_count,
    SUM(geod_minted) as geod_emitted,
    COUNT(DISTINCT call_tx_signer) as unique_mint_signers
FROM mints
GROUP BY 1
ORDER BY 1
