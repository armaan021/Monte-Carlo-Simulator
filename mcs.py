import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def run_simulation(ticker):
    TIMELINE = 1008
    SIMULATION_TIME = 1
    SIMULATIONS = 10000

    close_price = yf.download(ticker, period=f'{TIMELINE}d', interval='1d', progress=False)['Close']
    if close_price.empty or close_price.isna().any().any():
        close_price = close_price.dropna()

    log_returns = np.log(close_price / close_price.shift(1)).dropna()

    mu = (log_returns.mean() * 252).item()
    sigma = (log_returns.std() * np.sqrt(252)).item()
    s0 = close_price.iloc[-1].item()

    dt = 1/252
    num_steps = int(SIMULATION_TIME / dt)

    np.random.seed(42)

    Z = np.random.standard_normal((num_steps, SIMULATIONS))
    daily_factors = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)

    price_paths = np.zeros((num_steps + 1, SIMULATIONS))
    price_paths[0, :] = s0

    for t in range(1, num_steps + 1):
        price_paths[t, :] = price_paths[t-1, :] * daily_factors[t-1, :]

    plt.figure(figsize=(12, 6))
    plt.style.use('seaborn-v0_8-darkgrid')
    historical_dates = close_price.index
    plt.plot(historical_dates, close_price, label='Historical Price', color='black', linewidth=2)
    plt.axvline(close_price.index[-1], color='red', linestyle='dashed', label='Simulation Start')

    future_prices = pd.date_range(start=close_price.index[-1], periods=num_steps + 1)[1:]

    # # Plotting 200 of the 10,000 price paths
    # num_paths_to_plot = 200
    # plot_indices = np.random.choice(SIMULATIONS, num_paths_to_plot, replace=False)
    # plt.plot(future_prices, price_paths[1:, plot_indices], lw=1, alpha=0.3, color='blue')

    # Plotting using percentile bands
    percentiles = [5, 25, 50, 75, 95]
    pct_paths = np.percentile(price_paths, percentiles, axis=1)

    plt.fill_between(future_prices, pct_paths[0, 1:], pct_paths[4,1:], color='blue', alpha=0.15, label='5th-95th percentile')
    plt.fill_between(future_prices, pct_paths[1, 1:], pct_paths[3,1:], color='blue', alpha=0.35, label='25th-75th percentile')
    plt.plot(future_prices, pct_paths[2,1:], color='blue', linewidth=1.5, label='Median Price')

    print("Prediction metrics:")
    print(f"  Probability of a loss = {(np.mean(price_paths[-1] < s0) * 100):.2f}%")
    print(f"""  Median Price in {SIMULATION_TIME} yr(s) = ${pct_paths[2,-1]:.2f}
  5th Percentile = ${pct_paths[0,-1]:.2f}
  25th Percentile = ${pct_paths[1,-1]:.2f}
  75th Percentile = ${pct_paths[3,-1]:.2f}
  95th Percentile = ${pct_paths[4,-1]:.2f}""")
    print(f"""  Annuallized dift (mu) = {(mu * 100):.2f}%
  Annualized Volatility (sigma) = {(sigma * 100):.2f}%""")

    final_prices = price_paths[-1]
    returns = (final_prices - s0) / s0
    var_95 = np.percentile(returns, 5)
    es_95 = returns[returns <= var_95].mean()

    print(f"  95% VaR = {(var_95 * 100):.2f}%") # 5% chance of losing more than this
    print(f"  Expected Shortfall (95%) = {(es_95 * 100):.2f}%") # average loss in that 5%

    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def main():
    running = True
    while (running):
        ticker = input("Search Ticker (press enter to exit): ")
        if (ticker != ''):
            run_simulation(ticker)
        else:
            running= False

if __name__ == "__main__":
    main()

