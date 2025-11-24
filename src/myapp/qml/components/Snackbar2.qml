import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

Popup {
    id: control
    Material.theme: Material.Light

    // Properti kustom untuk pesan dan teks tombol
    property string text: ""
    property string actionText: ""

    // Sinyal yang dipancarkan saat tombol aksi diklik
    signal actionClicked

    // margins: 16

    // Durasi tampil (misal: 3 detik)
    property int duration: 3000

    // Jangan blokir UI di belakangnya
    modal: false
    dim: false

    // Tampilan visual (styling)
    background: Rectangle {
        color: "#333" // Warna latar belakang gelap khas snackbar
        radius: 4
    }

    contentItem: Row {
        spacing: 12

        Label {
            text: control.text
            color: "white"
            padding: 12
        }

        Button {
            // Hanya tampilkan tombol jika actionText diisi
            visible: control.actionText.length > 0
            text: control.actionText

            // Beri style "flat" agar menyatu
            flat: true

            height: parent.height

            // Styling untuk teks tombol (opsional)
            contentItem: Text {
                text: control.actionText
                color: "#4CAF50" // Contoh warna aksen
                font.bold: true
            }

            onClicked: {
                control.actionClicked();
                control.close();
            }
        }
    }

    // Timer untuk menutup otomatis
    Timer {
        id: closeTimer
        interval: control.duration
        onTriggered: control.close()
    }

    // Saat dibuka, mulai timer
    onOpened: {
        closeTimer.start();
    }

    // Saat ditutup, hentikan timer (jika ditutup manual)
    onClosed: {
        closeTimer.stop();
    }
}
