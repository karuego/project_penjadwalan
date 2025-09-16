import QtQuick
import QtQuick.Window
import QtQuick.Dialogs
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

import "../components"
import Theme

Page {
    id: root
    title: "Daftar Waktu"

    // readonly property size textFieldSize: Qt.size(150, 55)

    ColumnLayout {
        spacing: 10
        anchors.fill: parent

        Row {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter
            spacing: 32

            Column {
                id: inputWaktu
                anchors.bottom: parent.bottom

                Label { text: "Hari" }

                ComboBox {
                    id: comboBoxHari
                    model: ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
                    onCurrentValueChanged: {
                        spinMulaiJam.value = 8
                        spinMulaiMenit.value = 0
                    }
                }
            }

            Column {
                Label { text: "Waktu Mulai" }

                RowLayout {
                    /*CustomSpinner {
                        id: hourSpinner
                        from: 0
                        to: 23
                    }*/

                    SpinBox {
                        id: spinMulaiJam
                        from: 0
                        to: 23
                        value: 8
                        editable: true
                        // focus: true
                        onValueChanged: root.hitungDurasi()
                    }

                    SpinBox {
                        id: spinMulaiMenit
                        from: 0
                        to: 59
                        value: 0
                        editable: true
                        // focus: true
                        onValueChanged: root.hitungDurasi()
                    }
                }
            }

            Column {
                spacing: 8

                Label {
                    text: "Waktu Selesai"
                }

                RowLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.alignment: Qt.AlignVCenter

                    property int fontSize: 35

                    Label {
                        id: labelSelesaiJam
                        text: "08"
                        font.bold: true
                        font.pixelSize: parent.fontSize
                    }

                    Label {
                        text: ":"
                        font.bold: true
                        font.pixelSize: parent.fontSize
                    }

                    Label {
                        id: labelSelesaiMenit
                        text: "45"
                        font.bold: true
                        font.pixelSize: parent.fontSize
                    }
                }
            }

            Button {
                id: tambahWaktu
                text: qsTr("Tambah")
                Accessible.name: qsTr("Tambah Waktu Kuliah")
                Material.foreground: Material.Pink

                // width: 100
                // Layout.fillWidth: true
                implicitWidth: 145
                // height: 55
                // implicitHeight: 60
                implicitHeight: 65
                // Layout.alignment: Qt.AlignHCenter
                // Layout.bottomMargin: 16

                anchors.bottom: parent.bottom

                background: Rectangle {
                    radius: 8

                    // Atur warna Rectangle agar berubah secara dinamis
                    color: tambahWaktu.down ? "#9c9c9c" : tambahWaktu.hovered ? "#cccaca" : "#e0e0e0"

                    // border.color: "#adadad"
                    // border.width: 1

                    // Animasi halus untuk perubahan warna
                    Behavior on color { ColorAnimation { duration: 150 } }
                }

                onClicked: {
                    if (spinMulaiJam.value >= 23 && spinMulaiMenit.value >= 0) {
                        spinMulaiJam.value = 0
                        spinMulaiMenit.value = 0
                    } else {
                        spinMulaiJam.value = labelSelesaiJam.text
                        spinMulaiMenit.value = labelSelesaiMenit.text
                    }
                }
            }
        }

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
                    clip: true
                    model: waktuModel

                    delegate: ItemDelegate {
                        id: item
                        width: parent.width
                        highlighted: ListView.isCurrentItem

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
                                console.log(
                                    `Anda menghapus item: "${hariLabel.text}: ${jamLabel.text}"`
                                )

                                confirmDialog.openWithText(`Hapus waktu: "${hariLabel.text}: ${jamLabel.text}"`)
                            }
                        }

                        onClicked: {
                            console.log("Anda menekan item:", index, ":", hari)
                        }

                        // ScrollIndicator.vertical: ScrollIndicator { }
                    }
                }
            }
        }
    }

    ListModel {
        id: waktuModel

        ListElement {
            hari: "Senin"
            jamMulai: "08:00"
            jamSelesai: "09:30"
        }
        ListElement {
            hari: "Senin"
            jamMulai: "09:35"
            jamSelesai: "11:05"
        }
        ListElement {
            hari: "Senin"
            jamMulai: "11:10"
            jamSelesai: "12:50"
        }
        ListElement {
            hari: "Senin"
            jamMulai: "12:55"
            jamSelesai: "09:30"
        }
        ListElement {
            hari: "Senin"
            jamMulai: "08:00"
            jamSelesai: "09:30"
        }
        ListElement {
            hari: "Senin"
            jamMulai: "08:00"
            jamSelesai: "09:30"
        }
        ListElement {
            hari: "Senin"
            jamMulai: "08:00"
            jamSelesai: "09:30"
        }
        ListElement {
            hari: "Senin"
            jamMulai: "08:00"
            jamSelesai: "09:30"
        }
    }

    Dialog {
        id: confirmDialog
        title: qsTr("Konfirmasi penghapusan item")
        modal: true // Mencegah interaksi dengan window di belakangnya
        anchors.centerIn: parent
        standardButtons: Dialog.Ok | Dialog.Cancel

        // signal accepted
        // signal rejected
        // onAccepted: accepted()
        // onRejected: rejected()
        onAccepted: console.log("Ok clicked")
        onRejected: console.log("Cancel clicked")

        Label {
            id: msgLabel
            text: qsTr("Hapus item ....?")
            wrapMode: Text.WordWrap
        }

        function openWithText(message) {
            msgLabel.text = message
            open()
        }
    }

    function hitungDurasi() {
        const durasi = 45

        const mulaiJam = spinMulaiJam.value
        const mulaiMenit = spinMulaiMenit.value

        const waktuMulai = (mulaiJam * 60) + mulaiMenit
        // const start_h = Math.floor(waktuMulai / 60)
        // const start_m = waktuMulai % 60

        const waktuSelesai = waktuMulai + durasi
        const end_h = Math.floor(waktuSelesai / 60)
        const end_m = waktuSelesai % 60

        //const duaDigit = v => v < 10 ? "0" + v : v
        const duaDigit = v => v.toString().padStart(2, '0')

        labelSelesaiJam.text = duaDigit(end_h)
        labelSelesaiMenit.text = duaDigit(end_m)
    }
}
