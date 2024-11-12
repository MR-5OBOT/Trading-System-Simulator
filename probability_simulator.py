import random
import matplotlib.pyplot as plt

def simulate_trading(initial_balance=10000, risk_percent=1, rr_ratio=2, num_trades=100):
    balance = initial_balance
    balance_history = [initial_balance]
    wins = 0
    
    for trade in range(num_trades):
        # Risk 1% of current balance
        risk_amount = balance * (1/100)  # This is the 1% risk
        
        if random.random() > 0.5:  # 50% chance to win
            balance += risk_amount * rr_ratio  # Win 2x the risk
            wins += 1
        else:  # 50% chance to lose
            balance -= risk_amount  # Lose the risk amount
            
        balance_history.append(balance)
    
    win_rate = (wins/num_trades) * 100
    total_return = ((balance - initial_balance)/initial_balance) * 100
    
    print(f"Final Balance: ${balance:.2f}")
    print(f"Total Return: {total_return:.2f}%")
    print(f"Win Rate: {win_rate:.2f}%")
    
    plt.plot(balance_history)
    plt.title('Trading Simulation Results')
    plt.xlabel('Number of Trades')
    plt.ylabel('Balance ($)')
    plt.grid(True)
    plt.show()

simulate_trading()
