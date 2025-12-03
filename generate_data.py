import pandas as pd
import numpy as np

def generate_sample_data():
    """Generate synthetic linear regression data"""
    np.random.seed(42)
    
    # Generate 1000 samples with 3 features
    n_samples = 1000
    n_features = 3
    
    # Generate feature data
    X = np.random.randn(n_samples, n_features)
    
    # Create a linear relationship: y = 2*x1 + 3*x2 - 1.5*x3 + noise
    true_coefficients = [2.0, 3.0, -1.5]
    y = np.dot(X, true_coefficients) + np.random.randn(n_samples) * 0.1
    
    # Create DataFrame
    feature_names = [f'feature_{i+1}' for i in range(n_features)]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    # Save to CSV
    df.to_csv('data.csv', index=False)
    print(f"✅ Generated {n_samples} samples with {n_features} features")
    print(f"📁 Data saved to 'data.csv'")
    print(f"📊 Data shape: {df.shape}")
    print(f"🎯 True coefficients: {true_coefficients}")
    print("\nFirst 5 rows:")
    print(df.head())

if __name__ == "__main__":
    generate_sample_data()