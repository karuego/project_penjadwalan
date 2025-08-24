import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

Page {
    title: "Daftar Waktu Kuliah"

    ColumnLayout {
        spacing: 10
        anchors.fill: parent

        Button {
            id: tambahDosen
            text: qsTr("Tambah Waktu Kuliah")
            Accessible.name: qsTr("Tambah Waktu Kuliah")
            onClicked: stackView.push("TambahWaktuPage.qml") // qmllint disable unqualified

            Material.foreground: Material.Pink

            // width: 100
            // height: 55
            implicitHeight: 55
            Layout.alignment: Qt.AlignHCenter
            Layout.bottomMargin: 16

            background: Rectangle {
                radius: 8

                // Atur warna Rectangle agar berubah secara dinamis
                color: tambahDosen.down ? "#9c9c9c" : tambahDosen.hovered ? "#cccaca" : "#e0e0e0"

                // border.color: "#adadad"
                // border.width: 1

                // Animasi halus untuk perubahan warna
                Behavior on color { ColorAnimation { duration: 150 } }
            }
        }
    }
}
