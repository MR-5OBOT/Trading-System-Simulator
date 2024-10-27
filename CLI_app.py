import matplotlib.pyplot as plt
import numpy as np
import csv
import logging

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
def run_trading_simulation(
    RR,
    win_rate,
    risk_per_trade,
    total_trades,
    initial_balance,
    num_simulations,
    image_config,
):
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
            drawdown_percentage = (
                max_drawdown / peak_balance[np.argmax(peak_balance)]
            ) * 100
            if drawdown_percentage < worst_drawdown_value:
                worst_drawdown_value = drawdown_percentage
                worst_drawdown_sim = sim
                worst_drawdown_percentage = drawdown_percentage

    # Plotting
    if image_config == "single":
        fig, axs = plt.subplots(3, 1, figsize=(12, 18), tight_layout=True)
        fig.suptitle(
            f"Simulating {total_trades} Trades | "
            f"Risk: {risk_per_trade * 100:.1f}% | Win Rate: {win_rate * 100:.0f}% | RR: {RR:.1f}",
            fontsize=15,
        )
    else:
        fig, axs = plt.subplots(1, 1, figsize=(12, 6), tight_layout=True)

    # Balance history plot
    if image_config == "single":
        for sim in range(num_simulations):
            axs[0].plot(all_balances[sim], color=colors["lightblue"], alpha=0.5)
        axs[0].plot(
            average_balance, color=colors["green"], label="Average Balance", linewidth=2
        )
        axs[0].plot(
            all_balances[worst_drawdown_sim],
            color=colors["orange"],
            label="Worst Drawdown Simulation",
            linewidth=2,
        )

        peak_balance = np.maximum.accumulate(all_balances[worst_drawdown_sim])
        drawdown = all_balances[worst_drawdown_sim] - peak_balance
        max_drawdown_index = np.argmin(drawdown)
        max_drawdown_value = all_balances[worst_drawdown_sim][max_drawdown_index]

        # Highlighting the maximum drawdown point
        axs[0].scatter(
            max_drawdown_index, max_drawdown_value, color=colors["red"], zorder=5
        )

        text_y_position = max_drawdown_value - (
            0.1
            * (
                max(all_balances[worst_drawdown_sim])
                - min(all_balances[worst_drawdown_sim])
            )
        )

        axs[0].text(
            max_drawdown_index,
            text_y_position,
            f"{worst_drawdown_percentage:.2f}%",
            color=colors["red"],
            fontsize=10,
            ha="center",
            bbox=dict(facecolor="white", alpha=0.5, edgecolor="none"),
        )

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
        axs[1].bar(
            range(1, num_simulations + 1),
            max_consecutive_losses,
            color=colors["lightblue"],
            alpha=0.7,
        )
        max_consecutive_loss_index = np.argmax(max_consecutive_losses)
        axs[1].bar(
            max_consecutive_loss_index + 1,
            max_consecutive_losses[max_consecutive_loss_index],
            color=colors["salmon"],
            alpha=1,
        )
        axs[1].set_title("Maximum Consecutive Losses per Simulation", fontsize=14)
        axs[1].set_xlabel("Simulation Number", fontsize=12)
        axs[1].set_ylabel("Max Consecutive Losses", fontsize=12)
        axs[1].set_xticks(range(1, num_simulations + 1))
        axs[1].set_ylim(0, np.max(max_consecutive_losses) + 1)

    else:
        # Separate image for maximum consecutive losses
        fig, ax = plt.subplots(figsize=(12, 6), tight_layout=True)
        ax.bar(
            range(1, num_simulations + 1),
            max_consecutive_losses,
            color=colors["lightblue"],
            alpha=0.7,
        )
        ax.set_title("Maximum Consecutive Losses", fontsize=14)
        ax.set_xlabel("Simulation Number", fontsize=12)
        ax.set_ylabel("Max Consecutive Losses", fontsize=12)
        ax.set_ylim(0, np.max(max_consecutive_losses) + 1)

    # Wins and losses plot
    if image_config == "single":
        bar_width = 0.35
        x = np.arange(num_simulations)

        axs[2].bar(
            x,
            win_counts,
            width=bar_width,
            label="Wins",
            color=colors["lightblue"],
            alpha=0.7,
        )
        axs[2].bar(
            x + bar_width,
            loss_counts,
            width=bar_width,
            label="Losses",
            color=colors["salmon"],
            alpha=0.7,
        )

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

        ax.bar(
            x,
            win_counts,
            width=bar_width,
            label="Wins",
            color=colors["lightblue"],
            alpha=0.7,
        )
        ax.bar(
            x + bar_width,
            loss_counts,
            width=bar_width,
            label="Losses",
            color=colors["salmon"],
            alpha=0.7,
        )

        ax.set_title("Wins and Losses", fontsize=14)
        ax.set_xlabel("Simulation Number", fontsize=12)
        ax.set_ylabel("Count", fontsize=12)
        ax.set_xticks(x + bar_width / 2)
        ax.set_xticklabels(range(1, num_simulations + 1))
        ax.legend(fontsize=12)

    # Add watermarks to each subplot
    def add_watermark(ax):
        ax.text(
            0.5,
            0.5,
            "MRROBOT TRADES",
            fontsize=50,
            color="lightgrey",
            alpha=0.6,
            ha="center",
            va="center",
            transform=ax.transAxes,
        )

    if image_config == "single":
        add_watermark(axs[0])
    else:
        add_watermark(ax)

    plt.tight_layout(rect=[0, 0, 1, 0.97])

    # save_name = input("Export simulation at name (with .png extension): ")
    save_name = "Simulation.png"
    plt.savefig(save_name)

    # Export results to CSV
    with open("simulation_results.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Simulation", "Wins", "Losses", "Max Consecutive Losses", "Final Balance"]
        )
        for sim in range(num_simulations):
            writer.writerow(
                [
                    sim + 1,
                    win_counts[sim],
                    loss_counts[sim],
                    max_consecutive_losses[sim],
                    all_balances[sim][-1],
                ]
            )

    logging.info(f"Worst Max Drawdown Percentage: {worst_drawdown_percentage:.2f}%")
    logging.info(f"Worst Drawdown Simulation Index: {worst_drawdown_sim}")


# User input with validation
def get_float_input(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = float(input(prompt))
            if (min_value is not None and value < min_value) or (
                max_value is not None and value > max_value
            ):
                raise ValueError("Input is out of bounds.")
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_int_input(prompt, min_value=None):
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                raise ValueError("Input is out of bounds.")
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def main():
    RR = get_float_input("Enter the Risk-Reward Ratio (e.g., 1.5): ", min_value=0)
    win_rate = get_float_input(
        "Enter the Win Rate (as a decimal, e.g., 0.55 for 55%): ",
        min_value=0,
        max_value=1,
    )
    risk_per_trade = get_float_input(
        "Enter the Risk per Trade (as a decimal, e.g., 0.02 for 2%): ",
        min_value=0,
        max_value=1,
    )
    total_trades = get_int_input("Enter the Total Number of Trades: ", min_value=1)
    initial_balance = get_float_input(
        "Enter the Initial Balance (e.g., 1000): ", min_value=0
    )
    num_simulations = get_int_input("Enter the Number of Simulations: ", min_value=1)

    # Choose image configuration
    image_config = ""
    while image_config not in ["single", "separate"]:
        image_config = (
            input(
                "Do you want to save all plots in a single image or separate images? (type 'single' or 'separate'): "
            )
            .strip()
            .lower()
        )

    run_trading_simulation(
        RR,
        win_rate,
        risk_per_trade,
        total_trades,
        initial_balance,
        num_simulations,
        image_config,
    )


if __name__ == "__main__":
    main()
