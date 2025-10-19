function fromNumber(teksAngka) {
  const daftarHari = [
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat",
    "Sabtu",
    "Minggu",
  ];

  if (!teksAngka || typeof teksAngka !== "string" || teksAngka.trim() === "") {
    return [];
  }

  return teksAngka
    .split(",")
    .map((angkaStr) => {
      const angka = parseInt(angkaStr.trim(), 10);

      if (angka >= 1 && angka <= 7) {
        return daftarHari[angka - 1];
      }
      return null;
    })
    .filter(Boolean);
}

function fromNumberToJoinedText(teksAngka) {
  const arrayHari = fromNumber(teksAngka);
  return arrayHari.join(", ");
}
