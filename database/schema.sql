CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    target_user_id TEXT,
    game_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS last_alerts_sent (
    user_id TEXT,
    target_user_id TEXT,
    game_name TEXT,
    timestamp DATETIME
);
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    reminder TEXT NOT NULL,
    remind_at DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    description TEXT NOT NULL,
    is_done INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS calendars (
    user_id TEXT PRIMARY KEY,
    ical_url TEXT NOT NULL,
    timezone TEXT DEFAULT 'America/Denver'
);
ALTER TABLE calendars ADD COLUMN last_reminder_sent TEXT;

