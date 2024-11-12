import numpy as np
import matplotlib.pyplot as plt

# Simulation Parameters
initial_balance = int(input("Initial balance: "))
num_trades = int(input("Number of trades: "))
winrate = float(input("Winrate (0.0 to 1.0): "))
risk_reward = float(input("Risk-to-Reward Ratio: "))
risk_percent = float(input("Risk percentage: "))
loss_threshold = int(input("Reduce risk after X consecutive losses: "))

# Initialize tracking variables
balance = initial_balance
balances = [initial_balance]
current_risk = risk_percent
consecutive_losses = 0
max_consecutive_losses = 0
peak_balance = initial_balance
max_drawdown = 0
wins = 0

# Simulate trades
for _ in range(num_trades):
    # Determine trade outcome
    is_win = np.random.random() < winrate
    
    # Calculate profit/loss
    risk_amount = balance * (current_risk / 100)
    if is_win:
        profit = risk_amount * risk_reward
        balance += profit
        consecutive_losses = 0
        wins += 1
        # Reset risk if we're above initial balance
        if balance > initial_balance:
            current_risk = risk_percent
    else:
        balance -= risk_amount
        consecutive_losses += 1
        max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
        # Reduce risk after consecutive losses
        if consecutive_losses >= loss_threshold:
            current_risk = max(0.5, current_risk / 2)  # Minimum 0.5% risk

    # Track maximum drawdown
    peak_balance = max(peak_balance, balance)
    drawdown = (peak_balance - balance) / peak_balance
    max_drawdown = max(max_drawdown, drawdown)
    
    balances.append(balance)

# Calculate final metrics
win_rate = wins / num_trades
final_return = ((balance - initial_balance) / initial_balance) * 100

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(balances, label='Balance', color='blue', linewidth=1)
plt.axhline(initial_balance, color='gray', linestyle='--', label='Initial Balance')

# Add metrics text
plt.text(0.02, 0.98, 
         f'Final Balance: ${balance:,.2f}\n'
         f'Return: {final_return:.1f}%\n'
         f'Win Rate: {win_rate:.1%}\n'
         f'Max Drawdown: {max_drawdown:.1%}\n'
         f'Max Consecutive Losses: {max_consecutive_losses}',
         transform=plt.gca().transAxes,
         verticalalignment='top',
         bbox=dict(facecolor='white', alpha=0.7))

plt.title('Trading Simulation Results')
plt.xlabel('Trade Number')
plt.ylabel('Account Balance ($)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
