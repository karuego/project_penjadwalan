import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material
import "../components"
import Theme

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

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        // Search Bar Sederhana
        RowLayout {
            Layout.fillWidth: true
            TextField {
                id: searchField
                placeholderText: "Cari Matkul / Pengajar..."
                Layout.fillWidth: true
                onTextChanged: {
                    jadwalModelRef.filter(text, root.type);
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
                        // Sembunyikan ID (0) dan Jenis (4)
                        if (column === 0 || column === 4)
                            return 0;

                        // Atur lebar kolom lainnya
                        if (column === 3)
                            return 200; // Matakuliah diperlebar
                        if (column === 10)
                            return 150; // Pengajar diperlebar

                        return 100; // Default lebar kolom lain (Hari, Jam, SKS, dll)
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
