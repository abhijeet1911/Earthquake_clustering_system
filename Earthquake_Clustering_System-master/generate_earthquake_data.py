"""
Generate synthetic earthquake dataset with realistic patterns.
Magnitude: 3.0-8.0 (Richter scale)
Depth: 5-700 km (various types: shallow, intermediate, deep)
Location: latitude/longitude pairs
"""

import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

# Generate earthquake data with realistic clustering patterns
n_samples = 500

# Create 4 clusters with different characteristics
cluster_1 = {
    'magnitude': np.random.normal(5.5, 0.6, 80),
    'depth': np.random.normal(50, 15, 80),
    'latitude': np.random.normal(35.5, 2.0, 80),
    'longitude': np.random.normal(139.0, 2.0, 80),
    'label': 'Shallow Subduction Zone'
}

cluster_2 = {
    'magnitude': np.random.normal(6.2, 0.8, 120),
    'depth': np.random.normal(150, 40, 120),
    'latitude': np.random.normal(37.0, 3.0, 120),
    'longitude': np.random.normal(142.0, 3.0, 120),
    'label': 'Intermediate Depth'
}

cluster_3 = {
    'magnitude': np.random.normal(4.8, 0.5, 150),
    'depth': np.random.normal(15, 8, 150),
    'latitude': np.random.normal(32.0, 1.5, 150),
    'longitude': np.random.normal(135.0, 1.5, 150),
    'label': 'Crustal Seismicity'
}

cluster_4 = {
    'magnitude': np.random.normal(7.0, 0.9, 150),
    'depth': np.random.normal(400, 100, 150),
    'latitude': np.random.normal(40.0, 5.0, 150),
    'longitude': np.random.normal(145.0, 5.0, 150),
    'label': 'Deep Slab'
}

# Combine clusters
data = {}
for key in ['magnitude', 'depth', 'latitude', 'longitude']:
    data[key] = np.concatenate([
        cluster_1[key],
        cluster_2[key],
        cluster_3[key],
        cluster_4[key]
    ])

data['true_cluster'] = np.concatenate([
    np.full(80, 'Shallow Subduction Zone'),
    np.full(120, 'Intermediate Depth'),
    np.full(150, 'Crustal Seismicity'),
    np.full(150, 'Deep Slab')
])

# Enforce realistic ranges
data['magnitude'] = np.clip(data['magnitude'], 3.0, 8.0)
data['depth'] = np.clip(data['depth'], 5, 700)
data['latitude'] = np.clip(data['latitude'], 20, 50)
data['longitude'] = np.clip(data['longitude'], 130, 150)

df = pd.DataFrame(data)

# Add earthquake ID
df.insert(0, 'earthquake_id', range(1, len(df) + 1))

# Save to CSV
output_path = Path(__file__).parent / 'earthquake_data.csv'
df.to_csv(output_path, index=False)

print(f"Generated {len(df)} earthquake records")
print(f"Saved to: {output_path}")
print(f"\nData summary:\n{df.describe()}")
print(f"\nTrue cluster distribution:\n{df['true_cluster'].value_counts()}")
