import pandas as pd
import sys
import os

def enrich_flight_data(file_path):
    try:
        # Load the dataset
        df = pd.read_csv(file_path)
        print(f"[INFO] Loaded dataset with {len(df)} rows.")

        # Convert to datetime
        df['departure_date'] = pd.to_datetime(df['departure_date'], errors='coerce')
        df['search_date'] = pd.to_datetime(df['search_date'], errors='coerce')

        # Drop rows with invalid dates
        df = df.dropna(subset=['departure_date', 'search_date'])

        # Derived columns
        df['days_before_departure'] = (df['departure_date'] - df['search_date']).dt.days
        df['day_of_week'] = df['departure_date'].dt.day_name()
        df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday'])
        df['route'] = df['origin'] + '-' + df['destination']
        df['price_bucket'] = pd.cut(
            df['price'],
            bins=[0, 200, 400, 600, 10000],
            labels=['<$200', '$200–400', '$400–600', '>$600']
        )

        # Optional: add season from departure month
        month_to_season = {
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Fall', 10: 'Fall', 11: 'Fall'
        }
        df['season'] = df['departure_date'].dt.month.map(month_to_season)

        # Save enriched file
        base, ext = os.path.splitext(file_path)
        out_file = base + '_enriched.csv'
        df.to_csv(out_file, index=False)

        print(f"[SUCCESS] Enriched dataset saved to: {out_file}")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python enrich_flight_data.py <flight_data.csv>")
    else:
        enrich_flight_data(sys.argv[1])
