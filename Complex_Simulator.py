import numpy as np
import matplotlib.pyplot as plt

# Simulation Parameters
initial_balance = int(input("Initial balance: "))
num_trades = int(input("Number of trades: "))
winrate = float(input("Winrate (as a decimal, e.g., 0.5 for 50%): "))
RR = float(input("Risk-to-Reward Ratio (e.g., 1.5): "))
initial_risk_percentage = float(input("Initial risk percentage (e.g., 1.0): "))
consecutive_loss_threshold = int(input("Consecutive loss threshold: "))

# Initialize variables
balance = initial_balance
balance_history = [balance]
risk_percentage = initial_risk_percentage
consecutive_losses = 0
max_consecutive_losses = 0
peak_balance = initial_balance
max_drawdown = 0
max_dd_point = 0  # Store the point of maximum drawdown
consecutive_loss_point = 0  # Store the point of maximum consecutive losses


# Function to calculate profit/loss per trade
def trade_result(win, balance, risk):
    if win:
        return balance * (risk / 100) * RR
    else:
        return -balance * (risk / 100)


# Simulate trades
for i in range(num_trades):
    # Determine if the trade is a win or loss based on the winrate
    win = np.random.rand() < winrate  # Randomly determine the outcome of the trade

    # Calculate profit or loss
    profit_loss = trade_result(win, balance, risk_percentage)
    balance += profit_loss
    balance_history.append(balance)

    # Update peak balance and calculate drawdown
    if balance > peak_balance:
        peak_balance = balance
    current_drawdown = (peak_balance - balance) / peak_balance
    if current_drawdown > max_drawdown:
        max_drawdown = current_drawdown
        max_dd_point = i + 1  # Store the current trade number

    # Reset consecutive losses and risk on a win
    if win:
        consecutive_losses = 0
        # Check if balance is above or equal to initial balance to reset the risk
        if balance >= initial_balance:
            risk_percentage = initial_risk_percentage
        else:
            # If below initial balance, keep the current risk percentage
            risk_percentage = risk_percentage
    else:
        consecutive_losses += 1
        max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
        if consecutive_losses >= consecutive_loss_threshold:
            risk_percentage = max(
                0.5, risk_percentage / 2
            )  # Ensure risk doesn't drop below 0.5%
            if (
                consecutive_losses == consecutive_loss_threshold
            ):  # Capture point when threshold is met
                consecutive_loss_point = i + 1  # Store the current trade number

# Modify the figure size to be wider
plt.figure(figsize=(12, 6))

# Plot balance history
plt.plot(
    balance_history,
    label=f"Balance (Max DD: {max_drawdown:.1%}, Max Consec. Losses: {max_consecutive_losses})",
    color="blue",
    linewidth=1,
)

plt.axhline(initial_balance, color="gray", linestyle="--", label="Initial Balance")
plt.xlabel("Number of Trades", fontsize=12)
plt.ylabel("Account Balance", fontsize=12)
plt.title(
    "Simulated Trading Performance with Dynamic Risk Management Strategy", fontsize=12
)

plt.legend(fontsize=10, loc="upper left")
plt.grid(alpha=0.3)

# Adding annotations for max drawdown
plt.scatter(
    max_dd_point,
    balance_history[max_dd_point],
    color="red",
    label="Max Drawdown Point",
    zorder=10,
)

# Adding a watermark
plt.text(
    0.5,
    0.5,
    "Simulated by @MR-ROBOT",
    fontsize=17,
    color="gray",
    alpha=0.2,
    ha="center",
    va="center",
    rotation=30,
    transform=plt.gca().transAxes,
)

# Adding input parameters as text
plt.text(
    0.012,
    0.89,  # Position at the top left
    f"Winrate: {winrate * 100:.2f}%\n"
    f"Risk-Reward Ratio: {RR}\n"
    f"Starting Risk %: {initial_risk_percentage}%\n"
    f"Consecutive Loss Threshold: {consecutive_loss_threshold}",
    fontsize=9,
    transform=plt.gca().transAxes,
    verticalalignment="top",
    bbox=dict(facecolor="white", alpha=0.2),
)

plt.tight_layout()
plt.show()
