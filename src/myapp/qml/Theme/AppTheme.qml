pragma Singleton // Perintah ini wajib ada untuk menandakan ini adalah singleton

import QtQuick

QtObject {
    // Muat font di sini, di dalam singleton
    /*FontLoader {
        id: materialFontLoader;
        source: "../../fonts/MaterialSymbols.ttf"
    }*/

    // Definisikan FontLoader sebagai sebuah properti dari QtObject.
    // Kita akan menampungnya dalam sebuah properti "internal" (diawali huruf kecil).
    property FontLoader _fontLoader: FontLoader {
        source: "../../fonts/MaterialSymbols.ttf"
    }
    
    // Properti ini bisa diakses dari mana saja di seluruh aplikasi
    readonly property string materialFont: _fontLoader.name
    readonly property color primaryColor: "steelblue"
    readonly property color accentColor: "darkslateblue"
}
