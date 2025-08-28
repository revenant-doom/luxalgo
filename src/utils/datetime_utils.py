"""
Datetime utilities for TradingView CSV parser.

This module provides utilities for converting Unix timestamps to readable datetime formats.
"""

from datetime import datetime, timezone
from typing import Union, Optional


def unix_to_datetime(timestamp: Union[int, float, str], tz: Optional[timezone] = None) -> str:
    """
    Convert Unix timestamp to readable datetime string.
    
    Args:
        timestamp: Unix timestamp (seconds since epoch)
        tz: Timezone for conversion (default: UTC)
        
    Returns:
        Formatted datetime string in YYYY-MM-DD HH:MM:SS format
        
    Example:
        >>> unix_to_datetime(1754179200)
        '2025-08-12 00:00:00'
    """
    if tz is None:
        tz = timezone.utc
        
    try:
        # Handle string timestamps
        if isinstance(timestamp, str):
            timestamp = float(timestamp)
            
        # Convert to datetime
        dt = datetime.fromtimestamp(timestamp, tz=tz)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
        
    except (ValueError, TypeError, OSError) as e:
        return f"Invalid timestamp: {timestamp}"


def format_datetime_column(series, tz: Optional[timezone] = None) -> list:
    """
    Format a pandas Series of Unix timestamps to readable datetime strings.
    
    Args:
        series: Pandas Series containing Unix timestamps
        tz: Timezone for conversion (default: UTC)
        
    Returns:
        List of formatted datetime strings
    """
    return [unix_to_datetime(ts, tz) for ts in series]


def is_valid_timestamp(timestamp: Union[int, float, str]) -> bool:
    """
    Check if a timestamp is valid.
    
    Args:
        timestamp: Unix timestamp to validate
        
    Returns:
        True if timestamp is valid, False otherwise
    """
    try:
        if isinstance(timestamp, str):
            timestamp = float(timestamp)
        datetime.fromtimestamp(timestamp)
        return True
    except (ValueError, TypeError, OSError):
        return False