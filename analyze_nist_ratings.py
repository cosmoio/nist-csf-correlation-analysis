import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def analyze_nist_ratings(file_path):

    if "data/synthetic_nist_ratings.csv" in file_path:
        print(f"Analyzing *synthetic* NIST ratings from {file_path} ...")
    else:
        print(f"Analyzing NIST ratings from {file_path} ...")

    # 1. Load Data
    # Assumes columns: 'Category', 'Subcategory', 'Manager_1', 'Manager_2', ...
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the path and try again.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while loading the data: {e}")
        return
    
    # Identify manager columns (assuming they are the numeric ones, or explicitly named)
    # Here we assume columns 3 onwards are managers. Adjust as necessary.
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    manager_cols = [c for c in numeric_cols if c not in ['id', 'order']] # filter out non-rating numbers if any
    
    print(f"Managers identified: {manager_cols}")

    # --- LEVEL 1: Subcategory Analysis (Agreement/Variance) ---
    # We cannot correlate a single row, so we calculate variance/std dev
    df['agreement_std'] = df[manager_cols].std(axis=1)
    df['agreement_range'] = df[manager_cols].max(axis=1) - df[manager_cols].min(axis=1)
    
    # To print ALL rows without truncation:
    pd.set_option('display.max_rows', None)

    # Filter for significant disagreement (e.g., std > 1.0)
    # If you want absolutely ALL, just remove the [df['agreement_std'] > 1.0] filter
    high_disagreement = df[df['agreement_std'] > 1.0]

    print(f"\n--- Subcategories with High Disagreement (Std Dev > 1.0) [Count: {len(high_disagreement)}] ---")
    print(high_disagreement.sort_values(by='agreement_std', ascending=False)[['Category', 'Subcategory', 'agreement_std']])

    # --- LEVEL 2: Global Correlation ---
    # Correlation between managers across the ENTIRE dataset
    global_corr = df[manager_cols].corr(method='spearman')
    
    plt.figure(figsize=(6, 6))
    sns.heatmap(global_corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title("Global Inter-Rater Correlation (Spearman)")
    # plt.show() # Deferred to end

    # --- LEVEL 3: Function & Category Analysis ---
    # Generate one figure per FUNCTION, with subplots for each CATEGORY
    
    import math
    
    # Get unique functions
    functions = df['Function'].unique()
    
    for func in functions:
        # Filter data for this function
        func_data = df[df['Function'] == func]
        categories = func_data['Category'].unique()
        
        num_cats = len(categories)
        if num_cats == 0:
            continue
            
        # Determine grid size for subplots
        cols = 3 if num_cats > 1 else 1
        rows = math.ceil(num_cats / cols)
        
        fig, axes = plt.subplots(rows, cols, figsize=(6 * cols, 6 * rows))
        fig.suptitle(f"Inter-Rater Correlation: {func} Function", fontsize=12)
        
        # Flatten axes array for easy iteration if multiple subplots
        if num_cats > 1:
            axes = axes.flatten()
        else:
            axes = [axes]
            
        for i, cat in enumerate(categories):
            ax = axes[i]
            subset = func_data[func_data['Category'] == cat]
            
            if len(subset) > 2:
                cat_corr = subset[manager_cols].corr(method='spearman')
                
                # Calculate average correlation (off-diagonal)
                n = len(cat_corr)
                if n > 1:
                    avg_corr = (cat_corr.sum().sum() - n) / (n**2 - n)
                else:
                    avg_corr = 0
                
                sns.heatmap(cat_corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
                ax.set_title(f"{cat} (Avg Corr: {avg_corr:.2f})")
            else:
                ax.text(0.5, 0.5, "Not enough data", ha='center', va='center')
                ax.set_title(f"{cat}")
        
        # Clean up the figure by hiding any empty subplot slots
        # (e.g., if we have a 2x3 grid but only 5 categories, hide the 6th slot)
        for j in range(i + 1, len(axes)):
            axes[j].axis('off')
            
        # Adjust layout to prevent overlap, leaving top space (0.95) for the main title
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze NIST Ratings')
    parser.add_argument('file_path', nargs='?', default='data/synthetic_nist_ratings.csv', help='Path to the CSV file containing ratings')
    args = parser.parse_args()
    
    analyze_nist_ratings(args.file_path)