import csv, os
rows=list(csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "IO_holders_repull_2026-05-31.csv"))))
IO_CEX={  # Nansen-labeled CEX in IO top-50 (2026-05-31)
 "5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9":"Binance Wallet",
 "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM":"Binance Deposits",
 "GBrURzmtWujJRTA3Bkvo7ZgWuZYLMMwPCwre7BejJXnK":"Binance Wallet",
 "8Mm46CsqxiyAputDUp2cXHg41HE3BfynTeMBDwzrMZQH":"Bithumb Hot Wallet",
 "5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2":"Bybit Hot Wallet",
 "u6PJ8DtQuPFnfmwHbGFULQ4u4EgjDiyYKjVEsynXq2w":"Gate Wallet",
 "A77HErqtfN1hLLpvZ9pCtu66FEtM8BveoaKbbMoZ4RiR":"Bitget",
 "ASTyfSima4LLAdDgoFGkgqoKowG1LZFDr9fAQrg7iaJZ":"MEXC Wallet",
 "6FEVkH17P9y8Q9aCkDdPcMDjvj7SVxrTETaYEm8f51Jy":"Crypto.com Wallet",
 "4uHku8pkWV71nQugvRqrme3JAh8KXBjdgicyfVaNMHrU":"Coinbase Deposit",
 "76dtfyccwDZpgeowKQL5diLQFgVLtS9jsDjkFB2Vhezu":"Coinbase Deposit",
 "FjwVV9Eu1eVrYRkf8tq7NxGD6K83tvacVUXYktSvAfL5":"Coinbase Deposit",
 "7e33zbeyCrQaUPayj5i669ChZLd2sc5xGgRnYRTUMjcE":"Coinbase Deposit",
 "HDmwffzQ877XhBb9QhasDrRxapqmSJD6rtBynAAkcRY3":"Coinbase Deposit",
 "3jj7eQpbtEKgFrFNxG1H6oBogjwTuKdecE6L8YoQERxq":"Coinbase Deposit",
 "5qVwg1vcDsDGkqVHGnrzSSMUX43MhjuiDiaRSfZK6Esb":"Coinbase Deposit",
 "7X589hpdpnhZxS9atiU5DfHn3ozQ3ry8N1czcuQNi6bq":"Coinbase Deposit",
 "4p6CoMmNwSMsYAJxTSofw9JQmgajTWSNm7fcakKcBX7w":"Coinbase Deposit",
 "HHmmibJaGU9PJxkE1rCzNsBwEdXycnA4qdWWm2kFEZZn":"Coinbase Deposit",
 "BQk2H4BhPupxg27WYyiRcETzYMG95e8LhN3WdPPgt8uq":"Coinbase Deposit",
 "E32TkMnfp2mJcHgz9g2qE4mu6SsFK4qRopqa3qBZSjH8":"Coinbase Deposit",
 "3jsN8TrqBh9N7nEEJwCnRQtr8PcphJrTcmSp7LavREKq":"Coinbase Deposit",
 "C3EimsAkCxg6K33wkpnQecFYodtfD163XYpTFpUmdLLF":"Coinbase Deposit",
}
VAULT="3EpUYHv8NzoD5EzqB74JTYUtva2c1wj3Wq3oR5gaLfGt"  # IO Custody Vaults (protocol-controlled; OUT of CEX scope)
def hhi(excl):
    surv=[(r["address"],float(r["balance"])) for r in rows if r["address"] not in excl]
    T=sum(b for _,b in surv); sh=sorted((b/T for _,b in surv),reverse=True)
    return sum(s*s for s in sh), sh[0]*100, sum(sh[:5])*100, sum(sh[:10])*100, len(surv)
print("IO scenarios (fresh 2026-05-31 Helius pull, top-1000):")
h,t1,t5,t10,n=hhi(set()); print(f"  raw (no excl):            HHI={h:.6f} t1={t1:.2f} t5={t5:.2f} t10={t10:.2f} n={n}")
n_in=sum(1 for a in IO_CEX if any(r['address']==a for r in rows))
h,t1,t5,t10,n=hhi(set(IO_CEX)); print(f"  CEX-only (-{n_in} CEX, keep vault):  HHI={h:.6f} t1={t1:.2f} t5={t5:.2f} t10={t10:.2f} n={n}   <-- USE THIS (consistent w/ frame: vault incl)")
h,t1,t5,t10,n=hhi(set(IO_CEX)|{VAULT}); print(f"  CEX+vault (-{n_in+1}):       HHI={h:.6f} t1={t1:.2f} t5={t5:.2f} t10={t10:.2f} n={n}   (if vault PCA-excluded; OUT of scope, flag only)")
print(f"\n  CEX wallets found in IO top-1000: {n_in} of {len(IO_CEX)} labeled")
print(f"  frame of-record IO: 0.125136")
