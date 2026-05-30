#!/usr/bin/env python3
"""
B2 Nansen re-classification campaign (2026-05-29): parse raw Nansen top-holder
markdown + classify post-exclusion survivors via the original-methodology rule.

INPUTS (all persisted; produced by the campaign, no /tmp, no live-API at this stage):
  nansen_reclass_2026-05-29/nansen_raw/<subkey>.md     raw Nansen top-50 markdown (2 pages)
  nansen_reclass_2026-05-29/survivors_2026-05-29.json  post-exclusion top-10 survivors per token
  nansen_reclass_2026-05-29/b2_nansen_contract_map_2026-05-29.json

CLASSIFICATION RULE (verbatim from analysis/03_insider_classification.py line 125-133):
  exchange         : label contains exchange/binance/coinbase/kraken/okx/gate
  insider          : label contains team/investor/founder/vest/foundation/treasury/
                     multisig/deployer/grant
  protocol_contract: label contains bridge/escrow/gateway/locker/minter/staking/
                     comptroller/timelock/governor/migrator/distributor/reservoir
  (else)           : unlabeled / retail -> not insider (conservative)

insider_count_frac = #insider survivors / n_survivors (n=10 nominal)
insider_balance_frac = sum(share of insider survivors) / sum(share of all survivors)
  (reverse-engineered from new12_retention_vector: WLFI 0.4004 reproduces this way)

OUTPUTS:
  b2_nansen_insider_classification_v4_2026-05-29.csv   per-survivor classification
  insider_retention_vector_v4_nansen_2026-05-29.csv    recomputed insider_count_frac vector
  b2_nansen_v4_provenance_2026-05-29.json              per-address provenance (audit)
"""
import csv, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "nansen_raw")

EXCHANGE_KW = ['exchange', 'binance', 'coinbase', 'kraken', 'okx', 'gate']
INSIDER_KW = ['team', 'investor', 'founder', 'vest', 'foundation', 'treasury',
              'multisig', 'deployer', 'grant']
PROTOCOL_KW = ['bridge', 'escrow', 'gateway', 'locker', 'minter', 'staking',
               'comptroller', 'timelock', 'governor', 'migrator', 'distributor', 'reservoir']

ADDR_RE = re.compile(r'^(0x[0-9a-fA-F]{40}|[1-9A-HJ-NP-Za-km-z]{32,44})$')


def norm_key(addr):
    """EVM -> lowercase; Solana base58 -> exact case (case-sensitive)."""
    return addr.lower() if addr.startswith('0x') else addr


def clean_label(raw):
    """Strip leading emoji / zero-width / non-breaking spaces from a Nansen label cell."""
    s = raw.strip()
    # drop common Nansen emoji prefixes + zero-width chars
    s = s.replace('​', '').replace(' ', '').replace('﻿', '')
    s = re.sub(r'^[\U0001F000-\U0001FAFF☀-➿\s]+', '', s)
    return s.strip()


def parse_raw(path):
    """Parse a Nansen top-holder markdown file -> {norm_key: {address,label,ownership_pct}}."""
    out = {}
    if not os.path.exists(path):
        return out, "MISSING_FILE"
    txt = open(path, encoding='utf-8').read()
    if 'FETCH_ERROR' in txt and '|' not in txt:
        return out, "FETCH_ERROR_NO_DATA"
    for line in txt.splitlines():
        if '|' not in line:
            continue
        cells = [c.strip() for c in line.split('|')]
        # leading/trailing empty from the bordering pipes
        cells = [c for c in cells]
        if len(cells) < 11:
            continue
        addr = cells[1].strip()
        if not ADDR_RE.match(addr):
            continue  # header / separator / non-data row
        label = clean_label(cells[2])
        own = cells[9].replace('%', '').strip()
        try:
            own_pct = float(own)
        except ValueError:
            own_pct = None
        k = norm_key(addr)
        if k not in out:  # page-1 (higher) wins on dup
            out[k] = {'address': addr, 'label': label, 'ownership_pct': own_pct}
    return out, ("OK" if out else "EMPTY")


def classify(label):
    if label is None or label == '':
        return ('unlabeled', None)
    ll = label.lower()
    if any(x in ll for x in EXCHANGE_KW):
        return ('exchange', 'exchange_kw')
    if any(x in ll for x in INSIDER_KW):
        return ('insider', 'insider_kw')
    if any(x in ll for x in PROTOCOL_KW):
        return ('protocol_contract', 'protocol_kw')
    return ('other_labeled', 'no_kw_match')


def main():
    survivors = json.load(open(os.path.join(HERE, "survivors_2026-05-29.json")))
    cmap = json.load(open(os.path.join(HERE, "b2_nansen_contract_map_2026-05-29.json")))
    subkeys_by_token = {}
    for p in cmap['pulls']:
        subkeys_by_token.setdefault(p['frame_token'], []).append(p['subkey'])

    # Credit-minimization (2026-05-29): the 9 new-cohort tokens were already
    # Nansen-classified last session (author-corrected S2 boundary); reuse that
    # provenance instead of re-pulling. GTC is Social_Dead + out-of-frame; skip it.
    NEW9 = ['FXS', 'SNX', 'GNO', 'WLFI', 'ENA', 'PUMP', 'JTO', 'BONK', 'KMNO']
    SKIP = {'GTC'}
    prov_path = os.path.join(os.path.dirname(HERE), "new12_retention_provenance_2026-05-29.json")
    new9_prov_raw = json.load(open(prov_path))
    new9_prov = {}  # token -> {norm_key: {insider, label}}
    for tok, rows in new9_prov_raw.items():
        d = {}
        for r in rows:
            if 'address' in r:
                d[norm_key(r['address'])] = {'insider': bool(r.get('insider')),
                                             'label': r.get('insider_label')}
        new9_prov[tok] = d

    # parse all raw files once
    label_maps = {}
    parse_status = {}
    for ft, subs in subkeys_by_token.items():
        merged = {}
        statuses = []
        for sk in subs:
            m, st = parse_raw(os.path.join(RAW, f"{sk}.md"))
            statuses.append(f"{sk}:{st}({len(m)})")
            merged.update(m)
        label_maps[ft] = merged
        parse_status[ft] = "; ".join(statuses)

    per_survivor_rows = []
    vector_rows = []
    provenance = {}
    skipped = []
    for ft in sorted(survivors.keys()):
        if ft in SKIP:
            skipped.append(ft)
            continue
        info = survivors[ft]
        lm = label_maps.get(ft, {})
        is_new9 = ft in NEW9
        prov = []
        ins_count = 0
        ins_share = 0.0
        tot_share = 0.0
        n_matched = 0
        for s in info['survivors']:
            k = norm_key(s['address'])
            if is_new9:
                pe = new9_prov.get(ft, {}).get(k)
                hit = pe is not None
                label = pe['label'] if pe else None
                own = ''
                is_ins = bool(pe['insider']) if pe else False
                cls = 'insider' if is_ins else ('reuse_noninsider' if pe else 'unlabeled')
                src = 'new12_provenance_reuse'
            else:
                hit = lm.get(k)
                label = hit['label'] if hit else None
                own = hit['ownership_pct'] if hit else None
                cls, src = classify(label)
                is_ins = (cls == 'insider')
            ins_count += int(is_ins)
            tot_share += s['share']
            if is_ins:
                ins_share += s['share']
            if hit:
                n_matched += 1
            row = {
                'frame_token': ft, 'chain': info['chain'], 'rank': s['rank'],
                'address': s['address'], 'share': s['share'],
                'nansen_label': label if label else '',
                'nansen_ownership_pct': own if own not in (None, '') else '',
                'classification': cls, 'class_source': src,
                'insider': is_ins, 'matched_in_nansen': bool(hit),
            }
            per_survivor_rows.append(row)
            prov.append({'rank': s['rank'], 'address': s['address'], 'share': s['share'],
                         'insider': is_ins, 'insider_label': label, 'classification': cls,
                         'matched': bool(hit)})
        n = len(info['survivors'])
        frac = round(ins_count / n, 4) if n else None
        bal_frac = round(ins_share / tot_share, 4) if tot_share > 0 else 0.0
        pstat = 'new12_provenance_reuse' if is_new9 else parse_status[ft]
        vector_rows.append({'token': ft, 'insider_count': ins_count, 'n_top10': n,
                            'insider_count_frac': frac, 'insider_balance_frac': bal_frac,
                            'n_matched_in_nansen': n_matched, 'source': pstat})
        provenance[ft] = prov

    with open(os.path.join(HERE, "b2_nansen_insider_classification_v4_2026-05-29.csv"), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(per_survivor_rows[0].keys()))
        w.writeheader(); w.writerows(per_survivor_rows)
    with open(os.path.join(HERE, "insider_retention_vector_v4_nansen_2026-05-29.csv"), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(vector_rows[0].keys()))
        w.writeheader(); w.writerows(vector_rows)
    json.dump(provenance, open(os.path.join(HERE, "b2_nansen_v4_provenance_2026-05-29.json"), 'w'), indent=1)

    # console summary
    print(f"{'token':10}{'ins':>4}{'n':>3}{'frac':>7}{'balfrac':>9}{'matched':>9}  source")
    print('-' * 95)
    for v in sorted(vector_rows, key=lambda r: r['token']):
        print(f"{v['token']:10}{v['insider_count']:>4}{v['n_top10']:>3}{v['insider_count_frac']:>7}"
              f"{v['insider_balance_frac']:>9}{v['n_matched_in_nansen']:>9}  {v['source']}")
    print(f"\nskipped (out-of-frame / not pulled): {skipped}")
    low = [v['token'] for v in vector_rows
           if v['source'] != 'new12_provenance_reuse' and v['n_matched_in_nansen'] < 5]
    print(f"LOW-MATCH pulled tokens (<5/10 survivors found in Nansen page-1): {low}")
    # high-share unmatched survivors among PULLED tokens => page-2 candidates
    flips = [r for r in per_survivor_rows
             if r['class_source'] != 'new12_provenance_reuse'
             and not r['matched_in_nansen'] and r['share'] >= 0.02]
    print(f"\nHIGH-SHARE UNMATCHED survivors (share>=2%; page-2 deepen candidates): {len(flips)}")
    for r in sorted(flips, key=lambda x: -x['share']):
        print(f"    {r['frame_token']:10} rank{r['rank']:>3} share={r['share']:.4f}  addr={r['address'][:14]}")


if __name__ == "__main__":
    main()
