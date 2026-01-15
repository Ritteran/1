"""
Data Processor module for NSE/BSE Stock Market Scraper
Provides data analysis, filtering, and processing capabilities
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import json
from pathlib import Path
import config


class DataProcessor:
    """Process and analyze scraped stock market data"""

    def __init__(self):
        self.data_dir = config.DATA_DIR

    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load data from various file formats

        Args:
            file_path: Path to data file (JSON, CSV, or Excel)

        Returns:
            DataFrame with loaded data
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return pd.DataFrame(data)
                elif isinstance(data, dict):
                    return pd.DataFrame([data])

        elif file_path.suffix == '.csv':
            return pd.read_csv(file_path)

        elif file_path.suffix in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)

        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

    def filter_by_date(self, df: pd.DataFrame, date_column: str,
                      start_date: Optional[str] = None,
                      end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Filter DataFrame by date range

        Args:
            df: Input DataFrame
            date_column: Name of date column
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            Filtered DataFrame
        """
        if date_column not in df.columns:
            return df

        # Convert to datetime
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')

        if start_date:
            start_date = pd.to_datetime(start_date)
            df = df[df[date_column] >= start_date]

        if end_date:
            end_date = pd.to_datetime(end_date)
            df = df[df[date_column] <= end_date]

        return df

    def filter_by_keywords(self, df: pd.DataFrame, column: str,
                          keywords: List[str], case_sensitive: bool = False) -> pd.DataFrame:
        """
        Filter DataFrame by keywords in a specific column

        Args:
            df: Input DataFrame
            column: Column to search
            keywords: List of keywords to search for
            case_sensitive: Whether search is case sensitive

        Returns:
            Filtered DataFrame
        """
        if column not in df.columns or not keywords:
            return df

        if case_sensitive:
            mask = df[column].str.contains('|'.join(keywords), na=False, regex=True)
        else:
            mask = df[column].str.contains('|'.join(keywords), na=False, case=False, regex=True)

        return df[mask]

    def filter_by_company(self, df: pd.DataFrame, companies: List[str]) -> pd.DataFrame:
        """
        Filter data by company names or symbols

        Args:
            df: Input DataFrame
            companies: List of company names or symbols

        Returns:
            Filtered DataFrame
        """
        # Try different possible column names
        company_columns = ['company', 'Company', 'symbol', 'Symbol', 'SYMBOL']

        for col in company_columns:
            if col in df.columns:
                mask = df[col].str.contains('|'.join(companies), na=False, case=False)
                return df[mask]

        return df

    def search_data(self, df: pd.DataFrame, search_term: str,
                   columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Search across multiple columns for a term

        Args:
            df: Input DataFrame
            search_term: Term to search for
            columns: Specific columns to search (None = all text columns)

        Returns:
            DataFrame with matching rows
        """
        if not search_term:
            return df

        if columns is None:
            # Search all object (text) columns
            columns = df.select_dtypes(include=['object']).columns.tolist()

        mask = pd.Series([False] * len(df))
        for col in columns:
            if col in df.columns:
                mask |= df[col].astype(str).str.contains(search_term, case=False, na=False)

        return df[mask]

    def get_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate summary statistics for the dataset

        Args:
            df: Input DataFrame

        Returns:
            Dictionary with summary statistics
        """
        stats = {
            'total_records': len(df),
            'columns': list(df.columns),
            'date_range': {},
            'company_count': 0,
            'category_breakdown': {}
        }

        # Find date column
        date_columns = [col for col in df.columns if 'date' in col.lower()]
        if date_columns:
            date_col = date_columns[0]
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            stats['date_range'] = {
                'start': df[date_col].min().strftime('%Y-%m-%d') if pd.notna(df[date_col].min()) else None,
                'end': df[date_col].max().strftime('%Y-%m-%d') if pd.notna(df[date_col].max()) else None
            }

        # Company count
        company_columns = ['company', 'Company', 'symbol', 'Symbol']
        for col in company_columns:
            if col in df.columns:
                stats['company_count'] = df[col].nunique()
                break

        # Category breakdown
        category_columns = ['category', 'Category', 'purpose', 'Purpose', 'subject', 'Subject']
        for col in category_columns:
            if col in df.columns:
                stats['category_breakdown'] = df[col].value_counts().head(10).to_dict()
                break

        return stats

    def compare_exchanges(self, nse_df: pd.DataFrame, bse_df: pd.DataFrame,
                         comparison_column: str = 'company') -> Dict[str, Any]:
        """
        Compare data between NSE and BSE

        Args:
            nse_df: NSE DataFrame
            bse_df: BSE DataFrame
            comparison_column: Column to compare on

        Returns:
            Dictionary with comparison results
        """
        comparison = {
            'nse_only_count': 0,
            'bse_only_count': 0,
            'common_count': 0,
            'nse_total': len(nse_df),
            'bse_total': len(bse_df),
            'nse_only': [],
            'bse_only': [],
            'common': []
        }

        if comparison_column in nse_df.columns and comparison_column in bse_df.columns:
            nse_set = set(nse_df[comparison_column].dropna().unique())
            bse_set = set(bse_df[comparison_column].dropna().unique())

            comparison['nse_only'] = list(nse_set - bse_set)
            comparison['bse_only'] = list(bse_set - nse_set)
            comparison['common'] = list(nse_set & bse_set)

            comparison['nse_only_count'] = len(comparison['nse_only'])
            comparison['bse_only_count'] = len(comparison['bse_only'])
            comparison['common_count'] = len(comparison['common'])

        return comparison

    def aggregate_by_date(self, df: pd.DataFrame, date_column: str,
                         agg_column: str, freq: str = 'D') -> pd.DataFrame:
        """
        Aggregate data by date

        Args:
            df: Input DataFrame
            date_column: Date column name
            agg_column: Column to aggregate
            freq: Frequency ('D'=daily, 'W'=weekly, 'M'=monthly)

        Returns:
            Aggregated DataFrame
        """
        if date_column not in df.columns:
            return df

        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        df = df.dropna(subset=[date_column])

        if agg_column not in df.columns:
            # Just count records
            result = df.set_index(date_column).resample(freq).size()
            return result.reset_index(name='count')
        else:
            result = df.set_index(date_column).resample(freq)[agg_column].count()
            return result.reset_index()

    def detect_trends(self, df: pd.DataFrame, date_column: str) -> Dict[str, Any]:
        """
        Detect trends in the data

        Args:
            df: Input DataFrame
            date_column: Date column name

        Returns:
            Dictionary with trend information
        """
        trends = {
            'daily_activity': {},
            'peak_days': [],
            'quiet_days': [],
            'overall_trend': 'stable'
        }

        if date_column not in df.columns:
            return trends

        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        df = df.dropna(subset=[date_column])

        # Daily activity
        daily_counts = df.groupby(df[date_column].dt.date).size()
        trends['daily_activity'] = daily_counts.to_dict()

        if len(daily_counts) > 0:
            # Peak days (top 5)
            trends['peak_days'] = daily_counts.nlargest(5).to_dict()

            # Quiet days (bottom 5)
            trends['quiet_days'] = daily_counts.nsmallest(5).to_dict()

            # Overall trend
            if len(daily_counts) >= 7:
                first_week = daily_counts.iloc[:7].mean()
                last_week = daily_counts.iloc[-7:].mean()

                if last_week > first_week * 1.2:
                    trends['overall_trend'] = 'increasing'
                elif last_week < first_week * 0.8:
                    trends['overall_trend'] = 'decreasing'

        return trends

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize data

        Args:
            df: Input DataFrame

        Returns:
            Cleaned DataFrame
        """
        # Remove duplicates
        df = df.drop_duplicates()

        # Strip whitespace from string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()

        # Remove empty rows
        df = df.dropna(how='all')

        # Standardize date formats
        for col in df.columns:
            if 'date' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')

        return df

    def export_processed_data(self, df: pd.DataFrame, filename: str,
                             format: str = 'csv') -> str:
        """
        Export processed data to file

        Args:
            df: DataFrame to export
            filename: Output filename
            format: Output format ('csv', 'json', 'excel')

        Returns:
            Path to exported file
        """
        output_path = self.data_dir / filename

        if format == 'csv':
            df.to_csv(output_path, index=False)
        elif format == 'json':
            df.to_json(output_path, orient='records', indent=2)
        elif format == 'excel':
            df.to_excel(output_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")

        return str(output_path)

    def merge_datasets(self, datasets: List[pd.DataFrame],
                      how: str = 'outer') -> pd.DataFrame:
        """
        Merge multiple datasets

        Args:
            datasets: List of DataFrames to merge
            how: How to merge ('inner', 'outer', 'left', 'right')

        Returns:
            Merged DataFrame
        """
        if not datasets:
            return pd.DataFrame()

        result = datasets[0]
        for df in datasets[1:]:
            # Find common columns
            common_cols = list(set(result.columns) & set(df.columns))
            if common_cols:
                result = pd.merge(result, df, on=common_cols, how=how)
            else:
                result = pd.concat([result, df], axis=0, ignore_index=True)

        return result


if __name__ == "__main__":
    # Example usage
    processor = DataProcessor()

    # Load sample data
    try:
        data_files = list(config.DATA_DIR.glob('*.json'))
        if data_files:
            df = processor.load_data(data_files[0])
            print(f"Loaded {len(df)} records")

            # Get summary stats
            stats = processor.get_summary_stats(df)
            print(f"Summary: {json.dumps(stats, indent=2)}")

            # Clean data
            df_clean = processor.clean_data(df)
            print(f"Cleaned data: {len(df_clean)} records")
    except Exception as e:
        print(f"Example error: {e}")
