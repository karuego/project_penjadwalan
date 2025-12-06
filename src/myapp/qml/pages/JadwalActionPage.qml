import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Dialogs
import QtQuick.Layouts
import QtQuick.Window
import "../components"
import Theme
import Qt.labs.platform as Platform

Page {
    id: root
    title: "Jadwal " + (type == "teori" ? "Mata Kuliah" : "Praktikum")
    Material.theme: Material.Light

    required property string type // 'teori' atau 'praktek'

    property StackView stackViewRef
    property var contextBridgeRef: contextBridge
    property var jadwalModelRef: contextBridgeRef.jadwalModel

    // Saat halaman dimuat, filter data sesuai tipe
    Component.onCompleted: {
        jadwalModelRef.filter("", root.type);
    }

    FileDialog {
        id: fileDialog
        title: "Simpan Jadwal sebagai PDF"
        currentFolder: Platform.StandardPaths.writableLocation(Platform.StandardPaths.DocumentsLocation)
        fileMode: FileDialog.SaveFile
        nameFilters: ["PDF files (*.pdf)"]

        onAccepted: {
            // Panggil fungsi Python saat user menekan Save
            // selectedFile berisi URL (file:///...)
            jadwalModelRef.exportToPdf(selectedFile, root.type);
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        // Search Bar Sederhana
        RowLayout {
            Layout.fillWidth: true

            TextField {
                id: searchField
                placeholderText: "Cari Mata Kuliah / Pengajar..."
                Layout.fillWidth: true
                onTextChanged: {
                    jadwalModelRef.filter(text, root.type);
                }
            }

            // TOMBOL EKSPOR
            Button {
                text: "Ekspor PDF"
                icon.name: "document-save" // Jika menggunakan theme icon
                flat: false
                highlighted: true
                Material.background: Material.Green

                onClicked: {
                    // Set nama file default otomatis
                    var timestamp = new Date().toISOString().slice(0, 10);
                    fileDialog.currentFile = "Jadwal_" + root.type + "_" + timestamp + ".pdf";
                    fileDialog.open();
                }
            }
        }

        // --- TABLE VIEW (Diaktifkan) ---
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            border.color: "#cccccc"
            border.width: 1
            radius: 4

            ColumnLayout {
                anchors.fill: parent
                spacing: 0

                // Header Table
                HorizontalHeaderView {
                    id: headerView
                    syncView: tableView
                    Layout.fillWidth: true

                    clip: true

                    delegate: Rectangle {
                        color: "#f0f0f0"
                        implicitWidth: 120
                        implicitHeight: 40
                        border.color: "#ddd"
                        visible: width > 0

                        Text {
                            anchors.centerIn: parent
                            text: display
                            font.bold: true
                        }
                    }
                }

                // Body Table
                TableView {
                    id: tableView
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true

                    // Hubungkan ke Model
                    model: root.jadwalModelRef

                    // Konfigurasi Scroll
                    ScrollBar.vertical: ScrollBar {
                        policy: ScrollBar.AsNeeded
                    }
                    ScrollBar.horizontal: ScrollBar {
                        policy: ScrollBar.AsNeeded
                    }

                    // Lebar Kolom Manual (Bisa disesuaikan per indeks kolom jika mau)
                    columnWidthProvider: function (column) {
                        // switch (column) {
                        //     case 0:
                        //     case 4:  return 0;       // Sembunyikan ID (0) dan Jenis (4)
                        //     case 1:  return 50;      // Hari
                        //     case 3:  return 200;     // Mata Kuliah
                        //     case 5:  return 40;      // SKS
                        //     case 10: return 150;     // Pengajar
                        //     default: return 100;
                        // }

                        return {
                            0: 0      // Sembunyikan ID
                            ,
                            4: 0      // Sembunyikan Jenis
                            ,
                            1: 50     // Hari
                            ,
                            3: 200    // Mata Kuliah
                            ,
                            5: 0      // SKS
                            ,
                            10: 300     // Pengajar
                        }[column] ?? 100;
                    }

                    delegate: Rectangle {
                        implicitWidth: 100
                        implicitHeight: 40
                        border.color: "#eee"
                        color: row % 2 === 0 ? "white" : "#fafafa"

                        visible: width > 0

                        Text {
                            anchors.centerIn: parent
                            width: parent.width - 10
                            elide: Text.ElideRight
                            horizontalAlignment: Text.AlignHCenter
                            text: display // Mengambil data dari DisplayRole python
                            font.pixelSize: 13
                        }

                        // Tooltip jika teks kepotong
                        ToolTip.visible: ma.containsMouse
                        ToolTip.text: display
                        MouseArea {
                            id: ma
                            anchors.fill: parent
                            hoverEnabled: true
                        }
                    }
                }
            }
        }
    }
}
