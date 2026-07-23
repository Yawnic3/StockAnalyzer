# Stock Analyzer

A Python-based stock analysis tool that downloads historical market data and calculates technical indicators to evaluate a stock’s recent performance, momentum, volatility, and trading volume.

## Features

The analyzer currently calculates:

* **1-Day Return**: Percentage change from the previous trading day
* **20-Day Momentum**: Percentage price change over the previous 20 trading days
* **20-Day Moving Average**: Average closing price over the previous 20 trading days
* **50-Day Moving Average**: Average closing price over the previous 50 trading days
* **20-Day Volatility**: Annualized volatility calculated from daily returns
* **Volume Strength**: Current trading volume compared with the average volume over the previous 20 trading days
* **Overall Stock Score**: A combined score based on the calculated indicators

## Project Structure

```text
stock-analyzer/
├── analyze.py
├── download_data.py
├── indicators.py
├── requirements.txt
└── README.md
```

### `download_data.py`

Downloads two years of adjusted daily stock data using Yahoo Finance.

The returned dataset includes:

```text
date
symbol
open
high
low
close
volume
```

### `indicators.py`

Contains reusable functions for calculating each technical indicator.

### `analyze.py`

Acts as the main entry point for the program. It downloads the requested stock data, calculates the indicators, and displays the analysis results.

## Requirements

* Python 3.10 or newer
* pandas
* NumPy
* yfinance

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/stock-analyzer.git
cd stock-analyzer
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

### macOS or Linux

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

A basic `requirements.txt` file should contain:

```text
numpy
pandas
yfinance
```

## Usage

Run the analyzer and provide a valid ticker symbol:

```bash
python analyze.py AAPL
```

Example ticker symbols:

```text
AAPL   Apple
MSFT   Microsoft
NVDA   NVIDIA
GOOGL  Alphabet
AMZN   Amazon
TSLA   Tesla
```

Example output:

```text
Stock Analysis: AAPL

Latest Closing Price: $214.50
1-Day Return: 1.24%
20-Day Momentum: 5.81%
20-Day Moving Average: $208.37
50-Day Moving Average: $201.42
Annualized Volatility: 28.16%
Volume Strength: 1.18
Overall Stock Score: 74.50
```

The exact output depends on current market data.

## Indicator Calculations

### 1-Day Return

Measures the percentage change between the latest closing price and the previous trading day’s closing price.

```text
1-Day Return = Current Close / Previous Close - 1
```

### 20-Day Momentum

Measures how much the stock price has changed over the previous 20 trading days.

```text
20-Day Momentum = Current Close / Close 20 Days Ago - 1
```

### Moving Averages

Moving averages smooth short-term price changes and make trends easier to identify.

```text
Moving Average = Average Closing Price Over the Selected Window
```

A stock trading above its moving average may indicate positive momentum, while a stock trading below its moving average may indicate weaker momentum.

### Volatility

Volatility measures the amount of variation in the stock’s daily returns. Daily volatility is annualized using 252 trading days.

```text
Annualized Volatility =
Standard Deviation of Daily Returns × √252
```

Higher volatility generally means the stock has experienced larger price movements.

### Volume Strength

Compares the latest trading volume with the stock’s average trading volume.

```text
Volume Strength =
Current Volume / Average Volume Over the Previous 20 Days
```

A value greater than `1.0` indicates that the current volume is above its recent average.

## Error Handling

The analyzer may raise an error when:

* The ticker symbol is invalid
* Yahoo Finance returns no data
* Required columns are missing
* There is not enough historical data to calculate an indicator
* The device has no internet connection

## Limitations

This project is intended for educational and analytical purposes. Technical indicators are based on historical data and cannot reliably predict future stock performance.

The overall score should not be treated as a recommendation to buy, sell, or hold a security.

## Future Improvements

Possible future features include:

* A graphical user interface
* Interactive stock charts
* Support and resistance detection
* Relative Strength Index
* Moving Average Convergence Divergence
* Bollinger Bands
* Comparison of multiple stocks
* Fundamental financial metrics
* CSV and JSON report exports
* Portfolio-level analysis
* CUDA acceleration for large datasets
* Machine-learning-based scoring

## Disclaimer

This software is provided for educational purposes only and does not constitute financial advice. Always conduct independent research and consult a qualified financial professional before making your investment decisions.


```text
RuntimeError: No data returned for INVALID
```


