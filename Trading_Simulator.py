import numpy as np
import matplotlib.pyplot as plt

# Simulation Parameters
initial_balance = int(input("initial_balance: "))  # Starting account balance
num_trades = int(input("number of trades: "))  # Number of trades in the simulation
winrate = float(input("winrate (as a decimal, 0.5 for 50%): "))  # Winrate probability
RR = float(input("Risk-to-Reward Ratio (e.g., 1.5): "))  # Risk-to-Reward Ratio

# Calculate number of wins and losses based on winrate
num_wins = int(num_trades * winrate)
num_losses = num_trades - num_wins

# Generate sequence of wins and losses
trade_outcomes = [True] * num_wins + [False] * num_losses  # True = win, False = loss
np.random.shuffle(trade_outcomes)  # Shuffle to randomize order

# Initialize variables
balance = initial_balance
balance_history = [balance]
risk_percentage = 2.0  # Start with 2% risk
in_drawdown = False  # Track if in drawdown to adjust risk
consecutive_losses = 0  # Track consecutive losses


# Function to calculate profit/loss per trade
def trade_result(win, balance, risk):
    if win:
        return balance * (risk / 100) * RR  # Profit
    else:
        return -balance * (risk / 100)  # Loss


# Simulate trades
for i in range(num_trades):
    # Get the pre-determined trade outcome
    win = trade_outcomes[i]

    # Calculate profit or loss based on the current risk
    profit_loss = trade_result(win, balance, risk_percentage)

    # Update balance
    balance += profit_loss
    balance_history.append(balance)

    # Adjust risk according to drawdown recovery rule
    if balance < initial_balance:
        in_drawdown = True

    # Adjust risk based on win or loss
    if win:
        # Reset consecutive losses on a win
        consecutive_losses = 0
        if in_drawdown and balance >= initial_balance:
            # Return to 2% risk after recovery above the initial balance
            risk_percentage = 2.0
            in_drawdown = False
    else:
        # Increment consecutive losses on a loss
        consecutive_losses += 1
        if consecutive_losses == 1:
            risk_percentage = 1.0  # Set risk to 1% after first loss
        elif consecutive_losses >= 2:
            risk_percentage = 0.5  # Set risk to 0.5% after two or more losses

# Plotting results
plt.figure(figsize=(10, 6))
plt.plot(balance_history, label="Balance Over Time")
plt.axhline(initial_balance, color="gray", linestyle="--", label="Initial Balance")
plt.xlabel("Number of Trades")
plt.ylabel("Account Balance")
plt.title("Simulated Trading Performance with Dynamic Risk Management Strategy")
plt.legend()

# Adding a watermark
plt.text(
    0.5,
    0.5,  # Position in the center of the plot (0.5, 0.5 means center)
    "Simulated by @MR-ROBOT",  # Text for the watermark
    fontsize=16,  # Font size for a fancy look
    color="gray",  # Light color to keep it subtle
    alpha=0.3,  # Transparency level (0 = fully transparent, 1 = fully opaque)
    ha="center",  # Horizontal alignment to center
    va="center",  # Vertical alignment to center
    rotation=30,  # Rotation for a stylish angle
    transform=plt.gca().transAxes,  # Transform coordinates to plot axes
)

plt.show()
