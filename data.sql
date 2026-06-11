PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE classes (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT NOT NULL,
    instructor TEXT NOT NULL,
    time_slot TEXT NOT NULL,
    max_capacity INTEGER NOT NULL,
    spots_remaining INTEGER NOT NULL
);

CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE,
    UNIQUE(user_id, class_id)
);

-- Initial test data
INSERT INTO users (username, email) VALUES ('johndoe', 'john@gmail.com');
INSERT INTO classes (class_name, instructor, time_slot, max_capacity, spots_remaining) VALUES 
('Morning HIIT', 'Trainer Dan', '07:00 AM', 15, 14),
('Strength Training', 'Coach Sarah', '05:30 PM', 10, 10);