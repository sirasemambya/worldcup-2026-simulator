# World Cup 2026 Tournament Simulator

A Monte Carlo simulator for the 48-team 2026 FIFA World Cup. It starts from market-implied win/draw/loss probabilities for every group-stage fixture, layers on a heat and crowd adjustment, and plays out the full tournament (group stage, third-place qualification, and the official knockout bracket) tens of thousands of times to estimate each team's chance of reaching each stage.

The model was built before the tournament, in early June 2026. It has not yet been scored against the actual results (see "What I'd build next").

## How it works

1. **Base probabilities.** For each group-stage fixture, `market_probs.py` pulls market-implied win/draw/loss probabilities and normalizes them so they sum to 1. Team quality is not hand-rated anywhere in the code. All of it comes from these lines.
2. **Heat and crowd adjustment.** Each venue has a heat score, each team has a heat tolerance, and each kickoff time has a heat factor (afternoon peak, evening cool-down). The difference in tolerance between the two teams, scaled by venue and time, shifts the home win probability. Knockout matches also get a small crowd adjustment for the three host nations.
3. **Knockout matches.** No market lines exist for future knockout pairings, so the simulator derives a team strength from each team's group-stage probabilities (geometric mean of expected points share) and uses a Bradley-Terry model for matchups.
4. **Goals.** Scorelines are sampled from Poisson distributions conditioned on the sampled outcome, which is needed for group tiebreakers (goal difference, goals for).
5. **Bracket.** `bracket.py` encodes the official 2026 knockout bracket, including which group positions feed each round of 32 slot and the venue and local kickoff time of every match, so the heat adjustment applies correctly through the knockout rounds.

## Data sources

| Source | What it provides |
|---|---|
| [The Odds API](https://the-odds-api.com) | Market-implied group-stage match probabilities. Requires a free API key. |
| `config.py` | Groups, the group-stage fixture list, venue heat scores, and team heat tolerances (hand-entered) |
| `bracket.py` | The knockout bracket structure, venues, and kickoff times (hand-entered) |

## Running it

```bash
pip install -r requirements.txt
export ODDS_API_KEY=your_key_here     # never commit this

python main.py                  # full run, 50,000 simulations
python main.py --sims 5000      # quick test
python main.py --no-market      # skip the API call, equal-strength baseline
python report.py                # build a formatted Excel report from model_probs.csv
```

`main.py` prints the top teams for each stage and writes `model_probs.csv`. `report.py` turns that file into a workbook with one sheet per stage.

## Sample output

Top teams by championship probability from a pre-tournament run (50,000 simulations, June 5, 2026):

| team | group | advance | R16 | QF | SF | Final | Winner |
|---|---|---|---|---|---|---|---|
| Mexico | A | 91.3% | 54.7% | 32.1% | 19.6% | 11.6% | 7.1% |
| Spain | H | 98.8% | 60.5% | 36.4% | 21.4% | 12.4% | 6.9% |
| France | I | 96.6% | 60.1% | 34.0% | 19.3% | 10.7% | 5.9% |
| Argentina | J | 96.7% | 57.0% | 33.7% | 19.0% | 10.6% | 5.9% |
| Belgium | G | 95.3% | 59.7% | 35.0% | 19.2% | 10.7% | 5.8% |
| Portugal | K | 95.2% | 61.5% | 33.8% | 18.6% | 10.1% | 5.3% |

Mexico ranking first is worth a note: it comes from a strong group-stage line, a favorable heat profile, and the host crowd adjustment stacking together, not from an independent view that Mexico is the best team.

## Key modeling choices

- **Market probabilities as the only strength signal.** Aggregated market prices already contain far more information (injuries, form, squad depth) than I could model from scratch here, so the simulator does not try to out-rate them. The contribution is the tournament structure and the venue-level heat adjustment.
- **Outcome first, goals second.** The simulator samples win/draw/loss from the adjusted probabilities, then samples a scoreline consistent with that outcome. This keeps match outcomes faithful to the input probabilities while still producing goal difference for tiebreakers.
- **Geometric mean for strength.** Averaging log probabilities stops one easy group opponent from inflating a team's knockout strength.
- **Real bracket, real venues.** Using the actual bracket and per-match venues means a team's path through the knockout rounds affects its heat exposure, rather than treating all rounds as neutral.

## Limitations

- **No independent team ratings.** If the market inputs are off, the simulation inherits that. The model can only add value through the heat, crowd, and bracket-structure layers.
- **Heat and crowd parameters are hand-set and untuned.** Venue heat scores, team heat tolerances, `HEAT_WEIGHT`, and the crowd adjustments are informed judgments, not fitted values. The code marks `HEAT_WEIGHT` as still to be tuned.
- **Simplified tiebreakers.** Group ranking uses points, goal difference, then goals for. Head-to-head and fair-play tiebreakers are not implemented.
- **Simplified third-place assignment.** Each third-place slot takes the best available qualifying third-place team from its eligible group pool, rather than using FIFA's full lookup table of allowed combinations.
- **Knockout pairings use derived strength.** They are less well informed than group fixtures, which have direct market lines. Penalty shootouts are a strength-weighted coin flip.
- **Manual fallbacks.** A few group fixtures had no market line at run time and use hand-entered fallback probabilities. One fixture venue was still a placeholder.
- **No tests.** Correctness so far has been checked by running the simulator and confirming that probabilities are internally consistent (for example, championship probabilities sum to 100%).

## What I'd build next

- Score the pre-tournament probabilities against what actually happened, using Brier score and calibration by stage, since the tournament has now been played.
- Fit the heat weight and team heat tolerances against historical tournament data instead of setting them by hand.
- Implement the full FIFA tiebreaker rules and the official third-place assignment table.
- Replace the hand-entered fixture and bracket data with a maintained data source, and add unit tests around the bracket logic.
- Add a small independent rating component (for example an Elo or xG-based prior) so the model has a view of its own to compare against the market inputs.
