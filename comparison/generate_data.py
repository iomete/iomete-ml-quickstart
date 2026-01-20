import pandas as pd
import numpy as np

def generate_large_csv(filename="test_data", rows=10_000_000):
    print(f"Generating {rows} rows of data...")
    
    # Generate random features and a response variable with a linear relationship
    # x is the feature, y is the response (y = 2x + 3 + noise)
    x1 = np.random.uniform(0, 100, size=rows)
    x2 = np.random.uniform(0, 100, size=rows)
    x3 = np.random.uniform(0, 100, size=rows)
    noise = np.random.normal(0, 30, size=rows)
    y = 2 * x1 + 3*x2**2 - np.sqrt(x3) + noise
    
    df = pd.DataFrame({
        'feature_col1': x1,
        'feature_col2': x2,
        'feature_col3': x3,
        'target_col': y
    })
    
    print(f"Saving to {filename} (this may take a minute)...")
    filename += f'_{rows}.csv'
    df.to_csv(filename, index=False)
    print("Done! File created.")

if __name__ == "__main__":
    generate_large_csv()