"""
Data formatting utilities for TradingView CSV data.

This module handles formatting and organizing CSV data from TradingView exports,
specifically for LuxAlgo indicators.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path
# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from utils.datetime_utils import format_datetime_column


class DataFormatter:
    """
    Formats and organizes TradingView CSV data for better readability.
    """
    
    # Column categories for organization
    COLUMN_CATEGORIES = {
        'OHLC': ['time', 'open', 'high', 'low', 'close'],
        'LuxAlgo_Connector': ['LUCID Connector'],
        'Signals': ['Bullish', 'Bullish+', 'Bearish', 'Bearish+', 'Bullish Exit', 'Bearish Exit'],
        'Metrics': ['Trend Strength', 'Take Profit', 'Stop Loss', 'Bar Color Value'],
        'Indicators': ['Trend Tracer', 'Trend Catcher', 'Smart Trail', 'Smart Trail Extremity'],
        'Bands': ['RZ R3 Band', 'RZ R2 Band', 'RZ R1 Band', 'Reversal Zones Average', 
                 'RZ S1 Band', 'RZ S2 Band', 'RZ S3 Band'],
        'Neo': ['Neo Lead', 'Neo Lag'],
        'Alerts': ['Custom Alert Condition Highlighter', 'Alert Scripting Condition Highlighter'],
        'Other': ['@valuewhen']
    }
    
    def __init__(self, decimal_places: int = 4):
        """
        Initialize the data formatter.
        
        Args:
            decimal_places: Number of decimal places for numeric formatting
        """
        self.decimal_places = decimal_places
    
    def format_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Format the entire dataframe with proper data types and formatting.
        
        Args:
            df: Raw pandas DataFrame from CSV
            
        Returns:
            Formatted DataFrame
        """
        df_formatted = df.copy()
        
        # Format timestamp column if it exists
        if 'time' in df_formatted.columns:
            df_formatted['datetime'] = format_datetime_column(df_formatted['time'])
            # Move datetime column to front
            cols = ['datetime'] + [col for col in df_formatted.columns if col != 'datetime']
            df_formatted = df_formatted[cols]
        
        # Format numeric columns
        for col in df_formatted.columns:
            if col not in ['time', 'datetime']:
                df_formatted[col] = self._format_numeric_column(df_formatted[col])
        
        return df_formatted
    
    def _format_numeric_column(self, series: pd.Series) -> pd.Series:
        """
        Format a numeric column with proper precision and NaN handling.
        
        Args:
            series: Pandas Series to format
            
        Returns:
            Formatted Series
        """
        # Try to convert to numeric, keeping NaN values
        try:
            numeric_series = pd.to_numeric(series, errors='coerce')
            # Round to specified decimal places, but only if not NaN
            formatted_series = numeric_series.round(self.decimal_places)
            return formatted_series
        except Exception:
            # If conversion fails, return original series
            return series
    
    def organize_by_category(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Organize DataFrame columns by category.
        
        Args:
            df: DataFrame to organize
            
        Returns:
            Dictionary with category names as keys and DataFrames as values
        """
        organized = {}
        used_columns = set()
        
        for category, columns in self.COLUMN_CATEGORIES.items():
            # Find matching columns (case-insensitive)
            available_cols = []
            for col in columns:
                matching_cols = [c for c in df.columns 
                               if c.lower() == col.lower() and c not in used_columns]
                available_cols.extend(matching_cols)
                used_columns.update(matching_cols)
            
            if available_cols:
                # Include datetime if available and this is OHLC category
                if category == 'OHLC' and 'datetime' in df.columns:
                    available_cols = ['datetime'] + available_cols
                
                organized[category] = df[available_cols]
        
        # Add any remaining columns to 'Other' category
        remaining_cols = [col for col in df.columns if col not in used_columns and col != 'datetime']
        if remaining_cols:
            if 'Other' in organized:
                organized['Other'] = pd.concat([organized['Other'], df[remaining_cols]], axis=1)
            else:
                organized['Other'] = df[remaining_cols]
        
        return organized
    
    def format_for_display(self, df: pd.DataFrame, max_rows: Optional[int] = None) -> str:
        """
        Format DataFrame for console display with aligned columns.
        
        Args:
            df: DataFrame to format
            max_rows: Maximum number of rows to display
            
        Returns:
            Formatted string for console output
        """
        if max_rows:
            df = df.head(max_rows)
        
        # Replace NaN with empty string for display
        df_display = df.fillna('')
        
        return df_display.to_string(index=False, max_cols=None)
    
    def get_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary statistics for the dataset.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with summary statistics
        """
        stats = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'date_range': None,
            'missing_data': {},
            'numeric_columns': []
        }
        
        # Date range
        if 'datetime' in df.columns:
            stats['date_range'] = {
                'start': df['datetime'].iloc[0] if len(df) > 0 else None,
                'end': df['datetime'].iloc[-1] if len(df) > 0 else None
            }
        
        # Missing data analysis
        for col in df.columns:
            missing_count = df[col].isna().sum()
            if missing_count > 0:
                stats['missing_data'][col] = {
                    'count': missing_count,
                    'percentage': (missing_count / len(df)) * 100
                }
        
        # Numeric columns identification
        for col in df.columns:
            if col not in ['time', 'datetime']:
                try:
                    pd.to_numeric(df[col], errors='raise')
                    stats['numeric_columns'].append(col)
                except (ValueError, TypeError):
                    pass
        
        return stats