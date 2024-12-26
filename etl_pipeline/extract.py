import requests
import pandas as pd
import logging
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
import os
from io import StringIO
from datetime import datetime
from dataclasses import dataclass
from tqdm import tqdm
import sys

@dataclass
class ExtractionMetrics:
    start_time: datetime
    end_time: Optional[datetime] = None
    total_rows: int = 0
    total_batches: int = 0
    failed_attempts: int = 0
    
    def get_summary(self) -> Dict:
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time else 0
        return {
            "Start Time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "End Time": self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else "In Progress",
            "Total Rows": f"{self.total_rows:,}",
            "Total Batches": self.total_batches,
            "Failed Attempts": self.failed_attempts,
            "Duration (seconds)": f"{duration:.2f}",
            "Rows/Second": f"{(self.total_rows / duration if duration > 0 else 0):.2f}"
        }

class CDCDataExtractor:
    def __init__(
        self, 
        api_url: str, 
        batch_size: int = 1000,
        retry_attempts: int = 3,
        verbose: bool = True
    ):
        self.api_url = api_url
        self.batch_size = batch_size
        self.retry_attempts = retry_attempts
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
        self.metrics = ExtractionMetrics(start_time=datetime.now())
        
    def _print_status(self, message: str):
        """Print status messages if verbose mode is on."""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
            sys.stdout.flush()

    def _fetch_batch(self, offset: int) -> pd.DataFrame:
        attempts = 0
        while attempts < self.retry_attempts:
            try:
                params = {
                    "$limit": self.batch_size, 
                    "$offset": offset,
                    "$order": ":id"
                }
                
                self._print_status(f"Fetching batch at offset {offset:,}")
                
                response = requests.get(
                    self.api_url, 
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                
                df = pd.read_csv(StringIO(response.text))
                self.metrics.total_batches += 1
                
                if self.verbose:
                    self._print_status(f"Retrieved {len(df):,} rows")
                
                return df
                
            except Exception as e:
                attempts += 1
                self.metrics.failed_attempts += 1
                self._print_status(f"Attempt {attempts} failed: {str(e)}")
                if attempts == self.retry_attempts:
                    raise

    def extract(self) -> pd.DataFrame:
        offset = 0
        all_data: List[pd.DataFrame] = []
        
        try:
            self._print_status("Starting data extraction...")
            
            while True:
                batch = self._fetch_batch(offset)
                
                if batch.empty:
                    self._print_status("No more data to fetch")
                    break
                
                self.metrics.total_rows += len(batch)
                all_data.append(batch)
                
                self._print_status(
                    f"Progress: {self.metrics.total_rows:,} total rows, "
                    f"{self.metrics.total_batches} batches"
                )
                
                offset += self.batch_size
            
            self._print_status("Combining all batches...")
            final_df = pd.concat(all_data, ignore_index=True)
            
            self.metrics.end_time = datetime.now()
            self._print_status("\nExtraction Summary:")
            for key, value in self.metrics.get_summary().items():
                self._print_status(f"{key}: {value}")
            
            return final_df
            
        except Exception as e:
            self.metrics.end_time = datetime.now()
            self._print_status(f"Extraction failed: {str(e)}")
            raise

def save_dataframe(df: pd.DataFrame, output_dir: str, verbose: bool = True) -> Tuple[str, Optional[str]]:
    """Save DataFrame to CSV and optionally to Parquet if dependencies are available."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(output_dir, f"cdc_data_{timestamp}.csv")
    parquet_path = os.path.join(output_dir, f"cdc_data_{timestamp}.parquet")
    
    if verbose:
        print("\nSaving files...")
    
    # Always save CSV
    df.to_csv(csv_path, index=False)
    if verbose:
        print(f"- CSV saved: {csv_path}")
    
    # Try to save Parquet if possible
    try:
        df.to_parquet(parquet_path, compression='snappy')
        if verbose:
            print(f"- Parquet saved: {parquet_path}")
        return csv_path, parquet_path
    except ImportError:
        if verbose:
            print("\nWarning: Parquet file could not be saved.")
            print("To save in Parquet format, install either pyarrow or fastparquet:")
            print("pip install pyarrow")
            print("-- or --")
            print("pip install fastparquet")
        return csv_path, None

def extract_cdc_data(output_dir: str, verbose: bool = True) -> Tuple[str, Optional[str]]:
    """Main extraction function with enhanced error handling."""
    load_dotenv()
    
    api_url = os.getenv("CDC_API_URL", "https://data.cdc.gov/resource/swc5-untb.csv")
    batch_size = int(os.getenv("BATCH_SIZE", 1000))
    
    try:
        extractor = CDCDataExtractor(
            api_url=api_url, 
            batch_size=batch_size,
            retry_attempts=3,
            verbose=verbose
        )
        
        df = extractor.extract()
        
        if verbose:
            print("\nDataset Information:")
            print(f"Shape: {df.shape}")
            print("\nColumn Names:")
            for col in df.columns:
                print(f"- {col}")
            print("\nData Types:")
            print(df.dtypes)
            print("\nSample Data:")
            print(df.head())
        
        return save_dataframe(df, output_dir, verbose)
        
    except Exception as e:
        logging.error(f"Extraction failed: {str(e)}")
        raise

def get_absolute_project_paths():
    """Get and verify project paths."""
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get project root (parent of script directory)
    project_root = os.path.dirname(script_dir)
    
    # Define data and log directories using absolute paths
    data_dir = os.path.join(project_root, "data", "raw")
    log_dir = os.path.join(project_root, "logs")
    
    # Create directories if they don't exist
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    
    return {
        'project_root': project_root,
        'data_dir': data_dir,
        'log_dir': log_dir
    }

if __name__ == "__main__":
    # Get absolute paths
    paths = get_absolute_project_paths()
    
    print("Project Directories:")
    print(f"Project Root: {paths['project_root']}")
    print(f"Data Directory: {paths['data_dir']}")
    print(f"Log Directory: {paths['log_dir']}")
    print("-" * 50)
    
    # Configure logging with absolute path
    log_file = os.path.join(paths['log_dir'], 'etl_logs.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    try:
        csv_path, parquet_path = extract_cdc_data(paths['data_dir'], verbose=True)
        print("\nPipeline completed successfully!")
        
        # Verify and display file existence
        if csv_path and os.path.exists(csv_path):
            print(f"\nCSV file exists at:\n{csv_path}")
            print(f"File size: {os.path.getsize(csv_path):,} bytes")
        else:
            print("Warning: CSV file was not created or is missing")
            
        if parquet_path:
            if os.path.exists(parquet_path):
                print(f"\nParquet file exists at:\n{parquet_path}")
                print(f"File size: {os.path.getsize(parquet_path):,} bytes")
            else:
                print("Warning: Parquet file was not created or is missing")
                
    except Exception as e:
        print(f"\nPipeline failed: {str(e)}")
        raise