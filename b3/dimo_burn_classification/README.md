# DIMO null-address transfers on Polygon, classified transaction by transaction (B3 v18)

B3 through v17 reported a DIMO monthly S2R (burns over issuance) of 4.24 from
`data/dune_queries/03_dimo_s2r.sql`, which counts every DIMO ERC-20 transfer to the
null address (or `0x...dEaD`) on Polygon as a burn. This directory classifies each of
those transfers by the function it reaches on the DIMO token. The classification is
why B3 v18 reports no DIMO S2R and no longer plots DIMO in Figure 4.

## Result

Window: every transfer from 2024-01-01 up to 2026-03-01 (the same bounds as
`03_dimo_s2r.sql`; 26 months, 2024-01 to 2026-02).

| Class | Function reached on the DIMO token | Transfers | DIMO | Share of volume |
|---|---|---:|---:|---:|
| Polygon PoS bridge exit | `withdraw(uint256)`, permissionless | 3,405 | 280,903,087.65 | 99.600% |
| Wormhole NTT bridge | `burn(uint256)`, called by DIMO's two NTT managers | 108 | 1,092,306.30 | 0.387% |
| DIMO Credit (DCX) purchase | `burn(address,uint256)`, called by the DCX token | 55 | 36,184.79 | 0.013% |
| Unclassified | | 0 | 0 | 0 |
| **Total** | | **3,568** | **282,031,578.74** | **100%** |

Bridge exits are 99.987 percent of the volume. The transfers come from 467 distinct
senders. Credit-purchase burns occur only from June to December 2024 (40 distinct
transaction origins), and every one is sent by the DCX contract, not by the buyer.

4.24 matches no month of the published series (`data/processed/dimo_s2r_monthly.csv`;
February 2026 reads 2.9734). The cumulative ratio at the series' last row,
282,031,578.74 burned over 66,301,196.68 issued, is 4.2538, within 0.33 percent of
4.24. That is the leading explanation of the figure; it is an inference from the
numbers, not a record of how 4.24 was computed. B3 v18 (Section 5.2.1) reads the
issuance side of the same query as bridge inflow, so under any window the ratio
measures bridge flow rather than burns against emissions.

## Files

- `dimo_burn_sender_detail.sql`: the transfer-level Dune query. One row per
  null-address transfer, carrying the transaction's entry-point contract and method
  selector, plus the issuance side aggregated per month and recipient.
- `dimo_burn_sender_detail_2026-08-27.json`: its archived result set (the Dune API
  response from one execution on 2026-08-27).
- `dimo_burn_calldata_decode.py` and `dimo_burn_calldata_decode_2026-08-27.json`: for
  the 305 transactions that do not call `withdraw(uint256)` on the token directly, the
  unwrapped call chain (Gelato relay, Safe `execTransaction` and `multiSend`, ERC-4337
  `handleOps`, smart-account `execute`) and the burn call it reaches, cached from public
  Polygon RPC endpoints.
- `dimo_burn_construct_series.py`: the classifier. It writes
  `dimo_burn_classified_monthly.csv` (each month's volume by class beside the published
  ratio) and `dimo_burn_classified_summary.json` (totals, shares, sender concentration).
- `dimo_s2r_monthly.csv`: a byte-identical copy of `data/processed/dimo_s2r_monthly.csv`,
  which the classifier reconciles against.

## Reproduce

From this directory, with Python 3 and its standard library only, and no network:

```
python3 dimo_burn_calldata_decode.py --check
python3 dimo_burn_construct_series.py --check
```

The first confirms that every one of the 305 non-direct transactions has a decoded burn
call in the cache (0 missing, 0 errors). The second rebuilds both outputs, reconciles
every month's burn and issuance totals to the published series (26 of 26, 0
mismatches), and requires zero unclassified transfers. `git diff` afterwards shows the
rebuilt CSV is byte-identical to the committed one. The summary JSON can differ in the
last two or three digits of two floating-point fields on another Python build
(summation order); every count and share above reproduces exactly.

`python3 dimo_burn_calldata_decode.py --refresh` re-fetches the decode from public
Polygon RPC endpoints. Re-running the query itself needs a Dune account.
