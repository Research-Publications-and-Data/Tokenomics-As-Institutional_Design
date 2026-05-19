# Source-mismatch audit (2026-05-19)

User-flagged audit of the source-mismatch bug surfaced during net-flow operationalization (Morpheus AI initial net_subsidy = 14.78 vs gross 1.54).

## Summary

The bug was script-level (cross-source mixing) and is now fixed. A deeper audit reveals four categorical cases of data inconsistency across the canonical regression dataset, none of which materially affect the paper's headline findings but which should be documented for replication transparency.

## Categorical findings

### A. Genuine cross-source divergence (TT and OC give different gross subsidy values)

Protocols where the Token Terminal subsidy and on-chain subsidy disagree by more than 0.05 because they measure DIFFERENT underlying flows:

| Protocol | sub_TT | sub_OC | Cause |
|---|---:|---:|---|
| IoTeX | 39.05 | 27.80 | TT: $3.4M incentives / $88K revenue; OC: $3.8M emissions / $135K revenue |

For IoTeX, both values are INTERNALLY consistent within their source; the divergence reflects different revenue + emissions definitions across the two pipelines.

### B. Canonical-field-vs-raw-computation inconsistency

Protocols where the `subsidy_ratio_onchain` FIELD value differs from what raw on-chain `emissions_onchain_usd / revenue_onchain_usd` would compute:

| Protocol | sub_OC (canonical field) | sub_OC (raw OC computation) | Note |
|---|---:|---:|---|
| Aethir | 0.355 | 0.150 | Canonical OC = TT value; not computed from OC raw |
| io.net | 0.400 | 0.560 | Canonical OC = TT value; not computed from OC raw |
| Hivemapper | 5.46 | 5.47 | Negligible difference; both internally consistent |

The Aethir and io.net cases suggest the author chose to populate `subsidy_ratio_onchain` with the TT value rather than computing fresh from on-chain emit/rev. This is defensible if TT is judged more reliable for these protocols, but documentation of the choice is missing.

Substantive implication: if we use raw OC computation for these protocols:
- Aethir: net subsidy 0.150 (even MORE net-deflationary than canonical 0.355)
- io.net: net subsidy 0.560 (still net-deflationary; not flipping)
- Both remain in the burn-active subset under both definitions.

### C. Script-level cross-source mixing (the original Morpheus bug)

Bug location: `net_subsidy_analysis_2026-05-19.py` original implementation chose revenue and emissions from separate pipelines:

```python
# BUG: rev from TT, emit from OC -> bogus ratio
rev = rev_tt if not np.isnan(rev_tt) and rev_tt > 0 else (rev_oc if ...)
emit = inc_tt if not np.isnan(inc_tt) else (emit_oc if ...)
net_sub = emit / rev
```

Morpheus AI: rev_TT = $997K, emit_OC = $14.7M → net_sub = 14.78. Internally inconsistent (TT-revenue with OC-emit).

Fix: use `gross_subsidy` (canonical field, internally consistent within its source) as truth:

```python
net_sub = max(0, gross_subsidy - burns_usd / revenue_usd)
```

Morpheus AI now correctly net_sub = 1.54 (matching gross). The bug was confined to the net-flow analysis script; no other paper-cited numbers were affected.

### D. Filecoin sub_OC value provenance

Filecoin canonical `subsidy_ratio_onchain` = 21.6 with `revenue_onchain_usd` empty. The 21.6 value cannot be computed from the on-chain raw fields visible in the CSV. Likely sourced from a separate pipeline (Messari Q2/Q3 2025 reports referenced in the CSV notes). Documenting as provenance gap.

## Implications for the paper

1. The net-flow analysis (Section 3.7) uses `gross_subsidy` as truth (the canonical field). Aethir, io.net, and Filecoin's gross subsidies are taken at the canonical CSV value. This is the same convention used by the gross-flow subsidy analysis (Section 3.4 + Section 3.7 subsidy multivariate paragraphs). No headline finding is affected.

2. Under raw-OC re-computation (sensitivity check):
   - Aethir: gross 0.355 -> 0.150 (more net-deflationary)
   - io.net: gross 0.400 -> 0.560 (still net-deflationary)
   - Hivemapper: 5.46 -> 5.47 (negligible)
   Burn-active subset membership preserved under both conventions.

3. The cross-source IoTeX divergence (TT 39.05 vs OC 27.80) does not affect classification: IoTeX is net-inflationary under both definitions and remains so under net-flow.

4. The Morpheus AI script bug has been fixed; future cycles should use `gross_subsidy` field as the canonical truth source.

## Recommended follow-up (deferred)

If a future cycle wishes to harmonize the canonical `subsidy_ratio_onchain` field with raw OC computation:
- Aethir: update to 0.150
- io.net: update to 0.560
- Document the convention choice in S6 Address Methodology supplement.

This is a methodological refinement, not a data correction; both values are defensible (TT preference vs OC raw). Deferring to maintain consistency with the prior R1 / R2 subsidy multivariate analyses that used the canonical values.

## Audit verification

The script `net_subsidy_analysis_2026-05-19.py` now uses `gross_subsidy` as the single source of truth, eliminating cross-source mixing. The `net_flow_burn_data_2026-05-19.csv` data is independent and was not affected by this bug (burn USD values are computed from raw burn-side data with explicit price multiplication).
