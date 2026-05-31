# Supplementary File S15 Phase 3: Voting-HHI coverage expansion to the N=52 additions (FXS, SNX, GNO, TAO, DOT)

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond
Token Allocation* (Table 6; sec 4.5 Amplification; sec 4.6.1 Voting-HHI Methodology).

**Extends:** Supplementary File S15 (voting-HHI gap inventory) and the S15 Phase 2 addendum. The cycle-1
voting-HHI coverage was thirteen protocols; the Phase 2 addendum expanded the inventory. This Phase 3
addendum adds five protocols that entered the holdings sample with the expansion to N=52 and had no
voting-HHI coverage: Frax (FXS), Synthetix (SNX), Gnosis (GNO), Bittensor (TAO), and Polkadot (DOT).

**Method (unchanged from S12):** voting-HHI is the Herfindahl index over the top-100 realized voter pool,
shares normalized within the top-N sample; top1/top5/top10 are cumulative within-sample; gini is reported
under the positive convention. Each protocol's amplification ratio is its voting-HHI divided by the
holdings-HHI of record for the same protocol (the reconciled N=52 frame values shown in Table 3).

All five rows were acquired from live, keyed governance sources and independently recomputed from the saved
per-voter data by a second pass that did not reuse the collection code; every row reproduced.

## Results

| Token | Governance unit | voting-HHI | holdings-HHI | ratio | voters | direction |
|---|---|---:|---:|---:|---:|---|
| GNO | linear 1 GNO = 1 vote (Snapshot gnosis.eth) | 0.1039 | 0.0425 | 2.45x | 481 | amplify |
| FXS | veFXS vote-escrow weight (Snapshot frax.eth) | 0.3693 | 0.0324 | 11.40x | 177 | amplify |
| SNX | quadratically-weighted staked-debt, council election (Snapshot synthetix-elections.eth) | 0.0947 | 0.0171 | 5.55x | 30 | amplify |
| TAO | validator stake share (Taostats) | 0.0721 | 0.0075 | 9.63x | 75 | amplify |
| DOT | conviction-weighted referendum vote (Subscan) | 0.1334 | 0.0052 | 25.65x | 239 | amplify |

All five amplify. FXS joins the vote-escrow class discussed in sec 4.5.2 (veCRV approximately 15x, veBAL
approximately 21x, now veFXS approximately 11.4x). Counting the remaining four in the main cross-section,
the amplification fraction rises from nine of thirteen to thirteen of eighteen (72.2 percent), with the
dispersion cases now numbering five (ENS, GMX, HNT, JUP, and Livepeer at 0.27x, the most pronounced DePIN governance disperser). The amplification range widens from a prior maximum
near 9.9x to 25.6x (DOT), with FXS at 11.4x and DOT at 25.6x both exceeding the prior maximum; DOT is an
upward outlier, so the median is the more representative central value alongside the mean.

## Per-protocol governance-unit notes

- **GNO (linear control).** Per-voter Snapshot voting power summed across 42 closed proposals within an
  18-month window, 481-voter pool. Linear one-token-one-vote with no escrow, conviction, or quadratic
  transform; the cleanest control for whether amplification depends on the weighting rule.
- **FXS (vote-escrow).** Per-voter veFXS-weighted voting power. Aggregation across proposals is reported as
  the per-voter maximum rather than the sum: over the wide proposal window one address voted in 50 of 60
  proposals, and summing would double-count the same veFXS lock as a participation-frequency artifact
  (the sum cross-check inflates to 0.905 and is retained in the raw file only). The maximum-per-voter
  measure is a defensible veFXS-stake proxy comparable to the existing narrow-window Snapshot rows.
- **SNX (election layer).** Measured at the council-election layer; the proposal layer is structurally
  un-concentratable (an equal-weight seven-seat council under a four-of-seven threshold). Per-voter
  quadratically-weighted staked debt for the most recent election (2026-01-26; 30 voters). Small-sample
  caveat: the level is high-variance at this turnout (the prior cycle, n=44, gives approximately 17x; the
  union of the last two cycles, n=65, gives approximately 13.6x); the direction (amplify) is robust across
  windows, the level is reported with this sensitivity.
- **TAO (validator stake).** Validator-stake share over the full 75-validator set (Senate seats are
  allocated by stake rank). The value is a standing-power stake snapshot, consistent with the stake-weighted
  convention used for validator-set protocols; the snapshot date is documented. A separate qualitative point:
  a three-member foundation Triumvirate holds proposal drafting and closing power that a stake index does
  not represent, so the 9.63x stake amplification is a lower bound on effective governance concentration.
- **DOT (conviction-weighted).** Conviction-weighted realized-vote concentration, pooled over 20 recent
  decided referenda (multi-track), with delegated power attributed to the delegate who wields it. The pooled
  measure is 0.1334; the per-referendum index has a median of 0.250 and a range of 0.151 to 0.450. The most
  influential effective voter is a delegate aggregator (ChaosDAO OpenGov).

## The deviations and the participation reading

Two protocols deviated from the weighting-mechanism prediction, both toward more amplification. GNO uses
linear weighting and was expected to show near-equivalence; it amplifies 2.45x. SNX uses quadratic
weighting designed to compress large-holder advantage and was expected to disperse; it amplifies 5.55x. The
most parsimonious common account is that the realized voter pool is a small, self-selected electorate that
is more concentrated than the broad holder base: GNO sees roughly 79 voters per proposal and the recent SNX
election drew 30 voting wallets. Where few holders participate, the active electorate carries more
concentration than the holder distribution regardless of the weighting rule, with the weighting mechanism
modulating rather than creating the gap.

One measurement caveat bears on the strength of this reading: the voting index is computed over the top-100
realized voters while the holdings index is computed over the broader captured holder list, so the two
indices sample populations of different depth. Part of the observed amplification reflects this convention,
which applies uniformly across the entire voting sample and matches the method used for the original
thirteen protocols, so the cross-protocol comparison is internally consistent. The participation account is
therefore offered as the most parsimonious explanation of the two deviations rather than as an isolated
causal estimate; a turnout-matched comparison (voting and holdings indices over a common depth) is the
natural next test and is noted as future work.

## Coverage

This addendum raises voting-HHI coverage to eighteen protocols and closes the voting-coverage gap recorded
in the gap inventory. The expanded evidence strengthens rather than weakens the amplification finding: every
one of the five additions amplifies, including the linear control, and the predominant-amplification reading
holds at 76.5 percent of the main cross-section.
