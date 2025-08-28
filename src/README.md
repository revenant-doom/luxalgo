# TradingView CSV Parser

A Python package for parsing and formatting CSV data exported from TradingView, specifically designed for LuxAlgo indicators.

## Features

- ✅ Parse CSV files exported from TradingView
- ✅ Convert Unix timestamps to readable datetime format (YYYY-MM-DD HH:MM:SS)
- ✅ Organize data by categories (OHLC, Signals, Indicators, etc.)
- ✅ Handle missing data (NaN values) appropriately
- ✅ Format numeric values with customizable precision
- ✅ Export to multiple formats (CSV, JSON)
- ✅ Detailed summary statistics and data analysis
- ✅ Easy-to-use API with comprehensive error handling

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

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
parser.export_to_json('formatted_output.json')
```

## Data Categories

The parser automatically organizes columns into the following categories:

- **OHLC**: time, open, high, low, close, datetime
- **LuxAlgo_Connector**: LUCID Connector
- **Signals**: Bullish, Bullish+, Bearish, Bearish+, Bullish Exit, Bearish Exit
- **Metrics**: Trend Strength, Take Profit, Stop Loss, Bar Color Value
- **Indicators**: Trend Tracer, Trend Catcher, Smart Trail, Smart Trail Extremity
- **Bands**: RZ R3/R2/R1 Band, Reversal Zones Average, RZ S1/S2/S3 Band
- **Neo**: Neo Lead, Neo Lag
- **Alerts**: Custom Alert Condition Highlighter, Alert Scripting Condition Highlighter
- **Other**: @valuewhen and any unrecognized columns

## Example Usage

See `src/examples/parse_example.py` for a complete example that demonstrates all features.

Run the example:

```bash
python src/examples/parse_example.py
```

## Project Structure

```
src/
├── parsers/
│   ├── __init__.py
│   ├── csv_parser.py          # Main CSV parser
│   └── data_formatter.py      # Data formatting utilities
├── utils/
│   ├── __init__.py
│   └── datetime_utils.py      # DateTime conversion utilities
└── examples/
    ├── sample_data.csv        # Sample TradingView export data
    ├── parse_example.py       # Usage example
    └── output/                # Generated output files
```

## API Reference

### TradingViewCSVParser

Main parser class for processing TradingView CSV exports.

#### Methods

- `parse_csv(file_path)` - Parse CSV file and return formatted DataFrame
- `display_summary()` - Show data summary with statistics
- `display_data(category=None, max_rows=10)` - Display formatted data
- `list_categories()` - List available data categories
- `export_to_csv(output_path, category=None)` - Export to CSV format
- `export_to_json(output_path, category=None)` - Export to JSON format
- `get_column_info()` - Get detailed column information

### Utilities

#### datetime_utils

- `unix_to_datetime(timestamp)` - Convert Unix timestamp to datetime string
- `format_datetime_column(series)` - Format pandas Series of timestamps
- `is_valid_timestamp(timestamp)` - Validate timestamp

## Requirements

- Python 3.8+
- pandas >= 2.0.0

## Error Handling

The parser includes robust error handling for:
- Missing or invalid files
- Empty CSV files
- Invalid timestamps
- Malformed data
- Missing columns

All errors provide clear, actionable error messages.