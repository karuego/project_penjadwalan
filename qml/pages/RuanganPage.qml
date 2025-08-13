import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

Page {
    title: "Daftar Ruangan"

    Column {
        spacing: 10
        anchors.fill: parent

        Label {
            text: "Nama Ruangan :"
            // font.pixelSize: 24
            color: "#2ecc71"
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Button {
            text: "Simpan"
            onClicked: {
                // stackView.pop()
            }
        }
    }
}
