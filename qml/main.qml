import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

// Window {
//     width: 640
//     height: 480
//     visible: true
//     title: qsTr("Penjadwalan")
// }
ApplicationWindow {
    id: window
    visible: true
    width: 800
    height: 600
    title: "Aplikasi Qt Quick & Python"

    // StackView adalah area di mana halaman-halaman akan ditampilkan
    StackView {
        id: stackView
        anchors.fill: parent
        // Halaman awal yang ditampilkan saat aplikasi pertama kali berjalan
        initialItem: "HomePage.qml"
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
                    stackView.push("HomePage.qml")
                }
            }

            Button {
                text: "Pengaturan"
                Layout.fillWidth: true
                onClicked: {
                    stackView.push("SettingsPage.qml")
                }
            }
        }
    }*/
}
