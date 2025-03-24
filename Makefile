DATABASE_NAME = database.db
CREATE_TABLE_SCRIPTS = ./sql/users/create_users_table.sql ./sql/tasks/create_tasks_table.sql
SEED_SCRIPTS = ./sql/users/seed_users_table.py ./sql/tasks/seed_tasks_table.py

# Default target
all: db

# Target to create the SQLite database
db: db-tables seed-tables

# Create tables in the SQLite database
db-tables:
	@echo "Creating SQLite database: $(DATABASE_NAME)"
	@echo "Running SQL script: $(CREATE_TABLE_SCRIPTS)"
	@for script in $(CREATE_TABLE_SCRIPTS); do \
		if [ ! -f $$script ]; then \
			echo "ERROR: SQL script $$script not found!"; \
			exit 1; \
		fi; \
		sqlite3 $(DATABASE_NAME) < $$script; \
	done
	@echo "Tables created successfully."

# Seed the database with initial data
seed-tables: db-tables
	@echo "Seeding database with initial data"
	@for script in $(SEED_SCRIPTS); do \
		if [ ! -f $$script ]; then \
			echo "ERROR: Seed script $$script not found!"; \
			exit 1; \
		fi; \
		python $$script; \
	done
	@echo "Database seeded successfully."

# Clean up the database file (optional)
clean:
	@echo "Removing database file: $(DATABASE_NAME)"
	@if [ -f "$(DATABASE_NAME)" ]; then \
		rm -f $(DATABASE_NAME); \
		echo "Database file removed."; \
	else \
		echo "Database file does not exist."; \
	fi

# Help message
help:
	@echo "Makefile for SQLite database creation with multiple SQL scripts"
	@echo "Usage:"
	@echo "  make           - Create the SQLite database using the SQL scripts"
	@echo "  make seed-tables - Seed the database with initial data"
	@echo "  make clean     - Remove the database file"
	@echo "  make help      - Display this help message"