import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material
import QtQml.Models

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
                root.stackViewRef.push("DetailPengajarPage.qml");
            }
        }

        ListModel {
            id: fruitModel
            ListElement {
                name: "Apple"
                color: "green"
            }
            ListElement {
                name: "Cherry"
                color: "red"
            }
            ListElement {
                name: "Banana"
                color: "yellow"
            }
            ListElement {
                name: "Orange"
                color: "orange"
            }
            ListElement {
                name: "WaterMelon"
                color: "pink"
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
                placeholderText: "Cari pengajar (bisa regex)..."
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
                model: ["Semua", "Dosen", "Asisten dosen"]

                // Saat pilihan berubah, panggil slot Python dari ContextBridge
                onCurrentTextChanged: {
                    if (currentText === model[2])
                        // Kirim string kosong untuk menghapus filter
                        // root.contextBridgeRef.filterPengajar("");
                        root.contextBridgeRef.pengajarModel.filter(searchField.text, "asdos");
                    else
                        root.contextBridgeRef.pengajarModel.filter(searchField.text, currentText);
                }
            }
        }

        Rectangle {
            id: rectangle

            // Gunakan Layout untuk mengatur ukuran dan posisi bingkai
            Layout.fillWidth: true
            Layout.fillHeight: true

            // 2. Atur properti border
            border.color: "#cccccc" // Warna garis border
            border.width: 1        // Ketebalan garis border
            radius: 8              // (Opsional) Buat sudutnya membulat

            ScrollView {
                id: scrollView
                anchors.fill: parent
                anchors.margins: 4

                ListView {
                    id: listView
                    // model: root.contextBridgeRef.pengajarProxyModel
                    model: root.contextBridgeRef.pengajarModel
                    spacing: 8
                    clip: true

                    boundsBehavior: Flickable.StopAtBounds

                    // anchors.fill: parent // ListView mengisi seluruh area di dalam bingkai
                    // PENTING: Gunakan properti Layout, bukan anchors
                    //Layout.fillWidth: true  // Buat ListView mengisi lebar kolom
                    //Layout.fillHeight: true // Buat ListView mengisi sisa tinggi kolom
                    // implicitHeight: contentHeight

                    // Kurangi jeda sebelum scroll dimulai.
                    // Nilai defaultnya cukup tinggi. Coba atur ke 0 atau nilai kecil seperti 20.
                    // pressDelay: 0

                    // Atur seberapa cepat laju scroll melambat setelah di-flick.
                    // Nilai default: 1500. Nilai lebih rendah = lebih licin.
                    // flickDeceleration: 1000

                    // Tambahkan WheelHandler untuk mengontrol scroll dari touchpad/mouse wheel
                    /*WheelHandler {
                        // Properti custom untuk mengatur kecepatan, agar mudah diubah.
                        // Coba nilai antara 1.5 hingga 3.0 untuk merasakan perbedaannya.
                        property real speedMultiplier: 50.0

                        // Handler ini akan aktif setiap kali ada event scroll dari touchpad/wheel
                        onWheel: (event) => {
                            // Ambil nilai pergerakan vertikal dari touchpad (event.pixelDelta.y)
                            // dan kalikan dengan pengali kecepatan kita.
                            let scrollAmount = event.pixelDelta.y * speedMultiplier;

                            // Ubah posisi konten ListView secara manual.
                            listView.contentY += scrollAmount;

                            // Beritahu sistem bahwa kita sudah menangani event ini.
                            // Ini mencegah Flickable melakukan scroll default-nya (menghindari double scroll).
                            event.accepted = true;
                        }
                    }*/

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

                            // Bagian konten (teks dan tombol)
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
                                            text: Hari.fromNumberToJoinedText(item.waktu) || "--"
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
                                            root.stackViewRef.push// qmllint disable unqualified
                                            ("DetailPengajarPage.qml", {
                                                action: "view",
                                                pengajarId: item.id_
                                            });
                                        }
                                    }

                                    IconButton {
                                        iconName: "edit"
                                        iconColor: "orange"
                                        // tooltipText: "Edit"

                                        onClicked: {
                                            root.stackViewRef.push// qmllint disable unqualified
                                            ("DetailPengajarPage.qml", {
                                                action: "edit",
                                                pengajarId: item.id_
                                            });
                                        }
                                    }

                                    IconButton {
                                        iconName: "delete"
                                        iconColor: "red"
                                        // tooltipText: "Hapus"

                                        onClicked: {
                                            const message = `Apakah anda ingin menghapus pengajar: \nNama: ${item.nama}\nDeskripsi: ${item.tipe}`;

                                            root.confirmDialogRef.openWithCallback // qmllint disable unqualified
                                            (qsTr("Konfirmasi penghapusan pengajar"), message, () => {
                                                root.contextBridgeRef.removePengajarFromIndex(item.index);
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
}
