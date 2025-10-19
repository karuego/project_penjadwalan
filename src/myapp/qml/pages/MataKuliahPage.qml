import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

import "../components"
// qmllint disable import
import Theme

Page {
    id: root
    title: "Daftar Mata Kuliah"
    Material.theme: Material.Light

    property StackView stackViewRef
    property CustomDialog confirmDialogRef

    // qmllint disable unqualified
    property var waktuModel: contextBridge.waktuModel
    // qmllint enable unqualified

    ColumnLayout {
        spacing: 10
        anchors.fill: parent

        Button {
            id: tambahMataKuliah
            text: "Tambah Mata Kuliah"
            onClicked: root.stackViewRef.push("TambahMataKuliahPage.qml")
            implicitHeight: 55
            Layout.alignment: Qt.AlignHCenter
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true

            border.color: "#cccccc"
            border.width: 1
            radius: 8

            ScrollView {
                anchors.fill: parent
                anchors.margins: 4

                ListView {
                    id: listView
                    spacing: 8
                    anchors.fill: parent
                    boundsBehavior: Flickable.StopAtBounds
                    clip: true

                    model: root.waktuModel

                    delegate: ItemDelegate {
                        id: item
                        width: ListView.view.width
                        // highlighted: ListView.isCurrentItem

                        required property int index
                        required property string hari
                        required property string jamMulai
                        required property string jamSelesai

                        Label {
                            id: hariLabel
                            text: item.hari
                            font.pixelSize: 18
                            font.bold: true
                        }

                        Label {
                            id: jamLabel
                            text: item.jamMulai + " - " + item.jamSelesai
                            anchors.top: hariLabel.bottom
                            anchors.topMargin: 2
                            font.pixelSize: 13
                            color: "#555"
                        }

                        IconButton {
                            iconName: "delete"
                            iconColor: "red"
                            // tooltipText: "Hapus"
                            anchors.right: parent.right
                            anchors.rightMargin: 16

                            onClicked: {
                                const message = `Apakah anda ingin menghapus waktu: \nHari: "${item.hari}".\nWaktu: ${item.jamMulai} - ${item.jamSelesai}"`;

                                // qmllint disable unqualified
                                root.confirmDialogRef.openWithCallback(qsTr("Konfirmasi penghapusan waktu"), message, function () {
                                    root.waktuModel.removeWaktu(index);
                                }, () => {});
                                // qmllint enable unqualified
                            }
                        }

                        // ScrollIndicator.vertical: ScrollIndicator { }
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
