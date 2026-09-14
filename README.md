
MONTE CARLO SIMULATOR 

The project simulates a monte carlo simulation using Geometric Brownian Motion (GBM) 
using the formula:

Estimated Stock Price at time T (sT + dT) = s0 * exp( ((mu - 0.5 * (sigma**2)) * dT) + (sigma * sqrt(dT) * Z) )

dT represents change in time.
s0 represents initial stock price.
mu represents annualized drift.
0.5 * (sigma**2) is Ito's Lemma, adding volatility drag to drift.
Z represents a random sample from a standard normal distribution N(0,1)

-- Running the simulation --
Ensure the requirements are met and up-to-date.
Run in command line: 
 > python mcs.py

-- Expected Results --
The simulator should simulate 10,000 (=SIMULATIONS) price paths over 1 year (=SIMULATION_TIME),
based on historical (1008 days of data(=TIMELINE)) drift and standard normal randmoized shock 
calculation, plotting them using percentile bands.

Results also include information about loss probability, VaR, expected shortfall, median price, etc.

Limitations: Returns are considered to be normally distributed when using Geometric Brownian Motion
but rather in real-world, fat tails appear, increasing chances of extreme moves in reality. This 
shows the limitations of the model itself, make it clear to treat it as a risk baseline, rather 
than a precise forecast of events in the future.