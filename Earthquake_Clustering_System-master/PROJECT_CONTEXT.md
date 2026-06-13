# Earthquake Clustering Project - Context for Report Generation

## Domain
- **Topic**: Spatial Database Mining
- **Problem**: Earthquake epicentre clustering by magnitude and depth
- **Learning Type**: Clustering (Unsupervised Learning)

## Dataset
- **File**: earthquake_data.csv
- **Samples**: 500 earthquake records
- **Features**: magnitude, depth, latitude, longitude, true_cluster (for reference)
- **Generated patterns**: 4 natural clusters representing different earthquake types:
  - Shallow Subduction Zone: avg magnitude 5.5, depth 50 km
  - Intermediate Depth: avg magnitude 6.2, depth 150 km
  - Crustal Seismicity: avg magnitude 4.8, depth 15 km
  - Deep Slab: avg magnitude 7.0, depth 400 km

## Clustering Algorithms Implemented
1. **K-Means**: k=4 (selected via Elbow Method)
   - Silhouette Score: ~0.60
   - Davies-Bouldin Index: ~0.75
   - Calinski-Harabasz Index: ~185

2. **Hierarchical Clustering**: Ward linkage, k=4
   - Silhouette Score: ~0.58
   - Davies-Bouldin Index: ~0.78

3. **DBSCAN**: eps=0.5, min_samples=5
   - For comparison; may detect noise points

4. **Gaussian Mixture Model**: 4 components
   - Soft clustering approach
   - Reports log-likelihood and BIC

## Evaluation Metrics Provided
- **Silhouette Score**: Measures how similar objects are within their cluster vs other clusters
- **Davies-Bouldin Index**: Ratio of intra-cluster to inter-cluster distances (lower is better)
- **Calinski-Harabasz Index**: Ratio of between-cluster to within-cluster dispersion (higher is better)
- **Elbow Method**: Used to select optimal k

## Visualizations Generated
1. `elbow_silhouette_plot.png`: Elbow method and silhouette scores
2. `dendrogram.png`: Hierarchical clustering dendrogram
3. `cluster_scatter_magnitude_depth.png`: All 4 algorithms compared on magnitude vs depth
4. `cluster_scatter_spatial.png`: Spatial distribution (latitude vs longitude)

## Preprocessing
- Standardization: StandardScaler applied to all features
- No missing values in dataset
- Final feature vector dimensionality: 4
