# LuxAlgo TradingView CSV Parser

A Python package for parsing and formatting CSV data exported from TradingView, specifically designed for LuxAlgo® indicators.

## Features

- 📊 Parse CSV files exported from TradingView
- 🕒 Convert Unix timestamps to readable datetime format
- 📋 Organize data by categories (OHLC, Signals, Indicators, etc.)
- 🔢 Handle missing data (NaN values) appropriately
- 📈 Format numeric values with customizable precision
- 💾 Export to multiple formats (CSV, JSON)
- 📊 Detailed summary statistics and data analysis

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the example
python src/examples/parse_example.py
```

```python
from src.parsers import TradingViewCSVParser

# Initialize parser
parser = TradingViewCSVParser(decimal_places=4)

# Parse CSV file
df = parser.parse_csv('your_tradingview_export.csv')

# Display summary
print(parser.display_summary())

# Show formatted data
print(parser.display_data(max_rows=10))

# Export formatted data
parser.export_to_csv('formatted_output.csv')
```

## Documentation

See [src/README.md](src/README.md) for complete documentation and API reference.

## LuxAlgo Indicators Supported

The parser automatically recognizes and organizes these LuxAlgo indicator columns:

- **Signals**: Bullish, Bullish+, Bearish, Bearish+, Bullish Exit, Bearish Exit
- **Metrics**: Trend Strength, Take Profit, Stop Loss, Bar Color Value
- **Indicators**: Trend Tracer, Trend Catcher, Smart Trail, Smart Trail Extremity
- **Bands**: RZ R3/R2/R1 Band, Reversal Zones Average, RZ S1/S2/S3 Band
- **Neo**: Neo Lead, Neo Lag
- **Alerts**: Custom Alert Condition Highlighter, Alert Scripting Condition Highlighter
- **LUCID Connector**: Connector data
- **OHLC**: Standard price data with datetime conversion

---
*Backtest LuxAlgo® - Signals & Overlays™*
