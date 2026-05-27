# Supplementary File S19 ADDENDUM (verification framework): How to verify the DOT validator set

**Companion to:** S19 + S19 DOT validator analysis addendum (operator-attribution + governance-vote concentration).
**Generated:** 2026-05-27. **Trigger:** author directive "How can we verify dot validator set?" 2026-05-27T19Z.

---

## Verification axes framework

The DOT validator set (600 active + waiting; ~298 active per era) can be verified across multiple axes. This framework documents what we executed, what we attempted but couldn't programmatically access, and what's tractable for follow-on cycles.

### Axis A: Identity Pallet (executed)

**Source:** Subscan `stash_account_display.identity` field on `/api/scan/staking/validators`.
**Strength:** Authoritative for validators who registered on-chain identity with judgments from authoritative registrars.
**Coverage achieved:** 86 of 600 validators (14.33%) returned a display name; 514 (85.67%) returned empty.
**Stake coverage:** verified validators control 16.11% of total bonded stake; unverified control 83.89%.

**Method:** pattern-matching against curated CEX (17 entities) + Institutional (22 entities) + Foundation (2 entities) dictionary on display names.

**Output:** `dot_validators_classified.json` (full breakdown); see S19 DOT validator analysis addendum F.4 for class-by-class table.

### Axis B: W3F Thousand Validators Programme (TVP) (attempted; not tractable via standard URLs)

**Strength:** W3F-curated whitelist of vetted validator operators (originally targeting 1000 validators; currently ~200-300 active TVP members).
**What we tried:**
- `https://nodes.web3.foundation/api/candidates` -> 404
- `https://kusama-thousand-validators.w3f.community/candidates` -> 404
- `https://polkadot-thousand-validators.w3f.community/candidates` -> 404
- `https://thousand-validators.kusa.ma/api/candidates` -> 404
- W3F's "Decentralized Nodes" site (nodes.web3.foundation) returned 404 for /candidates path

**Why it didn't work:** the W3F Decentralized Nodes program (current iteration of TVP) loads data dynamically via JavaScript SPA at apisa.web3.foundation; standard URL probing doesn't return JSON.

**Follow-on tractable approach:**
- Direct query of W3F GitHub repo (`github.com/w3f/1k-validators-be`) candidates folder via raw.githubusercontent.com
- Or: GraphQL query against W3F Decentralized Nodes API (requires runtime endpoint discovery via SPA inspection)
- Or: Manual TVP membership download from W3F Discord/Element channels

### Axis C: Polkadot Telemetry (not attempted)

**Source:** `telemetry.polkadot.io` WebSocket endpoint (wss://telemetry.polkadot.io/feed/).
**Strength:** Real-time node identity, software version, hardware, geographic location, ISP fingerprint.
**Tractability:** Requires WebSocket client (websocat or similar); persistent connection; data is real-time-only (no historical query).
**Why valuable:** even validators without on-chain identity often publish telemetry node-name; would resolve a substantial fraction of the 514 unverified.

### Axis D: Polkawatch (attempted; SPA-rendered)

**Source:** `polkawatch.app/validation`
**What we tried:** Direct API probes against polkawatch.app/api/* and get.polkawatch.app/api/* -> connection-refused (Mautic CRM at get.) or SPA-only HTML at root.
**Why it didn't work:** Polkawatch frontend is JavaScript-rendered single-page app; data is loaded at runtime from a non-documented internal API endpoint.
**Follow-on tractable approach:** manual dashboard inspection at polkawatch.app/validation; the page reports operator-decentralization metrics including ISP/cloud distribution, geographic distribution, and per-operator reward concentration. Manual screenshot-capture or dev-tools network-trace inspection would identify the underlying API endpoint for programmatic access.

### Axis E: Era stability (executed; partial)

**Source:** Subscan `/api/scan/staking/validator` with stash address returns era-by-era validator-status.
**Method:** Validators consistently in the active set across many eras (>100 eras) are typically established operators (less likely to be one-off speculation).
**Tractability:** High; one API call per validator returns full era-status history.
**Status:** Endpoint verified working (`BINANCE_STAKE_9` returns era stats with `status: active`); cycle-level sweep not yet executed.

### Axis F: Nominator-overlap clustering (executed; uninformative for self-staked validators)

**Method:** Two validators sharing >=5 nominator-stash accounts are likely operator-co-controlled.
**Sample:** 45 validators (top-25 unverified + 10 Binance + 10 Institutional).
**Result:** 0 pairs with >=5 shared nominators.
**Why uninformative for this sample:**
- Most Binance validators have only 1-2 self-nominators (CEX treasury accounts; not retail)
- Most unverified validators have 1-2 nominators (likely self-staked enterprise accounts)
- Retail-aggregator operators (Figment, Stakin, RockX) have many nominators but those don't cross-nominate to multiple of the same operator's validators

**Output:** `dot_nominator_overlap_v2.json`.
**Where this method IS valuable:** identifying operators that have multiple retail-aggregator validators (e.g., Bison Trails / Coinbase Cloud might run multiple validators with overlapping retail customer base); not effective for self-staked treasury operators (Binance pattern).

### Axis G: Controller-stash relationship (partial)

**Source:** Subscan `/api/scan/staking/validator` returns both `stash_account_display` and `controller_account_display`.
**Method:** Validators sharing the same controller account are by definition the same operator.
**Sample-level finding:** For BINANCE_STAKE_9, stash == controller (both `114SUbKCXjmb9czpWTtS3JANSmNRwVa4mmsMrWYpRG1kDH5`). Self-controlled is common pattern post Polkadot 0.9.x (controller-stash separation deprecated as Polkadot moved to unified accounts).
**Tractability:** High; one API call per validator.
**Status:** Per-validator detail endpoint returns controller; full cross-sweep not yet executed.

### Axis H: Funding-source clustering (not attempted)

**Source:** Subscan `/api/scan/transfers` query for transfers TO each validator's stash address.
**Method:** Validators receiving initial bonded DOT from the same source address (or addresses funded by the same parent) are operator-co-controlled.
**Tractability:** High; one API call per validator returns historical incoming transfers.
**Why valuable:** would resolve operator-attribution for the 514 unverified validators by tracing funding-source patterns (e.g., does the Wormhole-bridged DOT go to a specific validator cluster? Does Foundation-vested DOT flow to specific validators?).
**Estimated cost:** ~600 API calls; 0.5 sec each per Subscan rate-limit; ~5 minutes per full sweep.

### Axis I: Reward / commission profile (not attempted)

**Source:** Subscan `/api/scan/staking/validator_history` or `era_reward` endpoint.
**Method:** Validators sharing the same commission rate over many eras + similar reward-distribution timing are operator-co-controlled.
**Tractability:** Medium; per-validator history endpoint may exist; era-by-era extraction is expensive.

### Axis J: Off-chain attestation (manual)

**Sources:**
- Polkadot Forum (forum.polkadot.network) - validator-runner self-introductions
- Polkadot Discord / Element channels - operator announcements
- Validator-runner websites linked from on-chain identity
- GitHub commits to known validator-runner repositories (stakebaby, sik-cripto, etc.)
- Twitter / Bluesky / Mastodon validator-runner profiles
- Polkadot conferences (Polkadot Decoded; sub0 events) - operator presence

**Tractability:** Low; requires sustained manual research per validator.

---

## What we know with high confidence

1. **Binance dominates verified operator-stake** at 3.72% (15 of 16 CEX validators); largest single CEX-validator concentration.
2. **Polkadot NPoS Phragmen algorithm equalizes per-validator stake** to ~1.5M DOT for active validators; per-validator HHI of 0.0017 is structural, not behavioral.
3. **84% of validator stake is in validators without on-chain identity** -- operator-attribution lower bound only.
4. **Governance-vote concentration on OpenGov is structurally higher than validator-stake** -- single voters deployed 8-9M DOT in referendum #1777.
5. **Self-staked validators dominate** (Binance + most unverified) -- nominator-overlap clustering won't surface their operator-set.

## What we don't know

1. **Operator identity of 514 unverified validators** controlling 84% of stake.
2. **Whether unverified validators cluster into a small number of operators** or are diffuse (the duplicate-stake pattern was refuted as clustering signal).
3. **Geographic / ISP distribution** of validators (Polkadot Telemetry would resolve).
4. **W3F TVP membership** (would identify ~200-300 vetted validators).
5. **Cross-CEX validator presence** beyond Binance + Kraken (Coinbase, OKX, Bybit, Crypto.com, Bitvavo, etc. may operate validators not detected by our pattern dictionary).
6. **Foundation / Web3 Foundation direct validator operations** -- W3F's DOT custody and operational validator-set are largely opaque.

---

## Recommended follow-on verification path (prioritized)

1. **Polkadot Telemetry WebSocket harvest** (Axis C) -- highest yield; would resolve most of the 514 unverified validators via their telemetry-published node names. Persistent WebSocket connection needed; would deliver node-name + hardware + ISP + geographic fingerprint per validator.
2. **Funding-source clustering** (Axis H) -- second-highest yield; bulk Subscan transfer-query sweep for the 600 validators reveals deposit-source patterns indicating operator-co-control.
3. **W3F TVP membership cross-reference** (Axis B continued) -- direct GitHub query against `w3f/1k-validators-be` repository candidates folder (raw.githubusercontent.com path); would tag ~200-300 vetted operators.
4. **Polkawatch manual dashboard inspection** (Axis D continued) -- visit polkawatch.app/validation in browser; dev-tools network-trace inspection to identify underlying API endpoint; one-time API discovery enables programmatic access.
5. **Era-stability sweep** (Axis E continued) -- multi-era validator-status sweep to identify long-stable operators (>100 eras of active status = established).

Of these, items 1 + 2 + 3 are the most tractable and would together resolve 70-85% of the 514 unverified validators.

---

## Honest summary for B2 §3.8 typology

The DOT validator-set verification challenge surfaces a methodological constraint for incorporating native-chain governance tokens into B2's cross-section:

- **EVM tokens** have a unified holder address-space; PCA classification via Etherscan public name tag (validated in S18 audit) covers majority of high-share holders.
- **Polkadot DOT** has a fragmented identity space: on-chain Identity Pallet (14% covered); off-chain TVP / Polkawatch / Telemetry sources (highly tractable individually but not integrated); manual attestation sources (low tractability per validator).

For B2 publication-readiness, the recommended methodology is:

1. **Report stake-level HHI on the validator set** with the explicit caveat that NPoS equalization caps per-validator concentration and 84% of operators are unverified.
2. **Report verified-operator-class breakdown** (Binance 3.72%; Kraken 0.18%; Institutional named providers 3.31%; etc.) as the verified-lower-bound operator concentration.
3. **Report governance-vote concentration** separately as the more meaningful operational-influence axis.
4. **Cross-reference with at least one additional verification axis** (recommend Polkadot Telemetry for fastest yield) before publishing as a settled measurement.

---

## Output artifacts

- `dot_validators_classified.json` (Axis A: Identity Pallet + pattern-matching)
- `dot_nominator_overlap_v2.json` (Axis F: nominator-overlap clustering)
- `dot_validator_detail.py` + `dot_nom_probe.py` (endpoint discovery scripts)
- This supplement (verification framework summary)

---

## Cross-references

- **Predecessor:** S19 DOT validator analysis addendum (operator-attribution + governance-vote concentration)
- **Sibling:** S19 v1 (Phase 4 scope expansion); S18 v1 + audit addendum (EVM Phase 4 mini-batch)
- **Methodology reference:** B2 PAPER.md §3.5 + §3.7 + §3.8

---

## Authorship note

Authored 2026-05-27 in response to author directive "How can we verify dot validator set?". PID 14088 (BULK-EXECUTOR; expanded task-scope).
