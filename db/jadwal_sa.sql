PRAGMA user_version = 1;
PRAGMA application_id = 0x12345678;

PRAGMA cache_size = 2000;
PRAGMA journal_mode = WAL;
-- PRAGMA auto_vacuum = FULL;
-- VACUUM;

PRAGMA foreign_keys = ON;
PRAGMA automatic_index = ON;
PRAGMA case_sensitive_like = OFF;
PRAGMA synchronous = NORMAL;
PRAGMA locking_mode = EXCLUSIVE;

-- Blok waktu 45 menit
CREATE TABLE timeslots (
    id      INTEGER PRIMARY KEY,
    hari    INTEGER NOT NULL,
    mulai   TEXT    NOT NULL,
    selesai TEXT    NOT NULL,

    UNIQUE(hari, mulai, selesai)
);

CREATE TABLE pengajar (
    id                  TEXT PRIMARY KEY, -- Nomor Induk (NIDN/NIM)
    nama                TEXT NOT NULL,
    jenis               TEXT NOT NULL DEFAULT 'dosen', -- jenis: 'dosen', 'asdos'
    preferensi_waktu    TEXT -- comma-separated list of integers representing non-preferred days (1-7)
);

CREATE TABLE ruangan (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nama    TEXT    NOT NULL UNIQUE, -- Contoh: "FT-I.7", "FT-III.2", "FT-III.4", "FT-III.5"
    jenis   TEXT    NOT NULL DEFAULT 'teori', -- jenis: 'teori', 'praktek'

    UNIQUE(nama, jenis)
);

-- Unit yang akan dijadwalkan
CREATE TABLE mata_kuliah (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nama            TEXT    NOT NULL, -- Misal: 'Basis Data', 'Praktikum Basis Data'
    jenis           TEXT    NOT NULL    DEFAULT 'teori', -- 'teori' atau 'praktek'
    sks             INTEGER NOT NULL, -- Jumlah blok 45 menit
    semester        INTEGER NOT NULL,
    jumlah_kelas    INTEGER NOT NULL, -- jumlah kelas yang mengikuti mata kuliah
    pengajar_id     TEXT,

    FOREIGN KEY (pengajar_id) REFERENCES pengajar(id)
);

-- CREATE TABLE preferensi_pengajar (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     pengajar_id INTEGER NOT NULL,
--     waktu_id INTEGER NOT NULL,
--     -- hindari BOOLEAN NOT NULL DEFAULT TRUE,
--     FOREIGN KEY (pengajar_id) REFERENCES pengajar(id),
--     FOREIGN KEY (waktu_id) REFERENCES waktu(id)
-- );

-- Merepresentasikan satu komponen yang telah dijadwalkan.
CREATE TABLE jadwal (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    hari            TEXT    NOT NULL, -- Contoh: "Senin", "Selasa", "Rabu"
    jam             TEXT    NOT NULL, -- Contoh: "08:00 - 09:30", "09:35 - 11:05"

    matakuliah      TEXT    NOT NULL, -- "Basis Data", "Praktikum Basis Data"
    jenis           TEXT    NOT NULL, -- 'teori' atau 'praktek'

    sks             INTEGER NOT NULL, -- 2 (teori) atau 3 (teori + praktikum (jenis==praktek))
    semester        INTEGER NOT NULL,

    kelas           CHAR    NOT NULL, -- Contoh: 'A', 'B', 'C'
    ruangan         TEXT    NOT NULL, -- Contoh: "FT-III.2", "FT-III.6", "FT-III.7"
    daring          BOOLEAN NOT NULL    DEFAULT FALSE, -- True jika ruangan habis sehingga akan dialihkan ke perkuliahan online

    pengajar        TEXT    NOT NULL -- Contoh: "Farhan Hidayat", "Safar Husada"
);

PRAGMA wal_checkpoint(TRUNCATE);
