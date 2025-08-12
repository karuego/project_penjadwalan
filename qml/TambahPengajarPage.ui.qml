import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

Page {
    title: "Tambah Pengajar"

    header: Rectangle {
        height: 50
        color: "#f0f0f0"

        Button {
            text: "Kembali"
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
            onClicked: stackView.pop()
        }

        Label {
            text: "Ini Halaman Tambah Pengajar"
            font.pixelSize: 24
            color: "#2ecc71"
            anchors.centerIn: parent
        }
    }

    Column {
        spacing: 10
        anchors.fill: parent


    }
}
