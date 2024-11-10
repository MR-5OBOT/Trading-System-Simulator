## 1. **Project Structure (Detailed)**

### **Inputs (Data You Will Need to Start the Simulation):**
- **Total Number of Trades (X trades)**: 
  - The total number of trades to simulate. 
  - Example: `100 trades`.

- **Risk per Trade**: 
  - The percentage of your starting capital that you are willing to risk on each trade. 
  - Example: `1%` of starting capital. 
  - If your starting capital is $10,000, risk per trade would be $100.

- **Reward-to-Risk Ratio (RR)**: 
  - This defines how much you are aiming to gain on a winning trade compared to what you risk.
  - Example: `2:1` reward-to-risk ratio (i.e., for every $1 you risk, you aim to make $2 on a winning trade).

- **Win/Loss Probability**:
  - The probability of a trade being a win or loss. 
  - Example: `50%` win rate (you have an equal chance of winning or losing each trade).

---

## 2. **Simulation Process**

### **Initialization**:
- **Starting Capital**: Set an initial amount of capital for the simulation. 
  - Example: `$10,000`.
  
- **Risk per Trade**: 
  - Determine how much of the starting capital to risk on each trade. 
  - Example: `1%` of capital, which equals `$100` for the first trade (if the starting capital is $10,000).

---

### **Loop Over X Trades**:
For each trade in your simulation (up to `X` total trades), you will perform the following steps:

1. **Random Outcome Generation**:
   - Use a random function to determine the outcome of each trade. 
     - A random number between `0` and `1` is generated.
     - If the number is below the `win rate` (e.g., less than `0.5` for 50% chance), it’s a win; otherwise, it’s a loss.

2. **Account Update**:
   - After determining if the trade is a win or a loss, update the account balance:
     - **Win**: Add `Risk * Reward-to-Risk` to the balance. 
       - Example: If `Risk = $100` and the `Reward-to-Risk = 2R`, then add `$100 * 2 = $200` to the balance.
     - **Loss**: Subtract `Risk` from the balance. 
       - Example: If `Risk = $100`, subtract `$100` from the balance.

3. **Tracking the Metrics**:
   - After each trade, record the outcome (win or loss), and update the account balance.
   - Track key performance indicators (KPIs) such as:
     - Number of wins and losses.
     - Final account balance after all trades.
     - Win rate (percentage of wins over total trades).
     - Total profit or loss from all trades.

---

## 3. **Final Output**

After all trades are completed, you will calculate and display the following:

- **Total Number of Wins and Losses**: 
  - Count the total number of wins and losses.
  - Example: `60 wins, 40 losses`.

- **Final Account Balance**: 
  - The balance after all trades are processed.
  - Example: `Final balance = $11,200` (if the initial was $10,000).

- **Win Rate**:
  - The win rate is calculated as:  
    `Win Rate = (Number of Wins / Total Trades) * 100`
  - Example: `Win Rate = (60 / 100) * 100 = 60%`.

- **Total Profit/Loss**:
  - The difference between the final account balance and the starting capital.
  - Example: `Total profit = $11,200 - $10,000 = $1,200`.

---

## 4. **Example Code for Simulation**

```python
import random

def simulate_trades(starting_capital, risk_percentage, reward_to_risk_ratio, total_trades):
    capital = starting_capital
    risk_per_trade = starting_capital * (risk_percentage / 100)
    win_count = 0
    loss_count = 0

    for _ in range(total_trades):
        # Randomly determine win or loss (50% chance)
        if random.random() <= 0.5:  # 50% win chance
            # Win: Add 2 * risk per trade
            capital += risk_per_trade * reward_to_risk_ratio
            win_count += 1
        else:
            # Loss: Subtract risk per trade
            capital -= risk_per_trade
            loss_count += 1

    win_rate = (win_count / total_trades) * 100
    total_profit_loss = capital - starting_capital

    return {
        'total_trades': total_trades,
        'wins': win_count,
        'losses': loss_count,
        'final_balance': capital,
        'win_rate': win_rate,
        'total_profit_loss': total_profit_loss
    }

# Example Usage
starting_capital = 10000
risk_percentage = 1  # 1% risk per trade
reward_to_risk_ratio = 2  # 2:1 reward-to-risk ratio
total_trades = 100  # Simulate 100 trades

result = simulate_trades(starting_capital, risk_percentage, reward_to_risk_ratio, total_trades)

print(f"Total Trades: {result['total_trades']}")
print(f"Wins: {result['wins']}, Losses: {result['losses']}")
print(f"Final Account Balance: ${result['final_balance']:.2f}")
print(f"Win Rate: {result['win_rate']:.2f}%")
print(f"Total Profit/Loss: ${result['total_profit_loss']:.2f}")
