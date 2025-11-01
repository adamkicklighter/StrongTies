# Data Directory

This folder contains sample connection data for the StrongTies project.

## Contents

- `alice_connections.csv`  
- `bob_connections.csv`  
  These files are **synthetic datasets** generated locally using `src/generate_sample_connections.py`.  
  No real user data or external sources are included.

## Privacy & Usage

- All data is processed locally.
- No scraping or API calls to third-party platforms.
- No external transmission of personally identifiable information (PII).
- Datasets are for demonstration, testing, and development only.

## Regenerating Sample Data

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
