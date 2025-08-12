import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

Page {
    title: "Daftar Mata Kuliah"

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
            text: "Ini Halaman Daftar Mata Kuliah"
            font.pixelSize: 24
            color: "#2ecc71"
            anchors.centerIn: parent
        }
    }

    Column {
        spacing: 10
        anchors.fill: parent

        Button {
            text: "Tambah Mata Kuliah"
            onClicked: {
                stackView.push("TambahMataKuliahPage.ui.qml")
            }
        }

        Grid {
            columns: 3
            spacing: 5
            // anchors.centerIn: parent
            anchors.horizontalCenter: parent.horizontalCenter // aman, karena Column tidak atur horizontal

            Repeater {
                model: 6
                Rectangle {
                    width: 50
                    height: 50
                    color: Qt.rgba(Math.random(), Math.random(), Math.random(), 1)
                }
            }
        }
    }
}
