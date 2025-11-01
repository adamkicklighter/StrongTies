# SPDX-License-Identifier: Polyform-Noncommercial-1.0.0

"""
generate_sample_connections.py
---------------------------------
Generates two synthetic CSV files representing LinkedIn-style connection data.
Each CSV contains:
    - First Name
    - Last Name
    - Company
    - Position

This script uses the 'faker' library to generate realistic but fictional data.
All data is non-personal and for demonstration or testing only.

Output:
    data/sample_connections_1.csv
    data/sample_connections_2.csv
"""

import os
import pandas as pd
from faker import Faker
import random

def generate_synthetic_connections(num_rows: int, seed: int = None):
    """
    Generate a synthetic dataset of professional connections.
    """
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)
    
    fake = Faker()
    companies = [fake.company() for _ in range(50)]
    positions = [
        "Data Scientist", "Software Engineer", "Product Manager",
        "Analyst", "Consultant", "Designer", "Marketing Specialist",
        "Sales Executive", "Project Coordinator", "Operations Manager"
    ]

    data = []
    for _ in range(num_rows):
        first_name = fake.first_name()
        last_name = fake.last_name()
        company = random.choice(companies)
        position = random.choice(positions)
        data.append({
            "First Name": first_name,
            "Last Name": last_name,
            "Company": company,
            "Position": position
        })
    return pd.DataFrame(data)

def main():
    os.makedirs("data", exist_ok=True)

    df1 = generate_synthetic_connections(50, seed=42)
    df2 = generate_synthetic_connections(50, seed=99)

    # Use user IDs in filenames for compatibility with data_loader.py
    df1.to_csv("data/alice_connections.csv", index=False)
    df2.to_csv("data/bob_connections.csv", index=False)

    print("✅ Synthetic connection files created:")
    print(" - data/alice_connections.csv")
    print(" - data/bob_connections.csv")

if __name__ == "__main__":
    main()
