PRAGMA foreign_keys = ON;
CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE);
CREATE TABLE login_events (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    source_ip TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    outcome TEXT NOT NULL CHECK (outcome IN ('success', 'failure'))
);
CREATE INDEX login_events_user_time ON login_events(user_id, occurred_at);
