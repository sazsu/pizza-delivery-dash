--
-- File generated with SQLiteStudio v3.4.13 on Fri Feb 7 00:58:59 2025
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Stats

CREATE TABLE IF NOT EXISTS Stats (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    date       TEXT,
    time_taken REAL
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
