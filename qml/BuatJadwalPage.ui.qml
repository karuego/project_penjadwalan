import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

Page {
    title: "Pembuatan Jadwal"

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
            text: "Ini Halaman Pembuatan Jadwal"
            font.pixelSize: 24
            color: "#2ecc71"
            anchors.centerIn: parent
        }
    }

    Column {
        spacing: 10
        anchors.fill: parent

        Button {
            text: "Lihat Jadwal Teori"
            onClicked: {
                stackView.push("JadwalTeoriPage.ui.qml")
            }
        }

        Button {
            text: "Lihat Jadwal Praktek"
            onClicked: {
                stackView.push("JadwalPraktekPage.ui.qml")
            }
        }
    }
}
