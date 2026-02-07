-- SQLite
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT,
    role TEXT
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    location TEXT NOT NULL,
    price INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_id INTEGER,
    ticket_id TEXT
);

INSERT INTO events (name, date, location, price) VALUES
('Music Night', '2026-03-10', 'Hyderabad', 500),
('Tech Conference', '2026-04-15', 'Bangalore', 1000),
('Food Festival', '2026-02-25', 'Chennai', 300);
