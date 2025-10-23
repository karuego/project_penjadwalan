import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

import "../components"
// qmllint disable import
import Theme

Page {
    title: "Daftar Ruangan"

    property StackView stackViewRef
    property CustomDialog confirmDialogRef
    property CustomDialog alertDialogRef

    property var contextBridgeRef: contextBridge // qmllint disable unqualified
    property var ruangModelRef: contextBridgeRef.ruangModel
    property var ruangProxyRef: contextBridgeRef.ruangProxy

    // property string reloadMessage: "Memuat ulang database"
    // property var reloadFunc: () => ruangModelRef.reload()

    RowLayout {
        spacing: 10
        anchors.fill: parent

        ColumnLayout {
            // Layout.alignment: Qt.AlignLeft
            Layout.preferredWidth: parent.width / 2.5

            RowLayout {
                // implicitHeight: 42
                // implicitWidth: 300
                Layout.alignment: Qt.AlignLeft

                Label {
                    text: "Nama Ruangan :"
                    // font.pixelSize: 24
                    color: "#2ecc71"
                }

                Rectangle {
                    // Layout.fillWidth: true
                    // Layout.fillHeight: true
                    Layout.preferredWidth: 200
                    implicitHeight: inputNama.height

                    color: "#f0f0f0"
                    border.color: "gray"
                    // border.width: 1
                    // radius: 8

                    /*Text {
                        id: placeholder
                        text: "Ketik sesuatu di sini..."
                        color:"gray"
                        font.italic: true
                        anchors.fill: parent
                        anchors.leftMargin: 4
                        verticalAlignment: Text.AlignVCenter
                        visible: !inputNama.length && !inputNama.activeFocus
                    }*/

                    TextInput {
                        id: inputNama
                        text: "asd"
                        width: 200
                        height: 42
                        clip: true
                        anchors.fill: parent

                        // onTextChanged: {
                        //     display.text = "Halo, " + this.text;
                        // }
                    }
                }
            }

            Button {
                text: "Simpan"
                onClicked:
                // stackView.pop()
                {}
            }
        }

        ColumnLayout {
            // Layout.alignment: Qt.AlignRight
            // Layout.preferredWidth: parent.width / 2 + 500

            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true

                border.color: "#cccccc"
                border.width: 1
                radius: 8

                ListView {
                    id: listView
                    model: productModel
                    anchors.margins: 8
                    spacing: 5
                    anchors.fill: parent
                    clip: true

                    // PENTING: Gunakan properti Layout, bukan anchors
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    // Delegate ini akan dibuat ulang untuk setiap item di dalam model.
                    delegate: ItemDelegate {
                        id: item
                        // Setiap item akan mengisi lebar ListView
                        width: parent.width

                        required property int index
                        required property string productName
                        required property string productDescription

                        Label {
                            id: nameLabel
                            text: item.productName
                            font.pixelSize: 18
                            font.bold: true
                        }

                        Label {
                            text: item.productDescription
                            anchors.top: nameLabel.bottom // Posisikan di bawah teks besar
                            anchors.topMargin: 2
                            font.pixelSize: 13
                            color: "#555"
                        }

                        IconButton {
                            iconName: "delete"
                            iconColor: "red"
                            // tooltipText: "Hapus"
                            anchors.right: parent.right
                            onClicked: {
                                console.log("Anda menghapus item:", item.productName);
                            }
                        }

                        onClicked: {
                            console.log("Anda menekan item:", item.productName);
                        }
                    }
                }
            }
        }
    }

    ListModel {
        id: productModel

        ListElement {
            productName: "Mata Kuliah 1"
            productDescription: "Dosen 1"
        }
        ListElement {
            productName: "Mata Kuliah 2"
            productDescription: "Dosen 2"
        }
        ListElement {
            productName: "Mata Kuliah 3"
            productDescription: "Dosen 3"
        }
        ListElement {
            productName: "Mata Kuliah 4"
            productDescription: "Dosen 4"
        }
        ListElement {
            productName: "Mata Kuliah 5"
            productDescription: "Dosen 5"
        }
        ListElement {
            productName: "Mata Kuliah 6"
            productDescription: "Dosen 6"
        }
        ListElement {
            productName: "Mata Kuliah 7"
            productDescription: "Dosen 7"
        }
        ListElement {
            productName: "Mata Kuliah 8"
            productDescription: "Dosen 8"
        }
        ListElement {
            productName: "Mata Kuliah 9"
            productDescription: "Dosen 9"
        }
        ListElement {
            productName: "Mata Kuliah 10"
            productDescription: "Dosen 10"
        }
        ListElement {
            productName: "Mata Kuliah 11"
            productDescription: "Dosen 11"
        }
    }
}
