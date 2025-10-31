import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import "../components"
import "../Theme"

Page {
    id: root
    title: "Pembuatan Jadwal"

    property StackView stackViewRef
    property CustomDialog confirmDialogRef

    Column {
        spacing: 10
        anchors.fill: parent

        Button {
            text: "Lihat Jadwal Teori"
            onClicked: root.stackViewRef.push("JadwalTeoriPage.qml")
        }

        Button {
            text: "Lihat Jadwal Praktek"
            onClicked: root.stackViewRef.push("JadwalPraktekPage.qml")
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
                    height: isActive ? 2 : 1
                    color: isActive ? Material.accent : "#888"
                    anchors.bottom: parent.bottom

                    Behavior on color {
                        ColorAnimation {
                            duration: 200
                        }
                    }
                    Behavior on height {
                        NumberAnimation {
                            duration: 200
                        }
                    }
                }
            }
        }

        BusyIndicator {
            id: busyIndicator
            running: true

            Label {
                id: helpLabel
                text: "help"
                font.pixelSize: 24
                font.family: AppTheme.materialFont
                visible: false
            }
        }

        Timer {
            id: timer
            interval: 2000
            onTriggered: {
                busyIndicator.running = false;
                helpLabel.visible = true;
            }
        }
    }

    Component.onCompleted: {
        timer.start();
    }
}
