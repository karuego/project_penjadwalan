import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

// import "../helpers"
import "../helpers/MaterialIcons.js" as MIcons
import "../components"
import Theme

Page {
    id: pagePengajar
    title: "Daftar Pengajar"
    Material.theme: Material.Light
    // padding: 24
    // leftPadding: 16
    // rightPadding: 16

    ColumnLayout {
        anchors.fill: parent

        Button {
            id: tambahDosen
            text: "Tambah Pengajar"
            onClicked: stackView.push("TambahPengajarPage.qml")

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
                Behavior on color { ColorAnimation { duration: 150 } }
            }
        }

        Rectangle {
            // Gunakan Layout untuk mengatur ukuran dan posisi bingkai
            Layout.fillWidth: true
            Layout.fillHeight: true

            // 2. Atur properti border
            border.color: "#cccccc" // Warna garis border
            border.width: 1        // Ketebalan garis border
            radius: 8              // (Opsional) Buat sudutnya membulat

            ScrollView {
                anchors.fill: parent
                anchors.margins: 4

                ListView {
                    id: listView
                    model: productModel
                    spacing: 8

                    // PENTING: Agar item tidak "bocor" keluar dari sudut bulat
                    clip: true

                    // anchors.fill: parent // ListView mengisi seluruh area di dalam bingkai
                    // PENTING: Gunakan properti Layout, bukan anchors
                    Layout.fillWidth: true  // Buat ListView mengisi lebar kolom
                    Layout.fillHeight: true // Buat ListView mengisi sisa tinggi kolom
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

                    // Delegate ini akan dibuat ulang untuk setiap item di dalam model.
                    delegate: ItemDelegate {
                        width: parent.width // Buat setiap item mengisi lebar ListView

                        // 'model' adalah variabel khusus di dalam delegate
                        // yang berisi data untuk baris saat ini.
                        // Kita akses properti dari ListElement melalui 'model'.

                        // Teks besar (Judul)
                        Label {
                            id: nameLabel
                            text: model.productName // Ambil 'productName' dari model
                            font.pixelSize: 18
                            font.bold: true
                        }

                        // Teks kecil (Deskripsi)
                        Label {
                            text: model.productDescription // Ambil 'productDescription' dari model
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
                            anchors.rightMargin: 15
                            onClicked: {
                                console.log("Anda menghapus item:", model.productName)
                            }
                        }

                        // Aksi saat item di-klik
                        onClicked: {
                            console.log("Anda menekan item:", model.productName)
                        }
                    }
                }
            }
        }
    }


    // Setiap ListElement adalah satu item dalam daftar.
    ListModel {
        id: productModel

        ListElement {
            productName: "Pengajar 1"
            productDescription: "Preferensi: ~"
        }
        ListElement {
            productName: "Mouse Gaming RGB"
            productDescription: "Stok: 42 unit - 12000 DPI"
        }
        ListElement {
            productName: "Keyboard Mekanikal"
            productDescription: "Stok: 21 unit - Switch Biru"
        }
        ListElement {
            productName: "Monitor 27-inch 4K"
            productDescription: "Stok: 8 unit - 144Hz, HDR"
        }
        ListElement {
            productName: "Webcam HD 1080p"
            productDescription: "Stok: 35 unit - Dengan mikrofon"
        }

        ListElement {
            productName: "Webcam HD 1081p"
            productDescription: "Stok: 35 unit - Dengan mikrofon"
        }
        ListElement {
            productName: "Webcam HD 1082p"
            productDescription: "Stok: 35 unit - Dengan mikrofon"
        }
        ListElement {
            productName: "Webcam HD 1083p"
            productDescription: "Stok: 35 unit - Dengan mikrofon"
        }
        ListElement {
            productName: "Webcam HD 1084p"
            productDescription: "Stok: 35 unit - Dengan mikrofon"
        }
        ListElement {
            productName: "Webcam HD 1085p"
            productDescription: "Stok: 35 unit - Dengan mikrofon"
        }
        ListElement {
            productName: "Webcam HD 1086p"
            productDescription: "Stok: 35 unit - Dengan mikrofon"
        }
        ListElement {
            productName: "Webcam HD 1087p"
            productDescription: "Stok: 35 unit - Dengan mikrofon"
        }
        ListElement {
            productName: "Webcam HD 1088p"
            productDescription: "Stok: 35 unit - Dengan mikrofon"
        }
        ListElement {
            productName: "Webcam HD 1089p"
            productDescription: "Stok: 35 unit - Dengan mikrofon"
        }
        ListElement {
            productName: "Webcam HD 10810p"
            productDescription: "Stok: 35 unit - Dengan mikrofon"
        }
    }
}
