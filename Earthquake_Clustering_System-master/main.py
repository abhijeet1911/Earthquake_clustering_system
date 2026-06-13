"""
Complete Earthquake Clustering Analysis - Standalone Script
Performs clustering on earthquake magnitude and depth data
Algorithms: K-Means, Hierarchical, DBSCAN, GMM
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import json
from pathlib import Path

sns.set_theme(style='whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

# ============================================================================
# 1. LOAD AND PREPROCESS DATA
# ============================================================================
print("Loading earthquake data...")
df = pd.read_csv('earthquake_data.csv')
print(f"Dataset shape: {df.shape}")

# Select features for clustering
features = ['magnitude', 'depth', 'latitude', 'longitude']
X = df[features].copy()

# Handle missing values
X = X.dropna()

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"Processed data shape: {X_scaled.shape}")
print(f"Features: {features}")

# ============================================================================
# 2. ELBOW METHOD FOR OPTIMAL K
# ============================================================================
print("\n" + "="*60)
print("ELBOW METHOD FOR OPTIMAL K")
print("="*60)

inertias = []
silhouette_scores_km = []
k_range = range(2, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores_km.append(silhouette_score(X_scaled, kmeans.labels_))
    print(f"k={k}: Inertia={kmeans.inertia_:.3f}, Silhouette={silhouette_scores_km[-1]:.3f}")

optimal_k = 4
print(f"\nOptimal k={optimal_k} (selected based on elbow point)")

# ============================================================================
# 3. TRAIN ALL CLUSTERING ALGORITHMS
# ============================================================================
print("\n" + "="*60)
print("TRAINING CLUSTERING ALGORITHMS")
print("="*60)

# K-Means
kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
kmeans_labels = kmeans_final.fit_predict(X_scaled)
print(f"K-Means trained with k={optimal_k}")

# Hierarchical Clustering
linkage_matrix = linkage(X_scaled, method='ward')
hierarchical_labels = fcluster(linkage_matrix, optimal_k, criterion='maxclust') - 1
print(f"Hierarchical Clustering trained (Ward linkage)")

# DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
dbscan_labels = dbscan.fit_predict(X_scaled)
n_clusters_dbscan = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
n_noise_dbscan = list(dbscan_labels).count(-1)
print(f"DBSCAN trained: {n_clusters_dbscan} clusters, {n_noise_dbscan} noise points")

# Gaussian Mixture Model
gmm = GaussianMixture(n_components=optimal_k, random_state=42)
gmm_labels = gmm.fit_predict(X_scaled)
print(f"GMM trained with {optimal_k} components")

# ============================================================================
# 4. EVALUATION METRICS
# ============================================================================
print("\n" + "="*60)
print("CLUSTERING EVALUATION METRICS")
print("="*60)

algorithms = {
    'K-Means': kmeans_labels,
    'Hierarchical': hierarchical_labels,
    'GMM': gmm_labels
}

metrics_results = []
for algo_name, labels in algorithms.items():
    silhouette = silhouette_score(X_scaled, labels)
    davies_bouldin = davies_bouldin_score(X_scaled, labels)
    calinski_harabasz = calinski_harabasz_score(X_scaled, labels)
    
    metrics_results.append({
        'Algorithm': algo_name,
        'Silhouette': silhouette,
        'Davies-Bouldin': davies_bouldin,
        'Calinski-Harabasz': calinski_harabasz
    })
    
    print(f"\n{algo_name}:")
    print(f"  Silhouette Score: {silhouette:.4f} (range: -1 to 1, higher better)")
    print(f"  Davies-Bouldin Index: {davies_bouldin:.4f} (lower better)")
    print(f"  Calinski-Harabasz Index: {calinski_harabasz:.4f} (higher better)")

if n_clusters_dbscan > 0:
    silhouette_dbscan = silhouette_score(X_scaled, dbscan_labels)
    print(f"\nDBSCAN (eps=0.5, min_samples=5):")
    print(f"  Silhouette Score: {silhouette_dbscan:.4f}")
    print(f"  Clusters: {n_clusters_dbscan}, Noise: {n_noise_dbscan}")

# ============================================================================
# 5. VISUALIZATIONS
# ============================================================================
print("\n" + "="*60)
print("GENERATING VISUALIZATIONS")
print("="*60)

# Elbow and Silhouette plot
fig, axes = plt.subplots(1, 2, figsize=(14, 4))

axes[0].plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
axes[0].axvline(optimal_k, color='red', linestyle='--', linewidth=2, label=f'Optimal k={optimal_k}')
axes[0].set_xlabel('Number of Clusters (k)', fontsize=12)
axes[0].set_ylabel('Inertia', fontsize=12)
axes[0].set_title('K-Means Elbow Method', fontsize=13, fontweight='bold')
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].plot(k_range, silhouette_scores_km, 'go-', linewidth=2, markersize=8)
axes[1].axvline(optimal_k, color='red', linestyle='--', linewidth=2, label=f'Optimal k={optimal_k}')
axes[1].set_xlabel('Number of Clusters (k)', fontsize=12)
axes[1].set_ylabel('Silhouette Score', fontsize=12)
axes[1].set_title('K-Means Silhouette Analysis', fontsize=13, fontweight='bold')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('elbow_silhouette_plot.png', dpi=300, bbox_inches='tight')
print("✓ Saved: elbow_silhouette_plot.png")
plt.close()

# Dendrogram
plt.figure(figsize=(14, 6))
dendrogram(linkage_matrix, no_labels=True, color_threshold=30)
plt.axhline(y=30, color='red', linestyle='--', linewidth=2, label=f'Cut for {optimal_k} clusters')
plt.xlabel('Sample Index', fontsize=12)
plt.ylabel('Distance', fontsize=12)
plt.title('Hierarchical Clustering Dendrogram (Ward Linkage)', fontsize=13, fontweight='bold')
plt.legend()
plt.tight_layout()
plt.savefig('dendrogram.png', dpi=300, bbox_inches='tight')
print("✓ Saved: dendrogram.png")
plt.close()

# Cluster scatter - Magnitude vs Depth
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
titles = ['K-Means', 'Hierarchical', 'DBSCAN', 'GMM']
labels_list = [kmeans_labels, hierarchical_labels, dbscan_labels, gmm_labels]

for idx, (ax, title, labels) in enumerate(zip(axes.flat, titles, labels_list)):
    scatter = ax.scatter(df['magnitude'], df['depth'], c=labels, cmap='viridis', 
                        s=80, alpha=0.6, edgecolors='black', linewidth=0.5)
    ax.set_xlabel('Magnitude (Richter Scale)', fontsize=11)
    ax.set_ylabel('Depth (km)', fontsize=11)
    ax.set_title(f'{title} Clustering', fontsize=12, fontweight='bold')
    ax.grid(alpha=0.3)
    plt.colorbar(scatter, ax=ax, label='Cluster')

plt.tight_layout()
plt.savefig('cluster_scatter_magnitude_depth.png', dpi=300, bbox_inches='tight')
print("✓ Saved: cluster_scatter_magnitude_depth.png")
plt.close()

# Spatial scatter - Latitude vs Longitude
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

for idx, (ax, title, labels) in enumerate(zip(axes.flat, titles, labels_list)):
    scatter = ax.scatter(df['longitude'], df['latitude'], c=labels, cmap='viridis',
                        s=80, alpha=0.6, edgecolors='black', linewidth=0.5)
    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.set_title(f'{title} - Spatial Distribution', fontsize=12, fontweight='bold')
    ax.grid(alpha=0.3)
    plt.colorbar(scatter, ax=ax, label='Cluster')

plt.tight_layout()
plt.savefig('cluster_scatter_spatial.png', dpi=300, bbox_inches='tight')
print("✓ Saved: cluster_scatter_spatial.png")
plt.close()

# ============================================================================
# 6. CLUSTER ANALYSIS
# ============================================================================
print("\n" + "="*60)
print("CLUSTER CHARACTERISTICS (K-MEANS)")
print("="*60)

for cluster_id in range(optimal_k):
    cluster_mask = kmeans_labels == cluster_id
    cluster_data = df[cluster_mask]
    print(f"\nCluster {cluster_id}:")
    print(f"  Size: {cluster_mask.sum()} earthquakes")
    print(f"  Avg Magnitude: {cluster_data['magnitude'].mean():.2f} ± {cluster_data['magnitude'].std():.2f}")
    print(f"  Avg Depth: {cluster_data['depth'].mean():.1f} ± {cluster_data['depth'].std():.1f} km")
    print(f"  Magnitude Range: {cluster_data['magnitude'].min():.2f} - {cluster_data['magnitude'].max():.2f}")
    print(f"  Depth Range: {cluster_data['depth'].min():.1f} - {cluster_data['depth'].max():.1f} km")

# ============================================================================
# 7. SAVE SUMMARY
# ============================================================================
summary = {
    'dataset_size': len(df),
    'num_features': len(features),
    'features': features,
    'optimal_k': optimal_k,
    'kmeans_silhouette': float(silhouette_score(X_scaled, kmeans_labels)),
    'hierarchical_silhouette': float(silhouette_score(X_scaled, hierarchical_labels)),
    'gmm_silhouette': float(silhouette_score(X_scaled, gmm_labels)),
    'kmeans_davies_bouldin': float(davies_bouldin_score(X_scaled, kmeans_labels)),
    'kmeans_calinski_harabasz': float(calinski_harabasz_score(X_scaled, kmeans_labels)),
    'dbscan_clusters': n_clusters_dbscan,
    'dbscan_noise': n_noise_dbscan,
}

with open('clustering_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print("\n✓ Saved: clustering_summary.json")

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
print("\nGenerated Files:")
print("  - elbow_silhouette_plot.png")
print("  - dendrogram.png")
print("  - cluster_scatter_magnitude_depth.png")
print("  - cluster_scatter_spatial.png")
print("  - clustering_summary.json")
