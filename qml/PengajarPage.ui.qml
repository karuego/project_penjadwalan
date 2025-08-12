import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

// import "../helpers"
import "helpers/MaterialIcons.js" as MIcons
import Theme

Page {
    title: "Daftar Pengajar"
    Material.theme: Material.Light

    header: ToolBar {

        Frame {
            anchors.fill: parent
            
            ToolButton {
                // icon.source: "qrc:/icons/arrow_back.svg" // ganti dengan file SVG

                // font.family: MaterialIcons.fontFamily
                font.family: AppTheme.materialFont
                font.pixelSize: 24

                // text: "\u25C0" // panah kiri Unicode
                text: MIcons.get("arrow_back")
                // text: MaterialIcons.get("arrow_back")

                // anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                
                onClicked: stackView.pop()
            }

            /*Label {
                text: "Kembali"
                font.family: "sans"
                // font.pixelSize: 24
                anchors.verticalCenter: parent.verticalCenter
            }*/
        }

        Label {
            text: window.title
            font.pixelSize: 20
            font.bold: true
            anchors.fill: parent
            anchors.centerIn: parent
            elide: Label.ElideRight
            horizontalAlignment: Qt.AlignHCenter
            verticalAlignment: Qt.AlignVCenter
        }
    }

    Column {
        spacing: 10
        anchors.fill: parent

        Row {
            spacing: 10

            Button {
                text: "Tambah Dosen"
                onClicked: {
                    stackView.push("TambahPengajarPage.ui.qml")
                }
            }

            Button {
                text: "Hapus Dosen Terpilih"
                onClicked: {
                    stackView.push("TambahPengajarPage.ui.qml")
                }
            }
        }

        Rectangle {
            width: 50
            height: 50
            color: "red"
        }
        Rectangle {
            width: 50
            height: 50
            color: "green"
        }
        Rectangle {
            width: 50
            height: 50
            color: "blue"
        }

    }

    /*Component.onCompleted: {
        Qt.fontFamilies().indexOf("Material Icons") === -1 && Qt.application.fontDatabase.addApplicationFont("fonts/MaterialIcons-Regular.ttf")
    }*/
}
