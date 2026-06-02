#!/usr/bin/env python3
"""TAO principal-exclusion PCA (DOT-analog, per author D2).
Coldkey-aggregated top-1000; exclude Class-5 CEX coldkeys (the big mover) via the
ground-truthed registry, plus Class-4 bridge. Report raw / principal-excluded as a
range with attribution caveat. Subnet-staking-pool (Class 3) + Opentensor foundation
(Class 2) long-tail deferred (HALT-B: raw-with-caveat fallback; TAO is non-headline L1).
"""
import csv, json, os as _os_anchor
_RR = _os_anchor.path.dirname(_os_anchor.path.abspath(__file__))
while _RR != _os_anchor.path.dirname(_RR) and not _os_anchor.path.exists(_os_anchor.path.join(_RR, "reproduce.py")):
    _RR = _os_anchor.path.dirname(_RR)
DATA = _RR
holders = list(csv.DictReader(open(f"{DATA}/data/raw/holder_lists/TAO_holders.csv")))
reg = json.load(open(f"{DATA}/data/processed/tao_exchange_coldkeys.json"))
cex = {r["coldkey"]: r["name"] for r in reg}
TAOBRIDGE = "5HiveMEoWPmQmBAb8v63bKPcFhgTGCmST1TVZNvPHSTKFLCv"  # Class-4 bridge custody

def hhi(bals):
    tot = sum(bals)
    return sum((b/tot)**2 for b in bals), tot

bals_all = [float(h["balance"]) for h in holders]
h_raw, tot = hhi(bals_all)
print(f"TAO top-{len(holders)} RAW holder-HHI = {h_raw:.6f}  (dispatch pre-excl ~0.014)")
print(f"  rank-1 share={bals_all[0]/tot:.4f}  top5={sum(bals_all[:5])/tot:.4f}  top10={sum(bals_all[:10])/tot:.4f}")

# classify
excluded = []
kept = []
for h in holders:
    a = h["address"]; b = float(h["balance"]); rk = int(h["rank"])
    if a in cex:
        excluded.append((rk, a, b, 5, f"CEX: {cex[a]}"))
    elif a == TAOBRIDGE:
        excluded.append((rk, a, b, 4, "Taobridge (bridge custody)"))
    else:
        kept.append(b)

print(f"\n=== Principal exclusions (Class 5 CEX + Class 4 bridge; registry-confirmed) ===")
exc_share = 0.0
for rk, a, b, cls, lbl in sorted(excluded):
    print(f"  rank{rk:>4} {a[:12]}... {b:>14.1f} TAO ({b/tot*100:5.2f}% top-1000) Class {cls} {lbl}")
    exc_share += b/tot
print(f"  total excluded: {len(excluded)} addresses, {exc_share*100:.2f}% of top-1000")

h_post, _ = hhi(kept)
print(f"\nTAO post-principal-exclusion holder-HHI = {h_post:.6f}  (renormalized on {len(kept)} remaining)")
print(f"  => TAO range: raw {h_raw:.4f} / principal-excluded {h_post:.4f}")
print(f"  L1 cross-section placement: vs DOT 0.0052, ALGO 0.0591, OP 0.0093, ENS 0.0494")
print(f"\nCAVEAT (report verbatim-equivalent): only registry-confirmed CEX/bridge excluded; Opentensor")
print(f"foundation (Class 2) + subnet-emission/validator-staking pools (Class 3) long-tail attribution")
print(f"deferred to future work (Substrate CEX-attribution-gap, analog to DOT's 44.4%% Class-5 gap).")
