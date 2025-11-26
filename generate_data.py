import pandas as pd
import numpy as np

def generate_synthetic_nist_data(filename='data/synthetic_nist_ratings.csv'):
    # NIST CSF 2.0 Structure (Functions and their Category Codes with Subcategory Counts)
    # Counts are approximations for demonstration or based on standard CSF 2.0
    structure = {
        'GOVERN': {
            'GV.OC': 5, 'GV.RM': 7, 'GV.RR': 4, 'GV.PO': 2, 'GV.OV': 3, 'GV.SC': 10
        },
        'IDENTIFY': {
            'ID.AM': 6, 'ID.RA': 7, 'ID.IM': 2
        },
        'PROTECT': {
            'PR.AA': 6, 'PR.AT': 5, 'PR.DS': 11, 'PR.PS': 6, 'PR.IR': 5
        },
        'DETECT': {
            'DE.CM': 3, 'DE.AE': 2
        },
        'RESPOND': {
            'RS.MA': 5, 'RS.AN': 5, 'RS.CO': 3, 'RS.MI': 2
        },
        'RECOVER': {
            'RC.RP': 1, 'RC.CO': 3
        }
    }

    data = []
    
    # Generate subcategories for each Category
    np.random.seed(42) # Fixed seed for reproducibility
    
    for function, categories in structure.items():
        for cat, num_subcats in categories.items():
            # num_subcats is now fixed per category
            
            for i in range(1, num_subcats + 1):
                subcategory_code = f"{cat}-{i:02d}" # e.g., GV.OC-01
                
                row = {
                    'Function': function,
                    'Category': cat,
                    'Subcategory': subcategory_code,
                }
                
                # Generate random ratings (1-6) for 6 Managers
                # We add some "bias" to make the correlation interesting (not purely random noise)
                # e.g., Managers roughly agree on the "true" maturity but vary by +/- 1
                base_maturity = np.random.randint(0, 6) 
                
                for m in range(1, 7):
                    # Manager rating is base_maturity +/- noise
                    noise = np.random.randint(-2, 2)
                    rating = np.clip(base_maturity + noise, 0, 6)
                    row[f'Manager_{m}'] = rating
                
                data.append(row)

    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Successfully generated {len(df)} rows of synthetic data at: {filename}")
    print(df.head())

if __name__ == "__main__":
    # Ensure directory exists if needed, or just save to root
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
        
    generate_synthetic_nist_data()