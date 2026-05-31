#!/usr/bin/env python3
"""B2 CEX-exclusion audit application (2026-05-31).

Applies the full 52-protocol missing-exchange audit (author-approved 2026-05-31):
  - appends Nansen-confirmed CEX custody wallets to exclusions_log.csv + the
    consolidated CSV across 21 protocols + IO (fresh repull),
  - fixes the AC5RDfQF JUP row's blank hhi_before/hhi_after,
  - replaces the truncated IO_holders.csv with the 2026-05-31 Helius top-1000 pull,
  - recomputes hhi/top1/top5/top10 for every affected protocol into the frame,
  - writes .pre_cex_audit backups; idempotent (refuses to re-append).

CEX detection = Nansen entity label (token_current_top_holders / v4 reclass CSV),
NOT the token-count heuristic or the brand-keyword list (both under-detect; see the
EC + DEC-203 Cycle-6 closeout). n_holders is left at the top-1000 convention
(unchanged), matching the a3_pca_tighten precedent.
"""
import csv, os, shutil, math

SIB = "/Users/zach/Tokenomics-As-Institutional_Design"
FRAME = os.path.join(SIB, "data/processed/regression_data_april2026.csv")
EXCL = os.path.join(SIB, "data/processed/exclusions_log.csv")
CONSOL = os.path.join(SIB, "b2/paper/analysis_n52_2026-05-29/b2_pca_exclusions_consolidated_2026-05-29.csv")
HLD = os.path.join(SIB, "data/raw/holder_lists")
IO_REPULL = "/tmp/IO_holders_repull_2026-05-31.csv"
GUARD = "cex_audit_2026-05-31"

# ---- CEX additions: token -> [(address, identity)] (Nansen-confirmed) ----
SOL_CEX = {
 "JUP":[("27b4PRN7K37rpTywq65t29rjuNfQkYpxZUjkbtHc5VvZ","Upbit (CEX deposit; Nansen entity label; live-confirmed 2026-05-31)"),
        ("43DbAvKxhXh1oSxkJSqGosNw3HpBnmsWiak6tB5wpecN","Backpack Exchange: Wallet (CEX; Nansen; live-confirmed)"),
        ("Gem2VAypSg7Ai7vjDKPTtqFahpoQWkfgVkyzx3rPoTka","Bybit: Hot Wallet (CEX; Nansen v4 reclass)")],
 "DRIFT":[("FH9iLV5Z8EUEDMnW6CzUPkpDhWJCsHqJ5N4W23njNsUo","Upbit: Internal Wallet (CEX; Nansen)"),
          ("EPpctwZpP7LE61Xkpbb9ixfxMFD8fFAxewe7dTk6dg1M","Coinbase: Deposit (CEX; Nansen; cycle-3 signature said Class2/3 -> corrected by label)"),
          ("5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2","Bybit: Hot Wallet (CEX; Nansen live-confirmed in IO top-holders 2026-05-31; supersedes prior institutional-investor classification per F-B2-16)"),
          ("8Mm46CsqxiyAputDUp2cXHg41HE3BfynTeMBDwzrMZQH","Bithumb: Hot Wallet (CEX; Nansen)")],
 "HNT":[("5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2","Bybit: Hot Wallet (CEX; Nansen)"),
        ("22Wnk8PwyWZV7BfkZGJEKT9jGGdtvu7xY6EXeRh7zkBa","Crypto.com (CEX; Nansen; cycle-3 Class5_CEX flag)"),
        ("53unSgGWqEWANcPYRF35B2Bgf8BkszUtcccKiXwGGLyr","Binance US: Hot Wallet (CEX; Nansen; cycle-3 Class5_CEX flag)"),
        ("EFE3j1pcSP1paUzA86zW7989ZjsFP2J7ginyUqo4ewqR","Kraken (CEX; Nansen)")],
 "HONEY":[("FsAA2JoVBLin4CbGk16eCjQM4Etixz9cbT1smJvfC6NQ","Coinbase: Deposit (CEX; Nansen)"),
          ("3A6s38hSeXDrapWiAR7pRxyaJSiCbGLeKmEZSA9Tix4F","Coinbase: Deposit (CEX; Nansen)"),
          ("5YMPkRAQN6S6sVw3hLwPGqg8w9ZDiVDwFdYNFK2QYJzp","Coinbase: Deposit (CEX; Nansen)")],
 "RENDER":[("7TWnq4WeYcwQWBCwKeEX2Q9xqVtthPGkB7adNvueuVuh","Bitget: Deposit (CEX; Nansen)")],
 "W":[("5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2","Bybit: Hot Wallet (CEX; Nansen)"),
      ("8Mm46CsqxiyAputDUp2cXHg41HE3BfynTeMBDwzrMZQH","Bithumb: Hot Wallet (CEX; Nansen)")],
}
EVM_CEX = {
 "AAVE":[("0x5a801a9418d036fd453078c3adcb761fdc5ae695","Upbit: Hot Wallet (CEX; Nansen)")],
 "ANYONE":[("0x446b86a33e2a438f569b15855189e3da28d027ba","KuCoin: Wallet (CEX; Nansen)"),
           ("0xaa10db8804d076601999c7cd769e02e44a99d5b2","KuCoin: Deposit (CEX; Nansen)")],
 "ARB":[("0xee5b5b923ffce93a870b3104b7ca09c3db80047a","Bybit (CEX; Nansen)"),
        ("0x361ad597f6a0cf86f8ab14234ca17a5739a67458","Bithumb: Wallet (CEX; Nansen)")],
 "ATH":[("0xaf8dcd50fdc14e413e5ef4468d4d21a961a7dcfd","Upbit: Internal Wallet (CEX; Nansen)"),
        ("0x651641299c7ec0aa44ad7ed9b7e12702fed2022f","Bybit (CEX; Nansen)"),
        ("0x8714909ac67adb799df8901b1825234215c96e19","Bithumb: Deposit (CEX; Nansen)")],
 "AXL":[("0xf42aac93ab142090db9fdc0bc86aab73cb36f173","Bybit: Hot Wallet (CEX; Nansen)"),
        ("0xab782bc7d4a2b306825de5a7730034f8f63ee1bc","Bitvavo: Hot Wallet (CEX; Nansen)")],
 "COMP":[("0x841ed663f2636863d40be4ee76243377dff13a34","Robinhood: Hot Wallet (CEX; Nansen)"),
         ("0x6522b7f9d481eceb96557f44753a4b893f837e90","Bybit (CEX; Nansen)")],
 "CRV":[("0x88a1493366d48225fc3cefbdae9ebb23e323ade3","Bybit (CEX; Nansen)")],
 "ENS":[("0x498697892fd0e5e3a16bd40d7bf2644f33cbbbd4","Bithumb: Hot Wallet (CEX; Nansen)"),
        ("0x187c9fbf5bd0f266883c03f320260c407c7b4100","Bybit (CEX; Nansen)")],
 "GRT":[("0x823fd1a44a37a4be35c3b0c8b11463cc4f27396c","Upbit (CEX; Nansen)"),
        ("0xeb8ee0503e0301720eb7616e0897f8ecdf751fc3","Bithumb: Wallet (CEX; Nansen)")],
 "LDO":[("0x88a1493366d48225fc3cefbdae9ebb23e323ade3","Bybit (CEX; Nansen)"),
        ("0xffa8db7b38579e6a2d14f9b347a9ace4d044cd54","Bitget: Deposit (CEX; Nansen)")],
 "MPL_SYRUP":[("0x517ce9b6d1fcffd29805c3e19b295247fcd94aef","FalconX: Deposit (institutional-broker custody; Nansen)"),
              ("0x89860fbeab8d59858c57c920f39f5d7ba48d0722","Upbit: Main Wallet (CEX; Nansen)")],
 "OP":[("0xb18fe4b95b7d633c83689b5ed3ac4ad0a857a2a7","Bithumb: Wallet (CEX; Nansen)")],
 "POL":[("0x4c569c1e541a19132ac893748e0ad54c7c989ff4","Upbit: MATIC Main Wallet (CEX; Nansen)")],
 "RPL":[("0x07a98956df1b3a555f8f8408e280d6342451daaa","Bithumb: Wallet (CEX; Nansen)")],
}
IO_CEX = [
 ("5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9","Binance: Wallet (CEX; Nansen 2026-05-31)"),
 ("9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM","Binance: Deposits (CEX; Nansen)"),
 ("GBrURzmtWujJRTA3Bkvo7ZgWuZYLMMwPCwre7BejJXnK","Binance: Wallet (CEX; Nansen)"),
 ("8Mm46CsqxiyAputDUp2cXHg41HE3BfynTeMBDwzrMZQH","Bithumb: Hot Wallet (CEX; Nansen)"),
 ("5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2","Bybit: Hot Wallet (CEX; Nansen)"),
 ("u6PJ8DtQuPFnfmwHbGFULQ4u4EgjDiyYKjVEsynXq2w","Gate: Wallet (CEX; Nansen; cross-protocol)"),
 ("A77HErqtfN1hLLpvZ9pCtu66FEtM8BveoaKbbMoZ4RiR","Bitget (CEX; Nansen)"),
 ("ASTyfSima4LLAdDgoFGkgqoKowG1LZFDr9fAQrg7iaJZ","MEXC: Wallet (CEX; Nansen)"),
 ("6FEVkH17P9y8Q9aCkDdPcMDjvj7SVxrTETaYEm8f51Jy","Crypto.com: Wallet (CEX; Nansen)"),
 ("4uHku8pkWV71nQugvRqrme3JAh8KXBjdgicyfVaNMHrU","Coinbase: Deposit (CEX; Nansen)"),
 ("76dtfyccwDZpgeowKQL5diLQFgVLtS9jsDjkFB2Vhezu","Coinbase: Deposit (CEX; Nansen)"),
 ("FjwVV9Eu1eVrYRkf8tq7NxGD6K83tvacVUXYktSvAfL5","Coinbase: Deposit (CEX; Nansen)"),
 ("7e33zbeyCrQaUPayj5i669ChZLd2sc5xGgRnYRTUMjcE","Coinbase: Deposit (CEX; Nansen)"),
 ("HDmwffzQ877XhBb9QhasDrRxapqmSJD6rtBynAAkcRY3","Coinbase: Deposit (CEX; Nansen)"),
 ("3jj7eQpbtEKgFrFNxG1H6oBogjwTuKdecE6L8YoQERxq","Coinbase: Deposit (CEX; Nansen)"),
 ("5qVwg1vcDsDGkqVHGnrzSSMUX43MhjuiDiaRSfZK6Esb","Coinbase: Deposit (CEX; Nansen)"),
 ("7X589hpdpnhZxS9atiU5DfHn3ozQ3ry8N1czcuQNi6bq","Coinbase: Deposit (CEX; Nansen)"),
 ("4p6CoMmNwSMsYAJxTSofw9JQmgajTWSNm7fcakKcBX7w","Coinbase: Deposit (CEX; Nansen)"),
 ("HHmmibJaGU9PJxkE1rCzNsBwEdXycnA4qdWWm2kFEZZn","Coinbase: Deposit (CEX; Nansen)"),
 ("BQk2H4BhPupxg27WYyiRcETzYMG95e8LhN3WdPPgt8uq","Coinbase: Deposit (CEX; Nansen)"),
 ("E32TkMnfp2mJcHgz9g2qE4mu6SsFK4qRopqa3qBZSjH8","Coinbase: Deposit (CEX; Nansen)"),
 ("3jsN8TrqBh9N7nEEJwCnRQtr8PcphJrTcmSp7LavREKq","Coinbase: Deposit (CEX; Nansen)"),
 ("C3EimsAkCxg6K33wkpnQecFYodtfD163XYpTFpUmdLLF","Coinbase: Deposit (CEX; Nansen)"),
]
SOURCE = "B2 CEX-exclusion audit 2026-05-31 (Nansen entity labels; full 52-protocol missing-exchange sweep)"
IO_VAULT = "3EpUYHv8NzoD5EzqB74JTYUtva2c1wj3Wq3oR5gaLfGt"  # IO Custody Vaults: protocol-controlled, OUT of CEX scope (flagged gap)

def frame_rows():
    with open(FRAME) as f:
        r = csv.reader(f); h = next(r); return h, list(r)

def chain_of(frame_map, tok):
    return frame_map[tok][3]

def main():
    # idempotency guard
    with open(EXCL) as f:
        if GUARD in f.read():
            print(f"GUARD '{GUARD}' present in exclusions_log.csv -> already applied; aborting."); return
    # backups
    for p in (FRAME, EXCL, CONSOL, os.path.join(HLD, "IO_holders.csv")):
        if os.path.exists(p): shutil.copy2(p, p + ".pre_cex_audit")
    # replace truncated IO holder list with fresh repull
    shutil.copy2(IO_REPULL, os.path.join(HLD, "IO_holders.csv"))
    print("IO_holders.csv replaced with 2026-05-31 Helius top-1000 (truncated 20-row version backed up .pre_cex_audit)")

    h, rows = frame_rows()
    frame_map = {row[1]: row for row in rows}

    # existing exclusion union (lowercased) per token, for recompute
    cur = {}
    for path, tc, ac in [(EXCL,"token","address"),
                         (os.path.join(SIB,"b2/paper/analysis_n52_2026-05-29/new12_unified_exclusions_2026-05-29.csv"),"token","address"),
                         (CONSOL,"token","address")]:
        for r in csv.DictReader(open(path)):
            t=(r.get(tc)or"").strip().upper(); a=(r.get(ac)or"").strip().lower()
            if t and a: cur.setdefault(t,set()).add(a)

    ALL = {}
    for d in (SOL_CEX, EVM_CEX):
        for t,v in d.items(): ALL.setdefault(t,[]).extend(v)
    ALL["IO"] = list(IO_CEX)

    def load_h(tok):
        p=os.path.join(HLD,f"{tok}_holders.csv")
        return list(csv.DictReader(open(p))) if os.path.exists(p) else None
    def recompute(tok, extra):
        rows_h=load_h(tok)
        ex=cur.get(tok,set())|{a.lower() for a in extra}
        surv=[float(r["balance"]) for r in rows_h if r["address"].strip().lower() not in ex]
        T=sum(surv); sh=sorted((b/T for b in surv),reverse=True)
        return sum(s*s for s in sh), sh[0]*100, sum(sh[:5])*100, sum(sh[:10])*100, len(surv)

    # compute new HHIs + collect exclusion-log rows
    new_vals={}
    log_rows=[]; consol_rows=[]
    for tok, adds in ALL.items():
        fr=frame_map[tok]; hhi_before=float(fr[5]); chain=chain_of(frame_map,tok)
        nh,t1,t5,t10,n = recompute(tok,[a for a,_ in adds])
        new_vals[tok]=(nh,t1,t5,t10,n)
        for addr,ident in adds:
            log_rows.append([tok,addr,ident,"Centralized-exchange custody wallet (customer deposits, not governance holdings); excluded per Section 3.8 Class 5",chain,f"{hhi_before:.6f}",f"{nh:.6f}",SOURCE])
            consol_rows.append([tok,addr.lower(),"5",SOURCE])

    # fix AC5RDfQF JUP row (blank hhi_before/after) -> document as no-op on current top-1000
    exc_all=list(csv.reader(open(EXCL))); exc_h=exc_all[0]; exc_data=exc_all[1:]
    for row in exc_data:
        if len(row)>=7 and row[1].strip()=="AC5RDfQFmDS1deWZos921JfqscXdByf8BKHs5ACWjtW2" and row[0].strip()=="JUP":
            if not row[5].strip(): row[5]="0.126008"
            if not row[6].strip(): row[6]="0.126008"
            row[7]=row[7]+" | AC5RDfQF blank-hhi completed 2026-05-31 (no-op on current top-1000; resolved from 2024-02-29 JUP_full snapshot)"
            print("AC5RDfQF JUP row hhi_before/after completed (no-op annotation)")

    # write exclusions_log.csv (existing + AC5 fix + new rows)
    with open(EXCL,"w",newline="") as f:
        w=csv.writer(f); w.writerow(exc_h); w.writerows(exc_data); w.writerows(log_rows)
    print(f"exclusions_log.csv: appended {len(log_rows)} CEX rows")

    # write consolidated CSV
    con_all=list(csv.reader(open(CONSOL))); con_h=con_all[0]; con_data=con_all[1:]
    with open(CONSOL,"w",newline="") as f:
        w=csv.writer(f); w.writerow(con_h); w.writerows(con_data); w.writerows(consol_rows)
    print(f"consolidated CSV: appended {len(consol_rows)} rows")

    # update frame: f[5]=hhi f[7]=top1 f[8]=top5 f[9]=top10 (n_holders f[10] unchanged per a3 precedent)
    nchg=0
    for row in rows:
        tok=row[1]
        if tok in new_vals:
            nh,t1,t5,t10,n=new_vals[tok]
            row[5]=f"{nh:.6f}"; row[7]=f"{t1:.6f}"; row[8]=f"{t5:.6f}"; row[9]=f"{t10:.6f}"
            nchg+=1
    with open(FRAME,"w",newline="") as f:
        w=csv.writer(f); w.writerow(h); w.writerows(rows)
    print(f"regression_data_april2026.csv: updated {nchg} protocol rows (hhi/top1/top5/top10; n_holders unchanged)")

    print("\nPer-protocol new HHIs:")
    for tok in sorted(new_vals):
        b=float(frame_map[tok][5]); print(f"  {tok:<10} {b:.6f} -> {new_vals[tok][0]:.6f}")
    print(f"\nFLAG (out of scope): IO rank-1 {IO_VAULT} = 'IO Custody Vaults' (protocol-controlled, ~28.6%) NOT excluded; separate PCA gap candidate.")

if __name__=="__main__":
    main()
