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
    id INTEGER PRIMARY KEY,
    hari INTEGER NOT NULL,
    mulai TEXT NOT NULL,
    selesai TEXT NOT NULL,
    UNIQUE(hari, mulai, selesai)
);

CREATE TABLE pengajar (
    id TEXT PRIMARY KEY,
    nama TEXT NOT NULL,
    -- jenis: 'dosen', 'asdos'
    jenis TEXT NOT NULL DEFAULT 'dosen',
    preferensi_waktu TEXT
);

CREATE TABLE mata_kuliah (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    semester INTEGER NOT NULL
);

CREATE TABLE ruangan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL UNIQUE,
    -- jenis: 'teori', 'praktek'
    jenis TEXT NOT NULL DEFAULT 'teori'
);

-- Unit yang akan dijadwalkan
CREATE TABLE komponen_mk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mata_kuliah_id INTEGER NOT NULL,
    nama_komponen TEXT NOT NULL, -- Misal: 'Teori Basis Data', 'Praktikum Basis Data'
    durasi_blok INTEGER NOT NULL, -- Jumlah blok 45 menit
    jenis TEXT NOT NULL DEFAULT 'teori', -- 'teori' atau 'praktek'
    jumlah_kelas INTEGER NOT NULL,
    jumlah_sesi_praktikum INTEGER NOT NULL DEFAULT 1, -- Default 1, bisa 2 atau lebih
    FOREIGN KEY (mata_kuliah_id) REFERENCES mata_kuliah(id)
);

CREATE TABLE pengampu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pengajar_id TEXT,
    komponen_mk_id INTEGER NOT NULL,
    FOREIGN KEY (pengajar_id) REFERENCES pengajar(id),
    FOREIGN KEY (komponen_mk_id) REFERENCES komponen_mk(id)
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    komponen_mk_id INTEGER NOT NULL,
    pengajar_id INTEGER NOT NULL,
    kelas CHAR NOT NULL,
    -- semester INTEGER NOT NULL,
    -- jenis TEXT NOT NULL DEFAULT 'teori', -- 'teori' atau 'praktek'
    sesi_ke INTEGER NOT NULL, -- Sesi ke-berapa untuk praktikum, 1 atau 2
    waktu_id_start INTEGER NOT NULL,
    durasi_blok INTEGER NOT NULL,
    ruangan_id INTEGER NULL, -- Bisa NULL jika online
    daring BOOLEAN NOT NULL DEFAULT FALSE, -- True jika online

    FOREIGN KEY (komponen_mk_id) REFERENCES komponen_mk(id),
    FOREIGN KEY (pengajar_id) REFERENCES pengajar(id),
    FOREIGN KEY (waktu_id_start) REFERENCES waktu(id)
);

PRAGMA wal_checkpoint(TRUNCATE);
