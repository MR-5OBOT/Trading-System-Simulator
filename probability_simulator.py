import random

import matplotlib.pyplot as plt


def simulate_trading(initial_balance, risk_percent, rr_ratio, num_trades):
    # starting points
    balance = initial_balance
    balance_history = [initial_balance]
    wins = 0

    for trade in range(num_trades):
        risk_amount = balance * (risk_percent / 100)  # formula to get risk by % from current balance
        # random generation of win or loss with 50% winrate
        if random.random() > 0.5:  # 50% chance to win
            balance += risk_amount * rr_ratio  # Win 2x the risk
            wins += 1
        else:  # 50% chance to lose
            balance -= risk_amount  # Lose the risk amount

        balance_history.append(balance)

    win_rate = (wins / num_trades) * 100
    total_return = ((balance - initial_balance) / initial_balance) * 100

    print(f"Final Balance: ${balance:.2f}")
    print(f"Total Return: {total_return:.2f}%")
    print(f"Win Rate: {win_rate:.2f}%")

    # plot the balance history
    plt.style.use("ggplot")
    # plt.figure(figsize=(10, 6))
    plt.plot(balance_history)
    plt.title("Trading Simulation Results")
    plt.xlabel("Number of Trades")
    plt.ylabel("Balance ($)")
    plt.grid(True)
    plt.show()


# inputs
initial_balance = 5000
risk_percent = 1
rr_ratio = 2
num_trades = 100

simulate_trading(initial_balance, risk_percent, rr_ratio, num_trades)
