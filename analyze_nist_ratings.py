import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def analyze_nist_ratings(file_path):
    # 1. Load Data
    # Assumes columns: 'Category', 'Subcategory', 'Manager_1', 'Manager_2', ...
    df = pd.read_csv(file_path)
    
    # Identify manager columns (assuming they are the numeric ones, or explicitly named)
    # Here we assume columns 3 onwards are managers. Adjust as necessary.
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    manager_cols = [c for c in numeric_cols if c not in ['id', 'order']] # filter out non-rating numbers if any
    
    print(f"Managers identified: {manager_cols}")

    # --- LEVEL 1: Subcategory Analysis (Agreement/Variance) ---
    # We cannot correlate a single row, so we calculate variance/std dev
    df['agreement_std'] = df[manager_cols].std(axis=1)
    df['agreement_range'] = df[manager_cols].max(axis=1) - df[manager_cols].min(axis=1)
    
    print("\n--- Top 5 Subcategories with Highest Disagreement (Std Dev) ---")
    print(df.sort_values(by='agreement_std', ascending=False)[['Category', 'Subcategory', 'agreement_std']].head(5))

    # --- LEVEL 2: Global Correlation ---
    # Correlation between managers across the ENTIRE dataset
    global_corr = df[manager_cols].corr(method='spearman')
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(global_corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title("Global Inter-Rater Correlation (Spearman)")
    plt.show()

    # --- LEVEL 3: Category-Specific Correlation ---
    # Correlation between managers per Category (e.g., Identify, Protect)
    categories = df['Category'].unique()
    
    for cat in categories:
        subset = df[df['Category'] == cat]
        if len(subset) > 2: # Need at least 2 data points to correlate
            cat_corr = subset[manager_cols].corr(method='spearman')
            
            # We can print the average correlation for this category to summarize
            # (Excluding the diagonal 1.0s)
            avg_corr = (cat_corr.sum().sum() - len(cat_corr)) / (len(cat_corr)**2 - len(cat_corr))
            
            print(f"\nCategory: {cat} (n={len(subset)})")
            print(f"Average Inter-Manager Correlation: {avg_corr:.3f}")
            # Optional: Plot heatmap for each category
            # sns.heatmap(cat_corr, ...) 
        else:
            print(f"\nCategory: {cat} - Not enough data points for correlation.")

if __name__ == "__main__":
    # Example
    analyze_nist_ratings('data/synthetic_nist_ratings.csv')