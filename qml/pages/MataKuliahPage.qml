import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

import "../components"
import Theme

Page {
    title: "Daftar Mata Kuliah"

    ColumnLayout {
        spacing: 10
        anchors.fill: parent

        Button {
            id: tambahMataKuliah
            text: "Tambah Mata Kuliah"
            onClicked: stackView.push("TambahMataKuliahPage.qml")
            implicitHeight: 55
            Layout.alignment: Qt.AlignHCenter
        }

        Rectangle {
            // Gunakan Layout untuk mengatur ukuran dan posisi bingkai
            Layout.fillWidth: true
            Layout.fillHeight: true

            // 2. Atur properti border
            border.color: "#cccccc" // Warna garis border
            border.width: 1        // Ketebalan garis border
            radius: 8              // (Opsional) Buat sudutnya membulat

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
                    // Setiap item akan mengisi lebar ListView
                    width: parent.width

                    // 'model' adalah variabel khusus di dalam delegate
                    // yang berisi data untuk baris saat ini.
                    // Kita akses properti dari ListElement melalui 'model'.

                    Label {
                        id: nameLabel
                        text: model.productName
                        font.pixelSize: 18
                        font.bold: true
                    }

                    Label {
                        text: model.productDescription
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
                        onClicked: { console.log("Anda menghapus item:", model.productName) }
                    }

                    onClicked: {
                        console.log("Anda menekan item:", model.productName)
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
