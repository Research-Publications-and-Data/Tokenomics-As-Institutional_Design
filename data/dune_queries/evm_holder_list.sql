-- EVM ERC-20 Top 1000 Holder List Export
-- Parameters: Replace {{contract_address}}, {{chain_table}}, {{decimals}}, {{symbol}}
-- Returns raw holder data for replication (Supplementary File S6)
-- Snapshot date: 2026-04-01

WITH
transfers_in AS (
    SELECT
        "to" AS address,
        SUM(CAST(value AS DOUBLE) / POWER(10, {{decimals}})) AS inflow
    FROM {{chain_table}}
    WHERE contract_address = {{contract_address}}
      AND evt_block_date <= DATE '2026-04-01'
    GROUP BY 1
),
transfers_out AS (
    SELECT
        "from" AS address,
        SUM(CAST(value AS DOUBLE) / POWER(10, {{decimals}})) AS outflow
    FROM {{chain_table}}
    WHERE contract_address = {{contract_address}}
      AND evt_block_date <= DATE '2026-04-01'
    GROUP BY 1
),
net_balances AS (
    SELECT
        COALESCE(i.address, o.address) AS address,
        COALESCE(i.inflow, 0) - COALESCE(o.outflow, 0) AS balance
    FROM transfers_in i
    FULL OUTER JOIN transfers_out o ON i.address = o.address
),
filtered AS (
    SELECT *
    FROM net_balances
    WHERE balance > 0
      AND address != 0x0000000000000000000000000000000000000000
      -- Paste exchange exclusion list from main query
      AND address NOT IN (
        0x28C6c06298d514Db089934071355E5743bf21d60,
        0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549,
        0xDFD5293D8e347dFe59E90eFd55b2956a1343963d,
        0x56Eddb7aa87536c09CCc2793473599fD21A8b17F,
        0x9696f59E4d72E237BE84fFD425DCaD154Bf96976,
        0xF977814e90dA44bFA03b6295A0616a897441aceC,
        0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8,
        0x503828976D22510aad0201ac7EC88293211D23Da,
        0xddfAbCdc4D8FfC6d5beaf154f18B778f892A0740,
        0x3cD751E6b0078Be393132286c442345e68FF0aA0,
        0xA9D1e08C7793af67e9d92fe308d5697FB81d3E43,
        0x77134cbC06cB00b66F4c7e623D5fdBF6777635EC,
        0xe93381fB4c4F14bDa253907b18faD305D799241a,
        0x5C985E89DDe482eFE97ea9f1950aD149Eb73829B,
        0xA7efAe728D2936e78BDA97dc267687568dD593f3,
        0x6cC5F688a315f3dC28A7781717a9A798a59fDA7b,
        0x236F233dBf78341d7B88b37e2faBf2CaA5271AeF,
        0x75e89d5979E4f6Fba9F97c104c2F0AFB3F1dcB88,
        0x0D0707963952f2fBA59dD06f2b425ace40b492Fe,
        0x1AB4973a48dc892Cd9971ECE8e01DcC7688f8F23,
        0x0639556F03714A74a5fEEaF5736a4A64fF70D206,
        0xd6216fC19DB775Df9774a6E33526131dA7D19a2c,
        0x2B5634C42055806a59e9107ED44D43c426E58258,
        0x267be1C1D684F78cb4F6a176C4911b741E4Ffdc0,
        0xAe2D4617c862309A3d75A0fFB358c7a5009c673F,
        0x2910543Af39abA0Cd09dBb2D50200b3E800A63D2,
        0xDA9dfA130Df4dE4673b89022EE50ff26f6EA73Cf,
        0x0681d8Db095565FE8A346fA0277bFfdE9C0eDBBF,
        0xf89d7b9c864f589bbF53a82105107622B35EaA40
      )
),
ranked AS (
    SELECT
        address,
        balance,
        ROW_NUMBER() OVER (ORDER BY balance DESC) AS rank
    FROM filtered
)
SELECT
    '{{symbol}}' AS token,
    address,
    balance,
    rank,
    balance / SUM(balance) OVER () AS share
FROM ranked
WHERE rank <= 1000
ORDER BY rank
