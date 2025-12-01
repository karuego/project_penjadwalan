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
    property var contextBridgeRef: contextBridge
    property var jadwalModelRef: contextBridgeRef.jadwalModel

    property bool isLoading: false

    // --- KONEKSI KE PYTHON MODEL ---
    Connections {
        target: jadwalModelRef

        function onOptimizationProgress(iteration, cost) {
            // Update UI Realtime
            progressBar.value = iteration;
            statusLabel.text = "Iterasi: " + iteration + " | Konflik (Cost): " + cost.toFixed(2);
        }

        function onOptimizationFinished(success, message) {
            root.isLoading = false;
            busyIndicator.running = false;

            if (success) {
                statusLabel.text = "Selesai! " + message;
                progressBar.value = progressBar.to;

                // Aktifkan tombol lihat jadwal
                btnTeori.enabled = true;
                btnPraktek.enabled = true;

                // Tampilkan notifikasi (opsional)
                // snackbarRef.show(message)
            } else {
                statusLabel.text = "Error: " + message;
            }
        }
    }

    ColumnLayout {
        id: mainContainer
        anchors.fill: parent
        anchors.margins: 130
        spacing: 16

        Item {
            Layout.fillHeight: true
        }

        // --- BAGIAN KONTROL ---
        // RowLayout {
        //     Layout.fillWidth: true
        //     Label {
        //         text: "Periode akademik :"
        //         font.pixelSize: 15
        //     }
        //     ComboBox {
        //         id: comboBoxPeriode
        //         Layout.fillWidth: true
        //         model: ListModel {
        //             ListElement {
        //                 text: qsTr("Gasal")
        //                 value: "gasal"
        //             }
        //             ListElement {
        //                 text: qsTr("Genap")
        //                 value: "genap"
        //             }
        //         }
        //         textRole: "text"
        //         valueRole: "value"
        //     }
        // }

        RowLayout {
            Layout.fillWidth: true
            Item {
                width: 80
            }

            Button {
                text: root.isLoading ? "Sedang Memproses..." : "Buat Jadwal Otomatis"
                Layout.fillWidth: true
                enabled: !root.isLoading

                onClicked: {
                    root.isLoading = true;
                    busyIndicator.running = true;
                    progressBar.value = 0;
                    statusLabel.text = "Memulai algoritma...";

                    // Panggil fungsi Python
                    jadwalModelRef.startOptimization();
                }
            }
            Item {
                width: 80
            }
        }

        // --- PROGRESS BAR ---
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 5

            Label {
                id: statusLabel
                text: "Siap membuat jadwal"
                Layout.alignment: Qt.AlignHCenter
                color: "#666"
            }

            ProgressBar {
                id: progressBar
                Layout.fillWidth: true
                from: 0
                to: 10000 // Sesuaikan dengan max_iter di Python
                value: 0
            }
        }

        BusyIndicator {
            id: busyIndicator
            running: false
            visible: running
            Layout.alignment: Qt.AlignHCenter
        }

        // --- NAVIGASI HASIL ---
        ColumnLayout {
            Layout.fillWidth: true
            Layout.topMargin: 24

            Label {
                Layout.alignment: Qt.AlignHCenter
                text: "Lihat jadwal yang sudah dibuat :"
                font.pixelSize: 15
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.topMargin: 10

                Button {
                    id: btnTeori
                    text: "Jadwal Teori"
                    Layout.fillWidth: true
                    // enabled: true // Debugging: set true untuk test navigasi
                    onClicked: root.gotoActionPage("teori")
                }

                Button {
                    id: btnPraktek
                    text: "Jadwal Praktikum"
                    Layout.fillWidth: true
                    // enabled: true
                    onClicked: root.gotoActionPage("praktek")
                }
            }
        }

        Item {
            Layout.fillHeight: true
        }
    }

    function gotoActionPage(type) {
        root.stackViewRef.push("JadwalActionPage.qml", {
            type: type
        });
    }
}
