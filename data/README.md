# Data Directory

This folder contains sample connection data and targeting preferences for the StrongTies project.

## Contents

- `alice_connections.csv`  
- `bob_connections.csv`  
  These files are **synthetic datasets** generated locally using `src/generate_sample_connections.py`.  
  No real user data or external sources are included.

- `targets.json`  
  Specifies **target companies and roles** for network analysis and graph construction.  
  Example format:
  ```json
  {
    "companies": ["Acme Corp", "Globex", "Initech"],
    "roles": ["Product Manager", "Data Scientist", "VP Engineering"]
  }
  ```

## Privacy & Usage

- All data is processed locally.
- No scraping or API calls to third-party platforms.
- No external transmission of personally identifiable information (PII).
- Datasets are for demonstration, testing, and development only.

## Regenerating Sample Data

> **Note:**  
> Example `.csv` files are intentionally **not tracked in version control** (see `.gitignore`).  
> To view or use the sample CSVs, you must generate them locally.

To create or extend sample connection files, run:

```bash
python src/generate_sample_connections.py
```

This will output new CSVs in the `data/` directory.

## Data Format

Each CSV contains columns such as:
- `person_id`
- `name`
- `connection_id`
- `connection_name`
- (other relevant fields as defined in `generate_sample_connections.py`)

See the script or open a sample CSV for details.

## Target Preferences Format

See `targets.json` for specifying companies and roles to focus analysis and suggestions.
