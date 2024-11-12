# Trading System Simulator

A Python-based trading simulator that implements dynamic risk management strategies based on consecutive losses. The simulator helps analyze trading performance under different probability scenarios with adjustable risk parameters.

## Core Logic

### Risk Management
- Implements dynamic risk reduction after consecutive losses
- Risk is halved when consecutive losses reach the threshold
- Minimum risk floor of 0.5%
- Risk resets to initial value when balance exceeds starting balance

### Trade Simulation
- Uses random probability distribution for trade outcomes
- Calculates profit/loss based on:
  - Current balance
  - Risk percentage
  - Risk-to-Reward ratio
- Tracks key metrics:
  - Maximum drawdown
  - Peak balance
  - Consecutive losses
  - Balance history

## Input Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| Initial Balance | Starting account value | 10000 |
| Number of Trades | Total trades to simulate | 100 |
| Winrate | Probability of winning trades | 0.45 (45%) |
| Risk-to-Reward Ratio | Profit target relative to risk | 1.5 |
| Initial Risk Percentage | Starting risk per trade | 1.0 |
| Consecutive Loss Threshold | Trades before risk reduction | 3 |

## Output Visualization

The simulator generates a plot showing:
- Account balance progression over time
- Initial balance reference line
- Maximum drawdown point marker
- Performance statistics including:
  - Maximum drawdown percentage
  - Maximum consecutive losses
- Input parameters summary

## Requirements
- Python 3.x
- NumPy
- Matplotlib

## Installation

1. Clone the repository:
   ```bash
   git clone [your-repo-url]
   cd trading-system-simulator
   ```

2. Install requirements:
   ```bash
   pip install numpy matplotlib
   ```

## Usage

Run the simulator:
```bash
python Trading_Simulator.py
```

Follow the prompts to input your simulation parameters.

