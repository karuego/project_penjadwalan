import QtQuick
import QtQuick.Window
import QtQuick.Effects
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material
import "../components"

Page {
    title: "Pembuatan Jadwal"

    Column {
        spacing: 10
        anchors.fill: parent

        Button {
            text: "Lihat Jadwal Teori"
            onClicked: stackView.push("JadwalTeoriPage.qml")
        }

        Button {
            text: "Lihat Jadwal Praktek"
            onClicked: stackView.push("JadwalPraktekPage.qml")
        }



        TextField {
            id: customField
            placeholderText: "Fokus atau Hover"

            background: Rectangle {
                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                }


                Rectangle {
                    property bool isActive: customField.activeFocus || mouseArea.containsMouse

                    width: parent.width
                    // Gunakan properti 'isActive'
                    height: isActive ? 2 : 1
                    color: isActive ? Material.accent : "#888"
                    anchors.bottom: parent.bottom

                    Behavior on color { ColorAnimation { duration: 200 } }
                    Behavior on height { NumberAnimation { duration: 200 } }
                }
            }
        }


    }
}
