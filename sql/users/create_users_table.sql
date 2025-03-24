CREATE TABLE IF NOT EXISTS users
(
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL
);

-- Create an index on the 'username' column to speed up queries
CREATE INDEX IF NOT EXISTS idx_username ON users (username);