import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQml

import "../components"
import "../helpers/String.js" as String
import Theme // qmllint disable import

Page {
    id: root
    objectName: "ruanganPage"
    title: "Daftar Ruangan"

    // readonly property size textFieldSize: Qt.size(150, 55)

    property StackView stackViewRef
    property CustomDialog confirmDialogRef
    property CustomDialog alertDialogRef
    property Snackbar snackbarRef

    property var contextBridgeRef: contextBridge // qmllint disable unqualified
    property var ruanganModelRef: contextBridgeRef.ruanganModel

    property string reloadMessage: "Memuat ulang database..."
    property var reloadFunc: () => ruanganModelRef.reload()

    ColumnLayout {
        spacing: 10
        anchors.fill: parent

        RowLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter
            spacing: 32

            TextField {
                id: textFieldNama
                placeholderText: qsTr("Nama Ruangan")
                font.pixelSize: 13
                // Layout.fillWidth: true
                Layout.alignment: Qt.AlignVCenter
                background.implicitHeight: 50
                background.implicitWidth: 265
            }

            CheckBox {
                id: checkboxTipeLab
                text: qsTr("Laboratorium")
                font.pixelSize: 13
                Layout.alignment: Qt.AlignVCenter
            }

            Button {
                id: tambahWaktu
                text: qsTr("Tambah")
                Accessible.name: qsTr("Tambah Ruangan")
                Material.foreground: Material.Pink

                implicitWidth: 145
                implicitHeight: 55
                Layout.alignment: Qt.AlignVCenter
                Layout.bottomMargin: 16

                background: Rectangle {
                    radius: 8

                    // Atur warna Rectangle agar berubah secara dinamis
                    color: tambahWaktu.down ? "#9c9c9c" : tambahWaktu.hovered ? "#cccaca" : "#e0e0e0"

                    // border.color: "#adadad"
                    // border.width: 1

                    // Animasi halus untuk perubahan warna
                    Behavior on color {
                        ColorAnimation {
                            duration: 150
                        }
                    }
                }

                onClicked: {
                    const result = root.ruanganModelRef.add(textFieldNama.text, checkboxTipeLab.checked);
                    if (!result.success) {
                        root.alertDialogRef.openWithCallback("Peringatan", result.message, null, null);
                    } else {
                        root.snackbarRef.show(`Ruangan "${textFieldNama.text}" berhasil ditambahkan.`);
                        textFieldNama.text = "";
                        checkboxTipeLab.checked = false;
                    }
                }
            }
        }

        // qmllint disable
        SortFilterProxyModel {
            id: proxy
            model: root.ruanganModelRef
            sorters: [
                RoleSorter {
                    roleName: "nama"
                    priority: 0
                }
            ]
        }
        // qmllint enable

        Rectangle {
            id: kotakList
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

                    model: proxy

                    delegate: ItemDelegate {
                        id: item
                        width: ListView.view.width
                        // highlighted: ListView.isCurrentItem

                        required property int index
                        required property int id_
                        required property string nama
                        required property string tipe

                        RowLayout {
                            spacing: 8

                            Label {
                                id: nameLabel
                                text: item.nama
                                font.pixelSize: 18
                                font.bold: true
                            }

                            Label {
                                text: String.capitalizeFirstLetter(item.tipe === "praktek" ? "Laboratorium" : "")
                                font.pixelSize: 11
                                color: "#555"
                                Layout.alignment: Qt.AlignTop
                            }
                        }

                        IconButton {
                            iconName: "delete"
                            iconColor: "red"
                            // tooltipText: "Hapus"
                            anchors.right: parent.right
                            anchors.rightMargin: 16

                            onClicked: {
                                const message = `Apakah anda ingin menghapus ruangan: "${item.nama}"?`;

                                // qmllint disable unqualified
                                root.confirmDialogRef.openWithCallback(qsTr("Konfirmasi penghapusan ruangan"), message, function () {
                                    const result = root.ruanganModelRef.removeId(id_);
                                    if (!result.success) {
                                        root.alertDialogRef.openWithCallback("Peringatan", result.message, null, null);
                                    } else {
                                        root.snackbarRef.show(`Ruangan "${item.nama}" berhasil dihapus.`);
                                    }
                                }, () => {});
                                // qmllint enable unqualified
                            }
                        }
                    }
                }
            }
        }
    }
}
