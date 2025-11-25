import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material
import "../components"
import "../Theme"

Page {
    id: root
    title: "Pembuatan Jadwal"
    Material.theme: Material.Light

    property StackView stackViewRef
    property CustomDialog confirmDialogRef
    property CustomDialog alertDialogRef
    property Snackbar snackbarRef

    property var contextBridgeRef: contextBridge // qmllint disable unqualified
    property var jadwalModelRef: contextBridgeRef.jadwalModel

    // property string reloadMessage: "Memuat ulang database"
    // property var reloadFunc: () => matakuliahModelRef.reload()

    property bool isLoading: false

    ColumnLayout {
        id: mainContainer
        anchors.fill: parent
        anchors.margins: 130
        spacing: 0

        Item {
            Layout.fillHeight: true
        }

        RowLayout {
            id: listTool
            Layout.fillWidth: true

            Label {
                text: "Periode akademik :"
                font.pixelSize: 15
                Layout.alignment: Qt.AlignVCenter
            }

            ComboBox {
                id: comboBoxPeriode
                Layout.fillWidth: true

                model: ListModel {
                    ListElement {
                        text: qsTr("Gasal")
                        value: "gasal"
                    }
                    ListElement {
                        text: qsTr("Genap")
                        value: "genap"
                    }
                }

                textRole: "text"
                valueRole: "value"

                onActivated: {
                    //
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true

            Item {
                width: 80
            }

            Button {
                text: "Buat Jadwal"
                Layout.fillWidth: true
                onClicked: {
                    console.log(root.isLoading)
                    if (!isLoading) timer.start(), busyIndicator.running = true;
                    else timer.stop(), busyIndicator.running = false;
                    root.isLoading = !root.isLoading;
                }
            }

            Item {
                width: 80
            }
        }

        BusyIndicator {
            id: busyIndicator
            running: false
            Layout.fillWidth: true
        }

        Timer {
            id: timer
            interval: 2000
            onTriggered: {
                busyIndicator.running = false;
                btnTeori.enabled = true
                btnPraktek.enabled = true
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.topMargin: 16
            Layout.bottomMargin: 16

            Label {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter
                text: "Lihat jadwal yang sudah dibuat :"
                font.pixelSize: 15
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.topMargin: 16
                Layout.bottomMargin: 16

                Button {
                    id: btnTeori
                    text: "Lihat Jadwal Teori"
                    Layout.fillWidth: true
                    enabled: false
                    onClicked: root.stackViewRef.push("JadwalTeoriPage.qml")
                }

                Button {
                    id: btnPraktek
                    text: "Lihat Jadwal Praktek"
                    Layout.fillWidth: true
                    enabled: false
                    onClicked: root.stackViewRef.push("JadwalPraktekPage.qml")
                }
            }
        }

        TextField {
            id: customField
            placeholderText: "Fokus atau Hover"
            visible: false

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

        Item {
            Layout.fillHeight: true
        }
    }

    Component.onCompleted: {
        //
    }
}
