import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

import "../components"
import "../helpers/Hari.js" as Hari
import "../helpers/String.js" as String
import Theme // qmllint disable import

Page {
    id: root
    title: "Jadwal " + (type == "teori" ? "Mata Kuliah" : "Praktikum")
    Material.theme: Material.Light

    property StackView stackViewRef
    property CustomDialog confirmDialogRef
    property CustomDialog alertDialogRef
    property Snackbar snackbarRef

    property var contextBridgeRef: contextBridge // qmllint disable unqualified
    property var jadwalModelRef: contextBridgeRef.jadwalModel

    // property string reloadMessage: "Memuat ulang database"
    // property var reloadFunc: () => matkulModelRef.reload()

    required property string type

    // Label {
    //     text: "Under construction"
    // }

    ColumnLayout {
        id: mainContainer
        anchors.fill: parent
        anchors.margins: 10
        spacing: 0 // Rapatkan header dengan body tabel

        // QSortFilterProxyModel {
        //     id: matkulFilter
        //     sourceModel: matModel
        //     filterRegularExpression: RegExp(fruitSearch.text, "i")
        //     filterRole: 0 // needs to be set explicitly
        // }

        // RowLayout {
        //     id: listTool
        //     implicitHeight: 55
        //     Layout.alignment: Qt.AlignVCenter
        //     Layout.fillWidth: true
        //     Layout.leftMargin: 16
        //     Layout.rightMargin: 16
        //     Layout.bottomMargin: 8

        //     property string selectedType: "semua"

        //     TextField {
        //         id: searchField
        //         placeholderText: "Cari mata kuliah..."
        //         Layout.fillWidth: true
        //         onTextChanged: root.contextBridgeRef.matakuliahModel.filter(text, listTool.selectedType)
        //     }

        //     // Item {
        //     //     Layout.preferredWidth: 16
        //     // }

        //     // Label {
        //     //     text: "Filter :"
        //     //     font.pixelSize: 15
        //     //     Layout.alignment: Qt.AlignVCenter
        //     // }

        //     // ButtonGroup {
        //     //     id: filterGroup
        //     //     buttons: opsiFilter.children

        //     //     onClicked: {
        //     //         const tipe = checkedButton.tipe; // qmllint disable

        //     //         /*if (tipe === "semua") {
        //     //             // Kirim string kosong untuk menghapus filter
        //     //             // root.contextBridgeRef.filterPengajar("");
        //     //             root.contextBridgeRef.pengajarProxy.filterPengajar("");
        //     //         } else {
        //     //             // root.contextBridgeRef.filterPengajar(tipe);
        //     //             root.contextBridgeRef.pengajarProxy.filterPengajar(tipe);
        //     //         }*/

        //     //         listTool.selectedType = tipe;
        //     //         root.contextBridgeRef.pengajarModel.filter(searchField.text, tipe);
        //     //     }
        //     // }

        //     // RowLayout {
        //     //     id: opsiFilter

        //     //     RadioButton {
        //     //         text: qsTr("Semua")
        //     //         checked: true
        //     //         property string tipe: "semua"
        //     //     }

        //     //     RadioButton {
        //     //         text: qsTr("Dosen")
        //     //         property string tipe: "dosen"
        //     //     }

        //     //     RadioButton {
        //     //         text: qsTr("Asisten Dosen")
        //     //         property string tipe: "asdos"
        //     //     }
        //     // }

        //     // ComboBox {
        //     //     id: filterComboBox
        //     //     popup.closePolicy: Popup.CloseOnEscape
        //     //     popup.modal: false

        //     //     model: ListModel {
        //     //         ListElement {
        //     //             text: qsTr("Semua")
        //     //             value: "semua"
        //     //         }
        //     //         ListElement {
        //     //             text: qsTr("Teori")
        //     //             value: "teori"
        //     //         }
        //     //         ListElement {
        //     //             text: qsTr("Praktikum")
        //     //             value: "praktek"
        //     //         }
        //     //     }

        //     //     textRole: "text"
        //     //     valueRole: "value"
        //     //     // currentIndex: 0
        //     //     // displayText: "Tipe: " + currentText

        //     //     // Saat item berubah, panggil function Python dari ContextBridge
        //     //     onActivated: {
        //     //         // root.contextBridgeRef.filterPengajar("")
        //     //         root.contextBridgeRef.matakuliahModel.filter(searchField.text, currentValue);
        //     //     }
        //     // }
        // }

        // qmllint disable
        // SortFilterProxyModel {
        //     id: proxy
        //     model: root.matkulModelRef

        //     sorters: [
        //         // RoleSorter {
        //         //     roleName: "tipe"
        //         //     priority: 0
        //         //     sortOrder: Qt.AscendingOrder
        //         // },
        //         RoleSorter {
        //             roleName: "nama"
        //             priority: 1
        //             sortOrder: Qt.AscendingOrder
        //         }
        //         // FunctionSorter {
        //         //     id: sortTipe
        //         //     function sort(lhsData: Pengajar, rhsData: Pengajar): int {
        //         //         return (lhsData.tipe < rhsData.tipe) ? -1 : ((lhsData === rhsData.tipe) ? 0 : 1);
        //         //     }
        //         // }
        //         // FunctionSorter {
        //         //     id: sortNama
        //         //     function sort(lhsData: Pengajar, rhsData: Pengajar): int {
        //         //         return (lhsData.nama > rhsData.nama) ? -1 : ((lhsData !== rhsData.nama) ? 0 : 1);
        //         //     }
        //         // }


        //     ]
        //     // filters: [
        //     //     FunctionFilter {
        //     //         id: functionSorter
        //     //         component TimeSlot: QtObject {
        //     //             property int id_
        //     //             property int hari
        //     //             property string mulai
        //     //             property string selesai
        //     //         }
        //     //         function filter(data: TimeSlot): bool {
        //     //             //return data.hari == 2
        //     //             return true;
        //     //         }
        //     //     }
        //     // ]
        // }
        // qmllint enable

        // Rectangle {
        //     id: rectangle
        //     Layout.fillWidth: true
        //     Layout.fillHeight: true
        //     border.color: "#cccccc"
        //     border.width: 1
        //     radius: 8

        //     ScrollView {
        //         id: scrollView
        //         anchors.fill: parent
        //         anchors.margins: 4
        //         spacing: 0 // Rapatkan header dengan body tabel

                // --- 1. Header Tabel (Judul Kolom) ---
                HorizontalHeaderView {
                    id: headerView
                    syncView: tableView // Sambungkan scrolling header dengan tabel
                    Layout.fillWidth: true

                    // Opsional: Styling Header
                    delegate: Rectangle {
                        color: "#ddd"
                        implicitWidth: 100
                        implicitHeight: 30
                        border.color: "gray"

                        Text {
                            anchors.centerIn: parent
                            text: display // Mengambil data dari method 'headerData' Python
                            font.bold: true
                        }
                    }
                }

                // --- 2. Isi Tabel ---
                TableView {
                    id: tableView
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true // Supaya teks tidak tembus keluar kotak

                    // boundsBehavior: Flickable.StopAtBounds

                    model: root.jadwalModelRef

                    // Atur lebar kolom (bisa manual atau otomatis)
                    columnWidthProvider: function (column) {
                        return 100; // Semua kolom lebar 100px
                    }

                    // --- DELEGATE (Tampilan per Sel) ---
                    delegate: Rectangle {
                        id: item
                        // width: ListView.view.width
                        // padding: 16
                        // padding: 0

                        implicitWidth: 100
                        implicitHeight: 40
                        border.color: "#eee"

                        // required property int index
                        // required property int id_
                        // required property string hari
                        // required property string jam
                        // required property string matakuliah
                        // required property string tipe
                        // required property int sks
                        // required property int semester
                        // required property string kelas
                        // required property string ruangan
                        // required property bool daring
                        // required property string pengajar

                        // Warna selang-seling (Zebra striping)
                        color: row % 2 === 0 ? "white" : "#f9f9f9"

                        Text {
                            anchors.centerIn: parent
                            // 'display' adalah keyword otomatis untuk mengambil
                            // data dari role 'DisplayRole' di Python
                            text: display
                        }
                    }

                    // Scrollbar (Opsional)
                    ScrollBar.vertical: ScrollBar {}
                    ScrollBar.horizontal: ScrollBar {}
                }
        //     }
        // }
    }
}
