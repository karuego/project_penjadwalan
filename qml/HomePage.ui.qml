import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

Page {
    title: "Halaman Utama"

    header: Rectangle {
    // header: ToolBar {
        height: 50
        color: "#f0f0f0"

        Label {
            text: window.title

            font.bold: true
            font.pixelSize: 24
            color: "#2ecc71"
            elide: Label.ElideRight

            // anchors.centerIn: parent
            anchors.fill: parent
            horizontalAlignment: Qt.AlignHCenter
            verticalAlignment: Qt.AlignVCenter
        }

        // Tombol di pojok kanan untuk info
        ToolButton {
            text: "?"
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            onClicked: infoDialog.open() // Membuka dialog
        }
    }

    ColumnLayout {
        anchors.centerIn: parent

        RowLayout {
            Button {
                text: "Daftar Dosen"
                Layout.fillWidth: true
                onClicked: {
                    stackView.push("PengajarPage.ui.qml")
                }
            }

            Button {
                text: "Daftar Mata Kuliah"
                Layout.fillWidth: true
                onClicked: {
                    stackView.push("MataKuliahPage.ui.qml")
                }
            }
        }

        RowLayout {
            Button {
                text: "Daftar Ruangan"
                Layout.fillWidth: true
                onClicked: {
                    stackView.push("RuanganPage.ui.qml")
                }
            }

            Button {
                text: "Daftar Waktu Kuliah"
                Layout.fillWidth: true
                onClicked: {
                    stackView.push("WaktuKuliahPage.ui.qml")
                }
            }
        }
        
        RowLayout {
            Button {
                text: "Buat Jadwal"
                Layout.fillWidth: true
                onClicked: {
                    stackView.push("BuatJadwalPage.ui.qml")
                }
            }
        }
    }
}
