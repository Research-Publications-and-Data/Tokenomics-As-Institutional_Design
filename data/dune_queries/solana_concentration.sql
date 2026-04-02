-- Solana SPL Token Concentration Query
-- Uses solana_utils.daily_balances (partitioned by month)
-- Parameters: Replace {{mint_address}}, {{decimals}}, {{symbol}}
-- Snapshot date: 2026-04-01

WITH daily_bal AS (
    SELECT
        token_balance_owner AS address,
        token_balance / POWER(10, {{decimals}}) AS balance
    FROM solana_utils.daily_balances
    WHERE token_mint_address = '{{mint_address}}'
      AND day = DATE '2026-04-01'
      AND month = DATE '2026-04-01'  -- partition prune
      AND token_balance > 0
),
filtered AS (
    SELECT *
    FROM daily_bal
    WHERE balance > 0
      -- Exclude known Solana exchange addresses
      AND address NOT IN (
        '5tzFkiKscjHsFKRq1DL8DW2P3RDLEP67475TzqCFMo5E', -- Binance SOL hot
        'AC5RDfQFmDS1deWZos921JfqscXdByf6BKHAbXh2pVnD', -- Binance SOL
        'GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE', -- Coinbase SOL
        'H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS', -- Coinbase Cold
        '2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm', -- Coinbase 2
        '6VKzED7MCZsxFTc1GzNhML9FDPxGGLHh8EiRBSwkpkG4', -- OKX
        'HNW4dGDsPHQjhqPxfX1PiKA6Xz8b8FHT8z7bMrVjXPT',  -- Kraken
        'BSfD6SHZigAfDWSjzD5Q41jw8LmKwtmjskCH9YHAJv9p'  -- Bybit
      )
),
ranked AS (
    SELECT
        address,
        balance,
        ROW_NUMBER() OVER (ORDER BY balance DESC) AS rank
    FROM filtered
),
top_holders AS (
    SELECT * FROM ranked WHERE rank <= 1000
),
total AS (
    SELECT SUM(balance) AS total_bal FROM top_holders
),
shares AS (
    SELECT
        t.address,
        t.balance,
        t.rank,
        t.balance / s.total_bal AS share
    FROM top_holders t
    CROSS JOIN total s
),
gini_calc AS (
    SELECT
        COUNT(*) AS n,
        SUM(share) AS sum_share,
        SUM((COUNT(*) + 1 - rank) * share) AS weighted_sum
    FROM shares
)
SELECT
    '{{symbol}}' AS token,
    SUM(s.share * s.share) AS hhi,
    1.0 - (2.0 / g.n) * g.weighted_sum / g.sum_share AS gini,
    MAX(CASE WHEN s.rank = 1 THEN s.share END) AS top1_share,
    SUM(CASE WHEN s.rank <= 5 THEN s.share ELSE 0 END) AS top5_share,
    SUM(CASE WHEN s.rank <= 10 THEN s.share ELSE 0 END) AS top10_share,
    COUNT(*) AS n_top_holders,
    (SELECT total_bal FROM total) AS total_balance_top1000,
    (SELECT COUNT(*) FROM filtered) AS total_unique_holders
FROM shares s
CROSS JOIN gini_calc g
GROUP BY g.n, g.weighted_sum, g.sum_share
