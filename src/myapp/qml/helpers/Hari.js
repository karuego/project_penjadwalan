const NAMA_HARI = [
  "_",
  "Senin",
  "Selasa",
  "Rabu",
  "Kamis",
  "Jumat",
  "Sabtu",
  "Minggu",
];

function getNama(id) {
  if (0 < id && id < NAMA_HARI.length) return NAMA_HARI[id];
  // return None;
  return "*Error*";
}

function getId(nama) {
  const target = nama.toLowerCase();

  NAMA_HARI.forEach((item, index) => {
    if (s.toLowerCase() == target) return i;
  });

  return -1;
}

function getAll() {
  return NAMA_HARI.slice(1);
}

function parseHari(teksAngka) {
  if (!teksAngka || typeof teksAngka !== "string" || teksAngka.trim() === "") {
    return [];
  }

  return teksAngka
    .split(",")
    .map((angkaStr) => {
      const angka = parseInt(angkaStr.trim(), 10);

      if (angka >= 1 && angka <= 7) {
        return getNama(angka);
      }
      return null;
    })
    .filter(Boolean);
}

function parseHariToJoinedText(teksAngka) {
  const arrayHari = parseHari(teksAngka);
  return arrayHari.join(", ");
}

function parseHariMap(teksAngka) {
  if (!teksAngka || typeof teksAngka !== "string" || teksAngka.trim() === "") {
    return [];
  }

  return teksAngka
    .split(",")
    .map((angkaStr) => {
      const angka = parseInt(angkaStr.trim(), 10);

      if (angka >= 1 && angka <= 7) {
        return {
          id: angka,
          nama: getNama(angka),
        };
      }

      return null;
    })
    .filter(Boolean);
}
