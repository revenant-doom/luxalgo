"""
Main CSV parser for TradingView data exports.

This module provides the primary functionality for parsing and processing
CSV files exported from TradingView, specifically designed for LuxAlgo indicators.
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, Optional, Union, List, Any
from .data_formatter import DataFormatter


class TradingViewCSVParser:
    """
    Parser for TradingView CSV exports with LuxAlgo indicators.
    """
    
    def __init__(self, decimal_places: int = 4):
        """
        Initialize the CSV parser.
        
        Args:
            decimal_places: Number of decimal places for numeric formatting
        """
        self.formatter = DataFormatter(decimal_places)
        self.raw_data = None
        self.formatted_data = None
        self.organized_data = None
    
    def parse_csv(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Parse CSV file from TradingView export.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Formatted pandas DataFrame
            
        Raises:
            FileNotFoundError: If file doesn't exist
            pd.errors.EmptyDataError: If CSV is empty
            Exception: For other parsing errors
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"CSV file not found: {file_path}")
            
            # Read CSV with pandas
            self.raw_data = pd.read_csv(file_path)
            
            if self.raw_data.empty:
                raise pd.errors.EmptyDataError("CSV file is empty")
            
            # Format the data
            self.formatted_data = self.formatter.format_dataframe(self.raw_data)
            
            # Organize by categories
            self.organized_data = self.formatter.organize_by_category(self.formatted_data)
            
            return self.formatted_data
            
        except Exception as e:
            raise Exception(f"Error parsing CSV file: {str(e)}")
    
    def get_formatted_data(self) -> Optional[pd.DataFrame]:
        """
        Get the formatted DataFrame.
        
        Returns:
            Formatted DataFrame or None if not parsed yet
        """
        return self.formatted_data
    
    def get_organized_data(self) -> Optional[Dict[str, pd.DataFrame]]:
        """
        Get data organized by categories.
        
        Returns:
            Dictionary with categorized DataFrames or None if not parsed yet
        """
        return self.organized_data
    
    def display_summary(self) -> str:
        """
        Display a summary of the parsed data.
        
        Returns:
            Formatted summary string
        """
        if self.formatted_data is None:
            return "No data parsed yet. Use parse_csv() first."
        
        stats = self.formatter.get_summary_stats(self.formatted_data)
        
        summary = []
        summary.append("=== TradingView CSV Parser Summary ===")
        summary.append(f"Total rows: {stats['total_rows']}")
        summary.append(f"Total columns: {stats['total_columns']}")
        
        if stats['date_range']:
            summary.append(f"Date range: {stats['date_range']['start']} to {stats['date_range']['end']}")
        
        if stats['missing_data']:
            summary.append("\\nMissing data:")
            for col, info in stats['missing_data'].items():
                summary.append(f"  {col}: {info['count']} rows ({info['percentage']:.1f}%)")
        
        summary.append(f"\\nNumeric columns: {len(stats['numeric_columns'])}")
        
        if self.organized_data:
            summary.append(f"\\nData categories found: {', '.join(self.organized_data.keys())}")
        
        return "\\n".join(summary)
    
    def display_data(self, category: Optional[str] = None, max_rows: int = 10) -> str:
        """
        Display formatted data for console output.
        
        Args:
            category: Specific category to display, or None for all data
            max_rows: Maximum number of rows to display
            
        Returns:
            Formatted string for console display
        """
        if self.formatted_data is None:
            return "No data parsed yet. Use parse_csv() first."
        
        if category and self.organized_data and category in self.organized_data:
            df_to_show = self.organized_data[category]
            title = f"=== {category} Data ==="
        else:
            df_to_show = self.formatted_data
            title = "=== All Data ==="
        
        output = [title]
        output.append(self.formatter.format_for_display(df_to_show, max_rows))
        
        if len(df_to_show) > max_rows:
            output.append(f"\\n... showing first {max_rows} of {len(df_to_show)} rows")
        
        return "\\n".join(output)
    
    def list_categories(self) -> List[str]:
        """
        List available data categories.
        
        Returns:
            List of category names
        """
        if self.organized_data:
            return list(self.organized_data.keys())
        return []
    
    def export_to_csv(self, output_path: Union[str, Path], category: Optional[str] = None) -> None:
        """
        Export formatted data to CSV file.
        
        Args:
            output_path: Path for output CSV file
            category: Specific category to export, or None for all data
        """
        if self.formatted_data is None:
            raise Exception("No data to export. Parse CSV first.")
        
        if category and self.organized_data and category in self.organized_data:
            df_to_export = self.organized_data[category]
        else:
            df_to_export = self.formatted_data
        
        df_to_export.to_csv(output_path, index=False)
    
    def export_to_json(self, output_path: Union[str, Path], category: Optional[str] = None) -> None:
        """
        Export formatted data to JSON file.
        
        Args:
            output_path: Path for output JSON file
            category: Specific category to export, or None for all data
        """
        if self.formatted_data is None:
            raise Exception("No data to export. Parse CSV first.")
        
        if category and self.organized_data and category in self.organized_data:
            df_to_export = self.organized_data[category]
        else:
            df_to_export = self.formatted_data
        
        # Convert DataFrame to JSON with proper handling of NaN values
        json_data = df_to_export.to_dict('records')
        
        with open(output_path, 'w') as f:
            json.dump(json_data, f, indent=2, default=str)
    
    def get_column_info(self) -> Dict[str, Any]:
        """
        Get information about all columns in the dataset.
        
        Returns:
            Dictionary with column information
        """
        if self.formatted_data is None:
            return {}
        
        column_info = {}
        for col in self.formatted_data.columns:
            info = {
                'type': str(self.formatted_data[col].dtype),
                'non_null_count': self.formatted_data[col].count(),
                'null_count': self.formatted_data[col].isna().sum(),
                'unique_count': self.formatted_data[col].nunique()
            }
            
            # Add min/max for numeric columns
            if pd.api.types.is_numeric_dtype(self.formatted_data[col]):
                info['min'] = self.formatted_data[col].min()
                info['max'] = self.formatted_data[col].max()
                info['mean'] = self.formatted_data[col].mean()
            
            column_info[col] = info
        
        return column_info