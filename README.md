# Requirements

- docker

# Set up

```bash
docker-compose up -d --build
docker-compose up -d
```

## Scripts for SQL

```bash
docker compose exec python-analysis bash

# Create Table
python scripts/create_tables.py

# Add Table
python scripts/add_tables.py <path_to_csv_file>

# Drop table
python scripts/drop_tables.py

```

## Jupyter

- http://localhost:8888/