import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

import "../components"
import Theme // qmllint disable import

Page {
    id: root
    title: "Daftar Waktu"

    // readonly property size textFieldSize: Qt.size(150, 55)

    property StackView stackViewRef
    property CustomDialog confirmDialogRef
    property CustomDialog alertDialogRef

    property var waktuModelRef: contextBridge.waktuModel // qmllint disable unqualified

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

                Label {
                    text: "Hari"
                }

                ComboBox {
                    id: comboBoxHari
                    model: ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
                    onCurrentValueChanged: {
                        spinMulaiJam.value = 8;
                        spinMulaiMenit.value = 0;
                    }
                }
            }

            Column {
                Label {
                    text: "Waktu Mulai"
                }

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
                    Behavior on color {
                        ColorAnimation {
                            duration: 150
                        }
                    }
                }

                onClicked: {
                    const jamMulaiStr = spinMulaiJam.value.toString().padStart(2, '0') + ":" + spinMulaiMenit.value.toString().padStart(2, '0');
                    const jamSelesaiStr = labelSelesaiJam.text + ":" + labelSelesaiMenit.text;

                    // Panggil slot addWaktu di model Python
                    root.waktuModelRef.addWaktu(comboBoxHari.currentText, jamMulaiStr, jamSelesaiStr);

                    // Logika untuk memajukan waktu input
                    if (spinMulaiJam.value >= 23 && spinMulaiMenit.value >= 0) {
                        spinMulaiJam.value = 0;
                        spinMulaiMenit.value = 0;
                    } else {
                        spinMulaiJam.value = labelSelesaiJam.text;
                        spinMulaiMenit.value = labelSelesaiMenit.text;
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
                    anchors.fill: parent
                    boundsBehavior: Flickable.StopAtBounds
                    clip: true

                    model: root.waktuModelRef

                    delegate: ItemDelegate {
                        id: item
                        width: ListView.view.width
                        // highlighted: ListView.isCurrentItem

                        required property int index
                        required property int id_
                        required property string hari
                        required property string mulai
                        required property string selesai

                        Label {
                            id: hariLabel
                            text: item.hari
                            font.pixelSize: 18
                            font.bold: true
                        }

                        Label {
                            id: jamLabel
                            text: item.mulai + " - " + item.selesai
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
                                const message = `Apakah anda ingin menghapus waktu: \nHari: "${item.hari}".\nWaktu: ${item.mulai} - ${item.selesai}"`;

                                // qmllint disable unqualified
                                root.confirmDialogRef.openWithCallback(qsTr("Konfirmasi penghapusan waktu"), message, function () {
                                    root.waktuModelRef.removeWaktuById(id_);
                                }, () => {});
                                // qmllint enable unqualified
                            }
                        }

                        // ScrollIndicator.vertical: ScrollIndicator { }
                    }
                }
            }
        }
    }

    function hitungDurasi() {
        const durasi = 45;

        const mulaiJam = spinMulaiJam.value;
        const mulaiMenit = spinMulaiMenit.value;

        const waktuMulai = (mulaiJam * 60) + mulaiMenit;
        // const start_h = Math.floor(waktuMulai / 60)
        // const start_m = waktuMulai % 60

        const waktuSelesai = waktuMulai + durasi;
        const end_h = Math.floor(waktuSelesai / 60);
        const end_m = waktuSelesai % 60;

        //const duaDigit = v => v < 10 ? "0" + v : v
        const duaDigit = v => v.toString().padStart(2, '0');

        labelSelesaiJam.text = duaDigit(end_h);
        labelSelesaiMenit.text = duaDigit(end_m);
    }
}
