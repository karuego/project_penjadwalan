import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

// import "../helpers/MaterialIcons.js" as MIcons
import "../components"
import "../helpers/Hari.js" as Hari
import "../helpers/String.js" as String
import Theme // qmllint disable import

Page {
    id: root
    title: "Daftar Pengajar"
    Material.theme: Material.Light
    // padding: 24
    // leftPadding: 16
    // rightPadding: 16

    property StackView stackViewRef
    property CustomDialog confirmDialogRef
    property CustomDialog alertDialogRef

    property var contextBridgeRef: contextBridge // qmllint disable unqualified
    property var pengajarModelRef: contextBridgeRef.pengajarModel
    property var pengajarProxyRef: contextBridgeRef.pengajarProxy

    // property string reloadMessage: "Memuat ulang database"
    // property var reloadFunc: () => pengajarModelRef.reload()

    ColumnLayout {
        id: mainContainer
        anchors.fill: parent

        Button {
            id: tambahDosen
            text: "Tambah Pengajar"

            Material.foreground: Material.Pink

            // width: 100
            // height: 55
            implicitHeight: 55
            Layout.alignment: Qt.AlignHCenter
            Layout.bottomMargin: 16

            background: Rectangle {
                radius: 8

                // Atur warna Rectangle agar berubah secara dinamis
                color: tambahDosen.down ? "#9c9c9c" : tambahDosen.hovered ? "#cccaca" : "#e0e0e0"

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
                root.stackViewRef.push("PengajarActionPage.qml");
            }
        }

        // QSortFilterProxyModel {
        //     id: fruitFilter
        //     sourceModel: fruitModel
        //     filterRegularExpression: RegExp(fruitSearch.text, "i")
        //     filterRole: 0 // needs to be set explicitly
        // }

        RowLayout {
            id: listTool
            implicitHeight: 55
            Layout.alignment: Qt.AlignVCenter
            Layout.fillWidth: true
            Layout.leftMargin: 16
            Layout.rightMargin: 16
            Layout.bottomMargin: 8

            property string selectedType: "semua"

            TextField {
                id: searchField
                placeholderText: "Cari pengajar..."
                Layout.fillWidth: true
                // onTextChanged: root.contextBridgeRef.pengajarProxy.setFilterText(text)
                onTextChanged: root.contextBridgeRef.pengajarModel.filter(text, listTool.selectedType)
            }

            Item {
                Layout.preferredWidth: 16
            }

            Label {
                text: "Filter :"
                font.pixelSize: 15
                Layout.alignment: Qt.AlignVCenter
            }

            // ButtonGroup {
            //     id: filterGroup
            //     buttons: opsiFilter.children

            //     onClicked: {
            //         const tipe = checkedButton.tipe; // qmllint disable

            //         /*if (tipe === "semua") {
            //             // Kirim string kosong untuk menghapus filter
            //             // root.contextBridgeRef.filterPengajar("");
            //             root.contextBridgeRef.pengajarProxy.filterPengajar("");
            //         } else {
            //             // root.contextBridgeRef.filterPengajar(tipe);
            //             root.contextBridgeRef.pengajarProxy.filterPengajar(tipe);
            //         }*/

            //         listTool.selectedType = tipe;
            //         root.contextBridgeRef.pengajarModel.filter(searchField.text, tipe);
            //     }
            // }

            // RowLayout {
            //     id: opsiFilter

            //     RadioButton {
            //         text: qsTr("Semua")
            //         checked: true
            //         property string tipe: "semua"
            //     }

            //     RadioButton {
            //         text: qsTr("Dosen")
            //         property string tipe: "dosen"
            //     }

            //     RadioButton {
            //         text: qsTr("Asisten Dosen")
            //         property string tipe: "asdos"
            //     }
            // }

            ComboBox {
                id: filterComboBox
                popup.closePolicy: Popup.CloseOnEscape
                popup.modal: false

                model: ListModel {
                    ListElement {
                        text: qsTr("Semua")
                        value: "semua"
                    }
                    ListElement {
                        text: qsTr("Dosen")
                        value: "dosen"
                    }
                    ListElement {
                        text: qsTr("Asisten Dosen")
                        value: "asdos"
                    }
                }

                textRole: "text"
                valueRole: "value"
                // currentIndex: 0
                // displayText: "Tipe: " + currentText

                // Saat item berubah, panggil function Python dari ContextBridge
                onActivated: {
                    // root.contextBridgeRef.filterPengajar("")
                    root.contextBridgeRef.pengajarModel.filter(searchField.text, currentValue);
                }
            }
        }

        // qmllint disable
        SortFilterProxyModel {
            id: proxy
            model: root.pengajarModelRef

            sorters: [
                // RoleSorter {
                //     roleName: "tipe"
                //     priority: 0
                //     sortOrder: Qt.AscendingOrder
                // },
                RoleSorter {
                    roleName: "nama"
                    priority: 1
                    sortOrder: Qt.AscendingOrder
                }
                // FunctionSorter {
                //     id: sortTipe
                //     function sort(lhsData: Pengajar, rhsData: Pengajar): int {
                //         return (lhsData.tipe < rhsData.tipe) ? -1 : ((lhsData === rhsData.tipe) ? 0 : 1);
                //     }
                // }
                // FunctionSorter {
                //     id: sortNama
                //     function sort(lhsData: Pengajar, rhsData: Pengajar): int {
                //         return (lhsData.nama > rhsData.nama) ? -1 : ((lhsData !== rhsData.nama) ? 0 : 1);
                //     }
                // }


            ]
            // filters: [
            //     FunctionFilter {
            //         id: functionSorter
            //         component TimeSlot: QtObject {
            //             property int id_
            //             property int hari
            //             property string mulai
            //             property string selesai
            //         }
            //         function filter(data: TimeSlot): bool {
            //             //return data.hari == 2
            //             return true;
            //         }
            //     }
            // ]
        }
        // qmllint enable

        Rectangle {
            id: rectangle
            Layout.fillWidth: true
            Layout.fillHeight: true
            border.color: "#cccccc"
            border.width: 1
            radius: 8

            ScrollView {
                id: scrollView
                anchors.fill: parent
                anchors.margins: 4

                ListView {
                    id: listView
                    // model: root.contextBridgeRef.pengajarProxyModel
                    // model: root.contextBridgeRef.pengajarModel
                    model: proxy
                    spacing: 8
                    clip: true
                    boundsBehavior: Flickable.StopAtBounds

                    delegate: ItemDelegate {
                        id: item
                        width: ListView.view.width
                        // padding: 16
                        padding: 0

                        required property int index
                        required property string id_
                        required property string nama
                        required property string tipe
                        required property string waktu

                        ColumnLayout {
                            width: parent.width
                            spacing: 0

                            RowLayout {
                                // width: parent.width

                                Layout.fillWidth: true
                                // Layout.topMargin: 16
                                Layout.leftMargin: 8
                                // Layout.rightMargin: 16

                                // Kolom untuk teks
                                ColumnLayout {
                                    // Layout.leftMargin: 8

                                    RowLayout {
                                        spacing: 8

                                        Label {
                                            id: nameLabel
                                            text: item.nama
                                            font.pixelSize: 18
                                            font.bold: true
                                        }

                                        Label {
                                            text: String.capitalizeFirstLetter(item.tipe)
                                            font.pixelSize: 11
                                            color: "#555"
                                            Layout.alignment: Qt.AlignTop
                                        }
                                    }

                                    RowLayout {
                                        Text {
                                            text: (item.tipe.toLowerCase() === "dosen" ? "NIDN" : "NIM  ") + " :"
                                            font.pixelSize: 13
                                        }

                                        Text {
                                            text: item.id_
                                            font.pixelSize: 13
                                            color: "#555"
                                        }

                                        Text {
                                            text: " | "
                                            font.pixelSize: 13
                                            // visible: item.waktu != ""
                                        }

                                        Text {
                                            text: "Pengecualian waktu: "
                                            font.pixelSize: 13
                                            // visible: item.waktu != ""
                                        }

                                        Label {
                                            text: Hari.parseHari(item.waktu).join(", ") || "--"
                                            font.pixelSize: 13
                                            color: "#555"
                                        }
                                    }
                                }

                                // Spacer untuk mendorong tombol ke kanan
                                Item {
                                    Layout.fillWidth: true
                                }

                                // Baris untuk tombol aksi
                                RowLayout {
                                    id: actionButton
                                    Layout.alignment: Qt.AlignRight
                                    Layout.rightMargin: 25

                                    IconButton {
                                        iconName: "visibility"
                                        iconColor: "#78A75A"
                                        // tooltipText: "Edit"

                                        onClicked: {
                                            root.gotoActionPage("view", item.id_); // qmllint disable unqualified
                                        }
                                    }

                                    IconButton {
                                        iconName: "edit"
                                        iconColor: "orange"
                                        // tooltipText: "Edit"

                                        onClicked: root.gotoActionPage("edit", item.id_) // qmllint disable unqualified
                                    }

                                    IconButton {
                                        iconName: "delete"
                                        iconColor: "red"
                                        // tooltipText: "Hapus"

                                        onClicked: {
                                            const message = `Apakah anda ingin menghapus pengajar: \nNama: ${item.nama}\nDeskripsi: ${item.tipe}`;

                                            root.confirmDialogRef.openWithCallback // qmllint disable unqualified
                                            (qsTr("Konfirmasi penghapusan pengajar"), message, () => {
                                                // root.contextBridgeRef.removePengajarFromIndex(item.index);
                                                const result = root.pengajarModelRef.removeById(item.id_);
                                                if (!result.success) {
                                                    console.error("Failed to delete pengajar");
                                                }
                                            }, null);
                                        }
                                    }
                                }
                            }

                            // Garis pemisah
                            Rectangle {
                                id: separator

                                Layout.topMargin: 4
                                Layout.fillWidth: true
                                Layout.preferredHeight: 1
                                color: "#e0e0e0"
                                // visible: item.index < (listView.count - 1) // qmllint disable unqualified
                            }
                        }

                        // // Aksi saat item di-klik
                        // onClicked: {
                        //     console.log("Anda menekan item:", item.productName);
                        // }
                    }
                }
            }
        }
    }

    function gotoActionPage(action, idn) {
        root.stackViewRef.push("PengajarActionPage.qml", {
            action: action,
            pengajarId: idn
        });
    }

    component TimeSlot: QtObject {
        property string id_
        property string nama
        property string tipe
        property string waktu
    }

    component Pengajar: QtObject {
        property string id_
        property string nama
        property string tipe
        property string waktu
    }
}
