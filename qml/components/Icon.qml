import QtQuick
import Theme 1.0
import "../helpers/MaterialIcons.js" as MIcons

// Komponen reusable untuk menampilkan sebuah ikon dari font.
Text {
    // --- Properti yang bisa diatur dari luar ---
    property string name: "help" // Nama ikon default jika tidak diatur
    property int size: 24
    // property color color: "#333"

    // --- Konfigurasi Internal ---
    text: name
    font.family: AppTheme.materialFont
    font.pixelSize: size
    // color: color
    color: "#333"

    // Atur ukuran Text agar pas dengan ukuran ikon
    width: paintedWidth
    height: paintedHeight

    Behavior on color { ColorAnimation { duration: 200 } }
}
