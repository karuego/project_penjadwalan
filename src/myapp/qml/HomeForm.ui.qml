import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

Page {
    title: "Halaman Utama"

    // visible: true
    // width: 800
    // height: 600
    property alias button1: button1

    ColumnLayout {
        id: column

        anchors.fill: parent
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 20

        anchors.margins: 2
        spacing: 0

        Button {
            id: button1
            text: qsTr("Tutup")
            font.bold: true
            // anchors.centerIn: parent
            Layout.alignment: Qt.AlignHCenter


            /*background: Rectangle {
                implicitWidth: 100
                implicitHeight: 40
                color: button1.down ? "#d6d6d6" : "#f6f6f6"
                border.color: "#26282a"
                border.width: 1
                radius: 4
            }*/
            highlighted: true
            Material.accent: Material.Blue
            Material.background: Material.Teal
            Material.foreground: Material.Grey
            Material.elevation: 6
            Material.roundedScale: Material.NotRounded
        }

        Column {

            // anchors.centerIn: parent
            Layout.alignment: Qt.AlignHCenter

            RadioButton {
                text: qsTr("Satu")
            }
            RadioButton {
                text: qsTr("Dua")
                checked: true
            }
            RadioButton {
                text: qsTr("Tiga")
            }
        }
    }
}
