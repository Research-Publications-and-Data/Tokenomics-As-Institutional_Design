import csv, os

# Locate JUP_holders.csv across clones
candidates = [
    "data/raw/holder_lists/JUP_holders.csv",
    "/Users/zach/b2-governance-data/data/raw/holder_lists/JUP_holders.csv",
]
holders_path = next((p for p in candidates if os.path.exists(p)), None)
print("holders_path:", holders_path)

rows = []
with open(holders_path, newline='') as f:
    r = csv.DictReader(f)
    print("holder cols:", r.fieldnames)
    for d in r:
        rows.append(d)
print("holder rows:", len(rows))

# normalize: address,balance,rank,share,token (per dispatch)
def bal(d):
    return float(d['balance'])
def addr(d):
    return d['address'].strip()

# Current JUP exclusions from exclusions_log.csv
excl_log = set()
jup_log_rows = []
with open("data/processed/exclusions_log.csv", newline='') as f:
    for d in csv.DictReader(f):
        if d['token'].strip().upper() == 'JUP':
            jup_log_rows.append(d)
            excl_log.add(d['address'].strip())
print("\nCurrent JUP exclusion-log addresses (%d):" % len(excl_log))
for d in jup_log_rows:
    print("  ", d['address'][:12], "| ident:", d.get('identity','')[:30], "| hhi_b:", d.get('hhi_before'), "hhi_a:", d.get('hhi_after'))

NEW = {
    '27b4PRN7K37rpTywq65t29rjuNfQkYpxZUjkbtHc5VvZ': 'Upbit',
    '43DbAvKxhXh1oSxkJSqGosNw3HpBnmsWiak6tB5wpecN': 'Backpack',
}

def hhi_topn(excluded):
    surv = [d for d in rows if addr(d) not in excluded]
    T = sum(bal(d) for d in surv)
    surv.sort(key=bal, reverse=True)
    shares = [bal(d)/T for d in surv]
    hhi = sum(s*s for s in shares)
    top1 = shares[0]*100
    top5 = sum(shares[:5])*100
    top10 = sum(shares[:10])*100
    return hhi, top1, top5, top10, len(surv), T

print("\n=== CURRENT state (reproduce of-record; should ~= 0.126008, top1 30.94) ===")
h,t1,t5,t10,n,T = hhi_topn(excl_log)
print(f"HHI={h:.6f} top1={t1:.2f}% top5={t5:.2f}% top10={t10:.2f}% n_surv={n} T={T:.1f}")

print("\n=== WITH new Upbit+Backpack excluded ===")
excl_new = set(excl_log) | set(NEW.keys())
h2,t12,t52,t102,n2,T2 = hhi_topn(excl_new)
print(f"HHI={h2:.6f} top1={t12:.2f}% top5={t52:.2f}% top10={t102:.2f}% n_surv={n2} T={T2:.1f}")
print(f"\nReduction: {h:.6f} -> {h2:.6f}  ({100*(h-h2)/h:.1f}% drop); top1 {t1:.2f}% -> {t12:.2f}%")

# Also show the rank-1/2/3 raw holders for sanity
rows.sort(key=lambda d:int(d['rank']) if d['rank'].strip().isdigit() else 9999)
print("\nRaw rank 1-4:")
for d in rows[:4]:
    print("  rank", d['rank'], addr(d)[:14], "bal", d['balance'], "share", d.get('share'))
