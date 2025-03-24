import sqlite3
import uuid
from datetime import date, timedelta
import random
from pathlib import Path

# Resolve DB_PATH using Path
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent.parent / "database.db"

USER_IDS = list(range(1, 11))  # Users with IDs 1-10 (after seeding users)
STATUSES = [0, 1, 2]  # 0 = To Do, 1 = In Progress, 2 = Done
SEVERITIES = [0, 1, 2]  # 0 = Low, 1 = Medium, 2 = High
PRIORITIES = [0, 1, 2]  # 0 = Low, 1 = Medium, 2 = High

# Base data for generating tasks
TASK_TITLES = [
    "Fix login issue",
    "Update user profile",
    "Review code changes",
    "Test new feature",
    "Write documentation",
    "Optimize database",
    "Design UI mockup",
    "Deploy to production",
    "Resolve bug",
    "Plan sprint"
]
DESCRIPTIONS = [
    "Critical issue affecting users",
    "Minor update requested by team",
    "Routine task for next release",
    "High-priority feature for client",
    "Documentation for new module",
    "Performance improvement needed",
    "UI enhancement for better UX",
    "Deployment preparation",
    "Bug reported by QA",
    "Planning for upcoming sprint"
]


# Generate 100 tasks
def generate_tasks(num_tasks=100):
    tasks = []
    start_date = date(2025, 3, 20)  # Starting from today

    for i in range(num_tasks):
        task_id = str(uuid.uuid4())
        title = f"{random.choice(TASK_TITLES)} #{i + 1}"
        description = random.choice(DESCRIPTIONS)
        assignee = random.choice(USER_IDS + [None])  # Random user (1-10) or unassigned
        status = random.choice(STATUSES)
        severity = random.choice(SEVERITIES)
        priority = random.choice(PRIORITIES)
        # 20% chance of due today, otherwise random day in next 30 days
        if random.random() < 0.2:  # ~20 tasks due today
            due_date = start_date
        else:
            due_date = start_date + timedelta(days=random.randint(1, 30))  # Due in 1-30 days

        tasks.append((
            task_id,
            title,
            description,
            assignee,
            status,
            severity,
            priority,
            due_date.isoformat()
        ))

    return tasks


# Seed the database
def seed_tasks_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Generate tasks
    tasks = generate_tasks(100)

    # Insert tasks
    cursor.executemany("""
        INSERT INTO tasks (id, title, description, assignee, status, severity, priority, due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, tasks)

    conn.commit()
    print(f"Seeded {len(tasks)} tasks into the database at {DB_PATH}")
    conn.close()


if __name__ == "__main__":
    seed_tasks_db()
