"""
LuxAlgo TradingView CSV Parser

A Python package for parsing and formatting CSV data exported from TradingView,
specifically designed for LuxAlgo indicators.

This package provides:
- CSV parsing with automatic data type detection
- Unix timestamp conversion to readable datetime format
- Data organization by categories (OHLC, Signals, Indicators, etc.)
- Export capabilities (CSV, JSON)
- Summary statistics and data analysis

Example usage:
    from src.parsers import TradingViewCSVParser
    
    parser = TradingViewCSVParser()
    df = parser.parse_csv('tradingview_export.csv')
    print(parser.display_summary())
"""

__version__ = "1.0.0"
__author__ = "LuxAlgo Team"
__description__ = "TradingView CSV Parser for LuxAlgo indicators"