CREATE TABLE IF NOT EXISTS "system_log" (
    id INTEGER PRIMARY KEY,
    username  TEXT,
    action TEXT,
    detail TEXT,
    datetime TEXT
);