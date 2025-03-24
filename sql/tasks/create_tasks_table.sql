CREATE TABLE IF NOT EXISTS tasks
(
    id          TEXT PRIMARY KEY,
    title       TEXT                                  NOT NULL,
    description TEXT                                  NOT NULL,
    assignee    INTEGER,
    status      INTEGER CHECK (status IN (0, 1, 2))   NOT NULL,
    severity    INTEGER CHECK (severity IN (0, 1, 2)) NOT NULL,
    priority    INTEGER CHECK (priority IN (0, 1, 2)) NOT NULL,
    due_date    DATE,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assignee) REFERENCES users (id)
);

