# Requirements

- docker
- Share IP address (to allow connections to Google Cloud SQL)

# Set up

```bash
docker-compose up -d --build
docker-compose up -d
```

## Run scripts for SQL

```bash
docker compose exec python-analysis bash

# Create Empty Table
python scripts/create_tables.py

# Add Table
python scripts/add_tables.py <path_to_csv_file>

# Drop table
python scripts/drop_tables.py

```

## Jupyter

While the `python-analysis` docker container is running, access below.

- http://localhost:8888/