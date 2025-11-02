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
    data/alice_connections.csv
    data/bob_connections.csv
"""

import os
import pandas as pd
from faker import Faker
import random

def generate_synthetic_connections(
    num_rows: int,
    shared_names: list,
    shared_companies: list,
    shared_positions: list,
    unique_seed: int,
    total_unique_names: int = 40
) -> pd.DataFrame:
    """
    Generate a synthetic dataset of professional connections with intentional overlap.
    """
    random.seed(unique_seed)
    Faker.seed(unique_seed)
    fake = Faker()

    # Generate unique names
    unique_names = [
        (fake.first_name(), fake.last_name())
        for _ in range(total_unique_names)
    ]

    # Combine shared and unique names
    all_names = shared_names + unique_names
    companies = shared_companies + [fake.company() for _ in range(25)]
    positions = shared_positions + [
        "Data Scientist", "Software Engineer", "Product Manager",
        "Analyst", "Consultant", "Designer", "Marketing Specialist",
        "Sales Executive", "Project Coordinator", "Operations Manager"
    ]

    data = []
    # Ensure shared names are present
    for first_name, last_name in shared_names:
        company = random.choice(shared_companies)
        position = random.choice(shared_positions)
        data.append({
            "First Name": first_name,
            "Last Name": last_name,
            "Company": company,
            "Position": position
        })

    # Fill out the rest with random names/companies/positions
    while len(data) < num_rows:
        first_name, last_name = random.choice(all_names)
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

    # Define shared entities for overlap
    shared_names = [
        ("Alex", "Morgan"),
        ("Jordan", "Lee"),
        ("Taylor", "Kim"),
        ("Casey", "Patel"),
        ("Morgan", "Smith")
    ]
    shared_companies = [
        "Acme Corp", "Globex Inc", "Initech", "Umbrella LLC", "Stark Industries"
    ]
    shared_positions = [
        "Product Manager", "Software Engineer", "Consultant"
    ]

    df1 = generate_synthetic_connections(
        num_rows=50,
        shared_names=shared_names,
        shared_companies=shared_companies,
        shared_positions=shared_positions,
        unique_seed=42
    )
    df2 = generate_synthetic_connections(
        num_rows=50,
        shared_names=shared_names,
        shared_companies=shared_companies,
        shared_positions=shared_positions,
        unique_seed=99
    )

    df1.to_csv("data/alice_connections.csv", index=False)
    df2.to_csv("data/bob_connections.csv", index=False)

    print("✅ Synthetic connection files created with intentional overlap:")
    print(" - data/alice_connections.csv")
    print(" - data/bob_connections.csv")

if __name__ == "__main__":
    main()
