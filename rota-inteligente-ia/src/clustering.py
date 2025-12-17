import pandas as pd
from sklearn.cluster import KMeans

def load_deliveries(path):
    df = pd.read_csv(path)
    if "priority" not in df.columns:
        df["priority"] = "medium"
    return df

def run_kmeans(df, k, random_state=42):
    coords = df[["x", "y"]].values
    model = KMeans(n_clusters=k, n_init="auto", random_state=random_state)
    df = df.copy()
    df["cluster"] = model.fit_predict(coords)
    return df, model.cluster_centers_, model.inertia_
