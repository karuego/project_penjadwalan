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

CREATE TABLE ruangan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL UNIQUE,

    -- jenis: 'teori', 'praktek'
    jenis TEXT NOT NULL DEFAULT 'teori'
);

CREATE TABLE pengajar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL
    jenis TEXT NOT NULL DEFAULT 'teori'
);

CREATE TABLE mata_kuliah (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    semester INTEGER NOT NULL,
    jumlah_kelas INTEGER NOT NULL,
    jumlah_sesi INTEGER DEFAULT 0,
    jenis TEXT NOT NULL DEFAULT 'teori'
);

CREATE TABLE waktu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hari TEXT NOT NULL,
    -- hari TEXT CHECK (hari IN ('Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'))
    jam_mulai TIME NOT NULL,
    jam_selesai TIME NOT NULL
);

CREATE TABLE pengampu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mata_kuliah_id INTEGER,
    pengajar_id INTEGER,
    FOREIGN KEY (mata_kuliah_id) REFERENCES mata_kuliah(id),
    FOREIGN KEY (pengajar_id) REFERENCES pengajar(id)
);

CREATE TABLE preferensi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pengajar_id INTEGER NOT NULL,
    waktu_id INTEGER NOT NULL,
    hindari BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (pengajar_id) REFERENCES pengajar(id),
    FOREIGN KEY (waktu_id) REFERENCES waktu(id)
);

CREATE TABLE jadwal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mata_kuliah_id INTEGER NOT NULL,
    kelas CHAR NOT NULL,
    ruangan_id INTEGER NOT NULL,

    -- jenis: teori, praktek
    jenis TEXT NOT NULL DEFAULT 'teori',

    -- 0   = teori
    -- 1.. = praktek
    sesi_kelas INTEGER DEFAULT 0,

    pengajar_id INTEGER NOT NULL,
    waktu_id INTEGER NOT NULL,
    daring BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (mata_kuliah_id) REFERENCES mata_kuliah(id),
    FOREIGN KEY (ruangan_id) REFERENCES ruangan(id),
    FOREIGN KEY (pengajar_id) REFERENCES pengajar(id),
    FOREIGN KEY (waktu_id) REFERENCES waktu(id)
);

PRAGMA wal_checkpoint(TRUNCATE);
