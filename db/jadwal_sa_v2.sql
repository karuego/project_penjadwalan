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
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    hari    INTEGER NOT NULL, -- 1: Senin, 2: Selasa, 3: Rabu, 4: Kamis, 5: Jumat, 6: Sabtu, 7: Minggu
    mulai   TEXT    NOT NULL, -- 'HH:MM'
    selesai TEXT    NOT NULL, -- 'HH:MM'

    UNIQUE(hari, mulai, selesai)
);

CREATE TABLE pengajar (
    id                  TEXT PRIMARY KEY,
    nama                TEXT NOT NULL,
    jenis               TEXT NOT NULL       DEFAULT 'dosen', -- 'dosen', 'asdos'
    preferensi_waktu    TEXT -- Comma-separated list of int representing non-preferred days (1-7)
);

-- CREATE TABLE preferensi_pengajar (
--     id           INTEGER PRIMARY KEY AUTOINCREMENT,
--     pengajar_id  INTEGER NOT NULL,
--     waktu_id     INTEGER NOT NULL,
--     -- hindari   BOOLEAN NOT NULL    DEFAULT TRUE,
--
--     FOREIGN KEY (pengajar_id) REFERENCES pengajar(id),
--     FOREIGN KEY (waktu_id) REFERENCES waktu(id)
-- );

CREATE TABLE ruangan (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nama    TEXT    NOT NULL    UNIQUE,
    jenis   TEXT    NOT NULL    DEFAULT 'teori', -- jenis: 'teori', 'praktek'

    UNIQUE(nama, jenis)
);

-- Unit yang akan dijadwalkan
CREATE TABLE mata_kuliah (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nama            TEXT    NOT NULL,
    semester        INTEGER NOT NULL,

    UNIQUE(nama, semester)
);

CREATE TABLE komponen_mk (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_komponen           TEXT    NOT NULL, -- Misal: 'Teori Basis Data', 'Praktikum Basis Data'
    jenis                   TEXT    NOT NULL    DEFAULT 'teori', -- 'teori' atau 'praktek'
    sks                     INTEGER NOT NULL, -- Jumlah blok 45 menit
    jumlah_kelas            INTEGER NOT NULL,
    jumlah_sesi_praktikum   INTEGER DEFAULT 0 -- "Default 1, bisa 2 atau lebih; Nilai 0 atau null jika bukan praktikum"]
    mata_kuliah_id          INTEGER NOT NULL,

    FOREIGN KEY (mata_kuliah_id)    REFERENCES mata_kuliah(id),

    UNIQUE(nama, mata_kuliah_id)
);

CREATE TABLE pengampu (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    komponen_mk_id  INTEGER NOT NULL,
    pengajar_id     INTEGER NOT NULL,

    FOREIGN KEY (komponen_mk_id)   REFERENCES komponen_mk(id),
    FOREIGN KEY (pengajar_id)      REFERENCES pengajar(id),

    UNIQUE(komponen_mk_id, pengajar_id)
);

-- Merepresentasikan satu komponen yang telah dijadwalkan.
CREATE TABLE jadwal (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    komponen_mk_id  INTEGER NOT NULL,
    waktu_mulai_id  INTEGER NOT NULL,
    pengajar_id     INTEGER NOT NULL,
    ruangan_id      INTEGER, -- Bisa NULL jika online

    kelas           CHAR    NOT NULL,
    sesi_ke         INTEGER, -- Sesi ke-berapa untuk praktikum, 1 atau 2; 0 jika bukan praktiktum
    durasi_blok     INTEGER NOT NULL,
    daring          BOOLEAN NOT NULL    DEFAULT FALSE, -- True jika online

    FOREIGN KEY (komponen_mk_id)    REFERENCES komponen_mk(id),
    FOREIGN KEY (waktu_mulai_id)    REFERENCES waktu(id),
    FOREIGN KEY (pengajar_id)       REFERENCES pengajar(id),

    UNIQUE(komponen_mk_id, waktu_mulai_id, pengajar_id, ruangan_id, kelas, daring)
);

PRAGMA wal_checkpoint(TRUNCATE);
