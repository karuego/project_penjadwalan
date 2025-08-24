import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

Page {
    title: qsTr("Halaman Utama")

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 8

        RowLayout {
            spacing: 16

            Button {
                text: qsTr("Daftar Waktu Kuliah")
                Layout.fillWidth: true
                onClicked: stackView.push("WaktuPage.qml")

                scale: activeFocus || hovered ? 1.05 : 1.0
                Behavior on scale { NumberAnimation { duration: 150 } }
            }

            Button {
                text: qsTr("Daftar Pengajar")
                Layout.fillWidth: true
                onClicked: stackView.push("PengajarPage.qml")
                Material.roundedScale: Material.ExtraSmallScale

                scale: activeFocus || hovered ? 1.05 : 1.0
                Behavior on scale { NumberAnimation { duration: 150 } }
            }
        }

        RowLayout {
            spacing: 16

            Button {
                text: qsTr("Daftar Mata Kuliah")
                Layout.fillWidth: true
                onClicked: stackView.push("MataKuliahPage.qml")
                Material.roundedScale: Material.ExtraSmallScale

                scale: activeFocus || hovered ? 1.05 : 1.0
                Behavior on scale { NumberAnimation { duration: 150 } }
            }

            Button {
                text: qsTr("Daftar Ruangan")
                Layout.fillWidth: true
                onClicked: stackView.push("RuanganPage.qml")
                scale: activeFocus || hovered ? 1.05 : 1.0
                Behavior on scale { NumberAnimation { duration: 150 } }
            }
        }

        RowLayout {
            Button {
                text: qsTr("Buat Jadwal")
                Layout.fillWidth: true
                onClicked: stackView.push("BuatJadwalPage.qml")
                Material.roundedScale: Material.NotRounded
                scale: activeFocus || hovered ? 1.05 : 1.0
                Behavior on scale { NumberAnimation { duration: 150 } }
            }
        }
    }
}
