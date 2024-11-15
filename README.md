# Formulas, inputs, examples

inputs:
- initial_balance
- risk_percent
- rr_ratio
- num_trades

expected value:
- EV = (Probability of Win × Win Amount) - (Probability of Loss × Loss Amount)

logic of the simple simulator:
- 50% chance to win 2x the risk
- 50% chance to lose the risk amount

```
in any system the Risk to Reward ratio is important than the winrate.
bc the winrate will never be a fixed number in the short term,
and even in the long term but with algo trading it can be more predictable.
```