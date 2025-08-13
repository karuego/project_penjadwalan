import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

Page {
    title: "Halaman Utama"

    ColumnLayout {
        anchors.centerIn: parent

        RowLayout {
            Button {
                text: "Daftar Pengajar"
                Layout.fillWidth: true
                onClicked: stackView.push("PengajarPage.qml")
            }

            Button {
                text: "Daftar Mata Kuliah"
                Layout.fillWidth: true
                onClicked: stackView.push("MataKuliahPage.qml")
            }
        }

        RowLayout {
            Button {
                text: "Daftar Ruangan"
                Layout.fillWidth: true
                onClicked: stackView.push("RuanganPage.qml")
            }

            Button {
                text: "Daftar Waktu Kuliah"
                Layout.fillWidth: true
                onClicked: stackView.push("WaktuPage.qml")
            }
        }

        RowLayout {
            Button {
                text: "Buat Jadwal"
                Layout.fillWidth: true
                onClicked: stackView.push("BuatJadwalPage.qml")
            }
        }
    }
}
