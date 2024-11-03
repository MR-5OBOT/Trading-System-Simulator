import matplotlib.pyplot as plt
import numpy as np
import csv
import logging
import tkinter as tk
from tkinter import messagebox

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Custom color palette
colors = {
    "lightblue": "#87CEFA",
    "green": "#3CB371",
    "orange": "#FFA500",
    "red": "#FF4500",
    "salmon": "#FA8072",
}

# Function to run the trading simulation
def run_trading_simulation(RR, win_rate, risk_per_trade, total_trades, initial_balance, num_simulations, image_config):
    all_balances = np.zeros((num_simulations, total_trades + 1))
    win_counts = np.zeros(num_simulations)
    loss_counts = np.zeros(num_simulations)
    max_consecutive_losses = np.zeros(num_simulations)

    for sim in range(num_simulations):
        balance_history = [initial_balance]
        current_balance = initial_balance
        wins = 0
        losses = 0
        consecutive_losses = 0
        max_losses = 0

        for trade in range(total_trades):
            if np.random.rand() < win_rate:
                current_balance += (risk_per_trade * current_balance) * RR
                wins += 1
                consecutive_losses = 0
            else:
                current_balance -= risk_per_trade * current_balance
                losses += 1
                consecutive_losses += 1
                max_losses = max(max_losses, consecutive_losses)

            balance_history.append(current_balance)

        all_balances[sim] = balance_history
        win_counts[sim] = wins
        loss_counts[sim] = losses
        max_consecutive_losses[sim] = max_losses

    average_balance = np.mean(all_balances, axis=0)
    worst_drawdown_value = np.inf
    worst_drawdown_percentage = 0
    worst_drawdown_sim = None

    for sim in range(num_simulations):
        peak_balance = np.maximum.accumulate(all_balances[sim])
        drawdown = all_balances[sim] - peak_balance
        max_drawdown = drawdown.min()

        if np.any(peak_balance > 0):
            drawdown_percentage = (max_drawdown / peak_balance[np.argmax(peak_balance)]) * 100
            if drawdown_percentage < worst_drawdown_value:
                worst_drawdown_value = drawdown_percentage
                worst_drawdown_sim = sim
                worst_drawdown_percentage = drawdown_percentage

    # Plotting
    if image_config == "single":
        fig, axs = plt.subplots(3, 1, figsize=(12, 18), tight_layout=True)
        fig.suptitle(f"Simulating {total_trades} Trades | Risk: {risk_per_trade * 100:.1f}% | Win Rate: {win_rate * 100:.0f}% | RR: {RR:.1f}", fontsize=15)
    else:
        fig, axs = plt.subplots(1, 1, figsize=(12, 6), tight_layout=True)

    # Balance history plot
    if image_config == "single":
        for sim in range(num_simulations):
            axs[0].plot(all_balances[sim], color=colors["lightblue"], alpha=0.5)
        axs[0].plot(average_balance, color=colors["green"], label="Average Balance", linewidth=2)
        axs[0].plot(all_balances[worst_drawdown_sim], color=colors["orange"], label="Worst Drawdown Simulation", linewidth=2)

        peak_balance = np.maximum.accumulate(all_balances[worst_drawdown_sim])
        drawdown = all_balances[worst_drawdown_sim] - peak_balance
        max_drawdown_index = np.argmin(drawdown)
        max_drawdown_value = all_balances[worst_drawdown_sim][max_drawdown_index]

        # Highlighting the maximum drawdown point
        axs[0].scatter(max_drawdown_index, max_drawdown_value, color=colors["red"], zorder=5)

        text_y_position = max_drawdown_value - (0.1 * (max(all_balances[worst_drawdown_sim]) - min(all_balances[worst_drawdown_sim])))

        axs[0].text(max_drawdown_index, text_y_position, f"{worst_drawdown_percentage:.2f}%", color=colors["red"], fontsize=10, ha="center", bbox=dict(facecolor="white", alpha=0.5, edgecolor="none"))

        axs[0].set_title("Account Balance Over Time", fontsize=14)
        axs[0].set_xlabel("Number of Trades", fontsize=12)
        axs[0].set_ylabel("Account Balance ($)", fontsize=12)
        axs[0].legend(fontsize=12)

    else:
        # Separate image for balance history
        axs.plot(all_balances[worst_drawdown_sim], color=colors["orange"], linewidth=2)
        axs.set_title("Account Balance Over Time", fontsize=14)
        axs.set_xlabel("Number of Trades", fontsize=12)
        axs.set_ylabel("Account Balance ($)", fontsize=12)

    # Maximum consecutive losses plot
    if image_config == "single":
        axs[1].bar(range(1, num_simulations + 1), max_consecutive_losses, color=colors["lightblue"], alpha=0.7)
        max_consecutive_loss_index = np.argmax(max_consecutive_losses)
        axs[1].bar(max_consecutive_loss_index + 1, max_consecutive_losses[max_consecutive_loss_index], color=colors["salmon"], alpha=1)
        axs[1].set_title("Maximum Consecutive Losses per Simulation", fontsize=14)
        axs[1].set_xlabel("Simulation Number", fontsize=12)
        axs[1].set_ylabel("Max Consecutive Losses", fontsize=12)
        axs[1].set_xticks(range(1, num_simulations + 1))
        axs[1].set_ylim(0, np.max(max_consecutive_losses) + 1)

    else:
        # Separate image for maximum consecutive losses
        fig, ax = plt.subplots(figsize=(12, 6), tight_layout=True)
        ax.bar(range(1, num_simulations + 1), max_consecutive_losses, color=colors["lightblue"], alpha=0.7)
        ax.set_title("Maximum Consecutive Losses", fontsize=14)
        ax.set_xlabel("Simulation Number", fontsize=12)
        ax.set_ylabel("Max Consecutive Losses", fontsize=12)
        ax.set_ylim(0, np.max(max_consecutive_losses) + 1)

    # Wins and losses plot
    if image_config == "single":
        bar_width = 0.35
        x = np.arange(num_simulations)

        axs[2].bar(x, win_counts, width=bar_width, label="Wins", color=colors["lightblue"], alpha=0.7)
        axs[2].bar(x + bar_width, loss_counts, width=bar_width, label="Losses", color=colors["salmon"], alpha=0.7)

        axs[2].set_title("Wins and Losses per Simulation", fontsize=14)
        axs[2].set_xlabel("Simulation Number", fontsize=12)
        axs[2].set_ylabel("Count", fontsize=12)
        axs[2].set_xticks(x + bar_width / 2)
        axs[2].set_xticklabels(range(1, num_simulations + 1))
        axs[2].legend(fontsize=12)

    else:
        # Separate image for wins and losses
        fig, ax = plt.subplots(figsize=(12, 6), tight_layout=True)
        bar_width = 0.35
        x = np.arange(num_simulations)

        ax.bar(x, win_counts, width=bar_width, label="Wins", color=colors["lightblue"], alpha=0.7)
        ax.bar(x + bar_width, loss_counts, width=bar_width, label="Losses", color=colors["salmon"], alpha=0.7)

        ax.set_title("Wins and Losses", fontsize=14)
        ax.set_xlabel("Simulation Number", fontsize=12)
        ax.set_ylabel("Count", fontsize=12)
        ax.set_xticks(x + bar_width / 2)
        ax.set_xticklabels(range(1, num_simulations + 1))
        ax.legend(fontsize=12)

    # Add watermarks to each subplot
    def add_watermark(ax):
        ax.text(0.5, 0.5, "MRROBOT TRADES", fontsize=50, color="lightgrey", alpha=0.6, ha="center", va="center", transform=ax.transAxes)

    if image_config == "single":
        add_watermark(axs[0])
    else:
        add_watermark(ax)

    plt.tight_layout(rect=[0, 0, 1, 0.97])

    save_name = "Simulation_Results.png"
    plt.savefig(save_name)
    logging.info(f"Results saved as {save_name}")
    plt.show()

class TradingSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Simulation")

        self.create_widgets()
        
        self.num_simulations = 100  # Default value
        self.image_config = "single"  # Default image configuration

    def create_widgets(self):
        self.RR_label = tk.Label(self.root, text="Risk-Reward Ratio (RR):")
        self.RR_label.pack()
        self.RR_entry = tk.Entry(self.root)
        self.RR_entry.pack()

        self.win_rate_label = tk.Label(self.root, text="Win Rate (as a decimal):")
        self.win_rate_label.pack()
        self.win_rate_entry = tk.Entry(self.root)
        self.win_rate_entry.pack()

        self.risk_per_trade_label = tk.Label(self.root, text="Risk per Trade (as a decimal):")
        self.risk_per_trade_label.pack()
        self.risk_per_trade_entry = tk.Entry(self.root)
        self.risk_per_trade_entry.pack()

        self.total_trades_label = tk.Label(self.root, text="Total Trades:")
        self.total_trades_label.pack()
        self.total_trades_entry = tk.Entry(self.root)
        self.total_trades_entry.pack()

        self.initial_balance_label = tk.Label(self.root, text="Initial Balance:")
        self.initial_balance_label.pack()
        self.initial_balance_entry = tk.Entry(self.root)
        self.initial_balance_entry.pack()

        self.num_simulations_label = tk.Label(self.root, text="Number of Simulations:")
        self.num_simulations_label.pack()
        self.num_simulations_entry = tk.Entry(self.root)
        self.num_simulations_entry.pack()

        self.image_config_label = tk.Label(self.root, text="Image Configuration:")
        self.image_config_label.pack()
        self.image_config_var = tk.StringVar(value="single")
        self.image_config_dropdown = tk.OptionMenu(self.root, self.image_config_var, "single", "separate")
        self.image_config_dropdown.pack()

        self.run_button = tk.Button(self.root, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack()

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_application)
        self.quit_button.pack()

    def run_simulation(self):
        try:
            RR = float(self.RR_entry.get())
            win_rate = float(self.win_rate_entry.get())
            risk_per_trade = float(self.risk_per_trade_entry.get())
            total_trades = int(self.total_trades_entry.get())
            initial_balance = float(self.initial_balance_entry.get())
            self.num_simulations = int(self.num_simulations_entry.get())
            self.image_config = self.image_config_var.get()

            # Run the trading simulation
            run_trading_simulation(RR, win_rate, risk_per_trade, total_trades, initial_balance, self.num_simulations, self.image_config)

            # Show a success message
            messagebox.showinfo("Simulation Complete", "The simulation has completed successfully!")

        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid input values.")

    def quit_application(self):
        self.root.quit()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def destroy(self):
        self.on_closing()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingSimulationApp(root)

    # Override the default close behavior
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    root.mainloop()
