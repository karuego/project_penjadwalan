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

-- Create ENUM equivalent tables
--CREATE TABLE JenisSesi (
--    value TEXT PRIMARY KEY
--);

--INSERT INTO JenisSesi (value) VALUES ('teori'), ('praktek');

--CREATE TABLE NamaHari (
--    value TEXT PRIMARY KEY
--);

--INSERT INTO NamaHari (value) VALUES ('senin'), ('selasa'), ('rabu'), ('kamis'), ('jumat'), ('sabtu');

--- ## Table Creation

CREATE TABLE ruangan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL UNIQUE,
    jenis TEXT NOT NULL DEFAULT 'teori'
    -- jenis TEXT CHECK (jenis IN ('teori', '', 'Rabu', 'Kamis', 'Jumat'))
    -- FOREIGN KEY (jenis) REFERENCES JenisSesi(value)
);

CREATE TABLE dosen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL
);

CREATE TABLE mata_kuliah (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    semester INTEGER NOT NULL,
    jumlah_kelas INTEGER NOT NULL,
    jenis TEXT NOT NULL DEFAULT 'teori'
    -- FOREIGN KEY (jenis) REFERENCES JenisSesi(value)
);

CREATE TABLE waktu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hari TEXT NOT NULL,
    -- hari TEXT CHECK (hari IN ('Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'))
    jam_mulai TIME NOT NULL,
    jam_selesai TIME NOT NULL
    -- FOREIGN KEY (hari) REFERENCES NamaHari(value)
);

CREATE TABLE pengampu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mata_kuliah_id INTEGER,
    dosen_id INTEGER,
    FOREIGN KEY (mata_kuliah_id) REFERENCES mata_kuliah(id),
    FOREIGN KEY (dosen_id) REFERENCES dosen(id)
);

CREATE TABLE preferensi_dosen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dosen_id INTEGER NOT NULL,
    waktu_id INTEGER NOT NULL,
    hindari BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (dosen_id) REFERENCES dosen(id),
    FOREIGN KEY (waktu_id) REFERENCES waktu(id)
);

CREATE TABLE jadwal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mata_kuliah_id INTEGER NOT NULL,
    kelas CHAR NOT NULL,
    ruangan_id INTEGER NOT NULL,
    sesi_kelas INTEGER,
    dosen_id INTEGER NOT NULL,
    waktu_id INTEGER NOT NULL,
    daring BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (mata_kuliah_id) REFERENCES mata_kuliah(id),
    FOREIGN KEY (ruangan_id) REFERENCES ruangan(id),
    FOREIGN KEY (dosen_id) REFERENCES dosen(id),
    FOREIGN KEY (waktu_id) REFERENCES waktu(id)
);

PRAGMA wal_checkpoint(TRUNCATE);
