import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Material

import Theme 1.0

// Window {
ApplicationWindow {
    id: window
    visible: true
    width: 800
    height: 600
    title: qsTr("Aplikasi Penjadwalan w/ Simulated Annealing")
    Material.theme: Material.Light

    // 1. Muat font menggunakan FontLoader
    /*FontLoader {
        id: materialFontLoader
        source: "fonts/MaterialSymbols.ttf" // Path relatif ke file font
    }*/

    // 2. Gunakan font yang sudah dimuat
    /*Text {
        anchors.horizontalCenter: parent.horizontalCenter

        // Gunakan nama font dari FontLoader setelah statusnya "Ready"
        // Properti .name akan berisi nama family font, misal: "Material Symbols Outlined"
        // font.family: materialFontLoader.name
        font.family: AppTheme.materialFont
        // font.pixelSize: 48
        font.pixelSize: 60
        // color: "darkgreen"
        color: AppTheme.primaryColor // Gunakan juga warna dari theme

        // Pastikan FontLoader selesai memuat sebelum menampilkan teks
        // text: materialFontLoader.status == FontLoader.Ready ? "verified_user" : ""
        text: "home"
    }*/


    // StackView adalah area di mana halaman-halaman akan ditampilkan
    StackView {
        id: stackView
        anchors.fill: parent

        // Halaman awal yang ditampilkan saat aplikasi pertama kali berjalan
        initialItem: "HomePage.ui.qml"
    }

    Dialog {
        id: infoDialog
        title: "Informasi"
        modal: true // Mencegah interaksi dengan window di belakangnya
        anchors.centerIn: parent
        standardButtons: Dialog.Ok // Tombol OK standar

        Label {
            text: "Aplikasi ini dibuat dengan QML."
        }
    }

    // Footer berisi tombol navigasi
    /*footer: Frame {
        RowLayout {
            anchors.fill: parent

            Button {
                text: "Home"
                Layout.fillWidth: true
                onClicked: {
                    // Mendorong halaman baru ke tumpukan.
                    // Jika halaman sudah ada, ia akan kembali ke sana.
                    stackView.push("HomePage.ui.qml")
                }
            }

            Button {
                text: "Dosen"
                Layout.fillWidth: true
                onClicked: {
                    stackView.push("DosenPage.ui.qml")
                }
            }
        }
    }*/
}
