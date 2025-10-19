function capitalizeFirstLetter(string) {
  // Menangani kasus jika input bukan string atau string kosong
  if (typeof string !== "string" || string.length === 0) {
    return string;
  }

  return string.charAt(0).toUpperCase() + string.slice(1);
}

function toTitleCase(sentence) {
  if (typeof sentence !== "string" || sentence.length === 0) {
    return sentence;
  }

  return sentence
    .split(" ") // 1. Pecah kalimat menjadi array kata-kata, dipisahkan oleh spasi
    .map((word) => capitalizeFirstLetter(word)) // 2. Terapkan fungsi kapitalisasi pada setiap kata
    .join(" "); // 3. Gabungkan kembali array menjadi satu string dengan spasi
}
