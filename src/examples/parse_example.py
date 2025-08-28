#!/usr/bin/env python3
"""
Example usage of the TradingView CSV Parser.

This script demonstrates how to use the parser to process CSV data
exported from TradingView with LuxAlgo indicators.
"""

import sys
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir.parent
sys.path.insert(0, str(src_dir))

from parsers import TradingViewCSVParser


def main():
    """
    Demonstrate the TradingView CSV parser functionality.
    """
    print("=== TradingView CSV Parser Example ===\\n")
    
    # Initialize the parser
    parser = TradingViewCSVParser(decimal_places=4)
    
    # Path to sample data
    sample_file = current_dir / "sample_data.csv"
    
    try:
        # Parse the CSV file
        print(f"Parsing CSV file: {sample_file}")
        df = parser.parse_csv(sample_file)
        print("✓ CSV parsed successfully!\\n")
        
        # Display summary
        print(parser.display_summary())
        print("\\n" + "="*60 + "\\n")
        
        # Display all data (first 5 rows)
        print(parser.display_data(max_rows=5))
        print("\\n" + "="*60 + "\\n")
        
        # Display data by categories
        categories = parser.list_categories()
        print(f"Available categories: {', '.join(categories)}\\n")
        
        for category in categories:
            print(parser.display_data(category=category, max_rows=3))
            print("\\n" + "-"*40 + "\\n")
        
        # Get column information
        print("=== Column Information ===")
        column_info = parser.get_column_info()
        for col, info in list(column_info.items())[:5]:  # Show first 5 columns
            print(f"\\n{col}:")
            print(f"  Type: {info['type']}")
            print(f"  Non-null: {info['non_null_count']}")
            print(f"  Null: {info['null_count']}")
            if 'min' in info:
                print(f"  Range: {info['min']:.4f} to {info['max']:.4f}")
                print(f"  Mean: {info['mean']:.4f}")
        
        # Export examples
        output_dir = current_dir / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Export formatted CSV
        csv_output = output_dir / "formatted_data.csv"
        parser.export_to_csv(csv_output)
        print(f"\\n✓ Formatted data exported to: {csv_output}")
        
        # Export OHLC data only
        if 'OHLC' in categories:
            ohlc_output = output_dir / "ohlc_data.csv"
            parser.export_to_csv(ohlc_output, category='OHLC')
            print(f"✓ OHLC data exported to: {ohlc_output}")
        
        # Export to JSON
        json_output = output_dir / "formatted_data.json"
        parser.export_to_json(json_output)
        print(f"✓ Data exported to JSON: {json_output}")
        
        print("\\n=== Example completed successfully! ===")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())