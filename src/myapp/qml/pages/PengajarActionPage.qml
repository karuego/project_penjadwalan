import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

import "../helpers/Hari.js" as Hari
import "../components"
import Theme 1.0 // qmllint disable import

Page {
    id: root
    title: "Tambah Pengajar"
    Material.accent: Material.Blue

    property StackView stackViewRef
    property CustomDialog confirmDialogRef
    property CustomDialog alertDialogRef

    readonly property size textFieldSize: Qt.size(250, 50)
    readonly property size buttonSize: Qt.size(120, 50)

    property string action: "add"
    property string pengajarId: "-1"

    property var contextBridgeRef: contextBridge // qmllint disable unqualified
    property var waktuModelRef: contextBridgeRef.waktuModel
    property var namaNamaHariRef: contextBridgeRef.namaNamaHari

    property string nama
    property string tipe
    property string waktu

    property bool isEdit: true

    ColumnLayout {
        spacing: 8
        anchors.fill: parent

        TextField {
            id: textFieldNama
            placeholderText: qsTr("Nama Pengajar")
            Accessible.name: qsTr("Input Nama Pengajar")
            // Material.containerStyle: Material.Filled
            Material.containerStyle: Material.Outlined
            background.implicitHeight: root.textFieldSize.height
            background.implicitWidth: root.textFieldSize.width
        }

        ButtonGroup {
            id: tipePengajarGroup
            // 'checkedButton' akan berisi RadioButton yang sedang aktif
        }

        RowLayout {
            spacing: 15

            RadioButton {
                id: radioDosen
                text: qsTr("Dosen")
                checked: true
                ButtonGroup.group: tipePengajarGroup
            }

            RadioButton {
                id: radioAsdos
                text: qsTr("Asisten Dosen")
                ButtonGroup.group: tipePengajarGroup
            }
        }

        // TextField {
        //     id: textFieldSks
        //     placeholderText: qsTr("Jumlah SKS")
        //     background.implicitHeight : root.textFieldSize.height
        //     background.implicitWidth: root.textFieldSize.width
        // }

        RowLayout {
            id: tambahWaktu
            spacing: 8
            visible: root.isEdit

            ComboBox {
                id: comboBoxWaktu
                background.implicitHeight: root.textFieldSize.height
                background.implicitWidth: root.textFieldSize.width
                // model: ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
                model: root.namaNamaHariRef
                // onCurrentValueChanged:
            }

            Button {
                id: btnTambahWaktu
                text: qsTr("Tambah")
                hoverEnabled: true
                Layout.alignment: Qt.AlignRight
                implicitWidth: root.buttonSize.width

                ToolTip.delay: 300
                ToolTip.timeout: 5000
                ToolTip.visible: hovered
                ToolTip.text: qsTr("This tool tip is shown after hovering the button for a second.")
            }
        }

        Rectangle {
            id: kotakList
            radius: 8
            border.width: 1.5
            border.color: "#bbb"

            Layout.fillWidth: true
            Layout.fillHeight: true

            ScrollView {
                id: waktuContent
                // anchors.centerIn: parent
                // spacing: 10

                anchors.fill: parent
                anchors.margins: 4

                ListView {
                    id: listView
                    spacing: 8
                    clip: true
                    model: root.waktuModelRef

                    delegate: ItemDelegate {
                        id: item
                        width: parent.width
                        highlighted: ListView.isCurrentItem

                        required property int index
                        required property string hari
                        required property string mulai
                        required property string selesai

                        Label {
                            id: hariLabel
                            text: Hari.getNama(item.hari)
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
                                console.log(`Anda menghapus item: "${hariLabel.text}: ${jamLabel.text}"`);

                                // confirmDialog.openWithText(`Hapus waktu: "${hariLabel.text}: ${jamLabel.text}"`);
                            }
                        }

                        onClicked: {
                            console.log("Anda menekan item:", index, ":", hari);
                        }

                        // ScrollIndicator.vertical: ScrollIndicator { }
                    }
                }
            }
        }

        Button {
            id: btnFinale
            text: qsTr("Simpan")
            Material.background: Material.Blue
            Layout.alignment: Qt.AlignRight
            implicitWidth: root.buttonSize.width * 1.5
            visible: root.isEdit

            // hoverEnabled: true
            ToolTip.delay: 300
            ToolTip.timeout: 5000
            // ToolTip.visible: hovered
            ToolTip.text: qsTr("This tool tip is shown after hovering the button for a second.")
        }

        /*Button {
            text: "Open"
            onClicked: popup.open()
            highlighted: true
            Material.accent: Material.Orange
            // Material.background: Material.Teal

            // Material.roundedScale: Material.NotRounded
            // Material.roundedScale: Material.ExtraSmallScale
            // Material.roundedScale: Material.SmallScale
            Material.roundedScale: Material.MediumScale
            // Material.roundedScale: Material.LargeScale
            // Material.roundedScale: Material.ExtraLargeScale
            // Material.roundedScale: Material.FullScale
        }*/

        // Popup {
        //     id: popup
        //     x: 100
        //     y: 100
        //     implicitWidth: 200
        //     implicitHeight: 300
        //     modal: true
        //     focus: true
        //     closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent

        //     padding: 10

        //     contentItem: Text {
        //         text: "Content"
        //     }

        //     /*ColumnLayout {
        //         anchors.fill: parent
        //         CheckBox { text: qsTr("E-mail") }
        //         CheckBox { text: qsTr("Calendar") }
        //         CheckBox { text: qsTr("Contacts") }
        //     }*/

        //     /*parent: Overlay.overlay

        //     x: Math.round((parent.width - width) / 2)
        //     y: Math.round((parent.height - height) / 2)
        //     width: 100
        //     height: 100*/

        //     // visible: true
        //     //     anchors.centerIn: parent
        //     //     margins: 10
        //     //     closePolicy: Popup.CloseOnEscape
        //     //     ColumnLayout {
        //     //         TextField {
        //     //             placeholderText: qsTr("Username")
        //     //         }
        //     //         TextField {
        //     //             placeholderText: qsTr("Password")
        //     //             echoMode: TextInput.Password
        //     //         }
        //     //     }
        // }

        /*RowLayout {
            Text {
                text: "Which basket?"
            }
            TextInput {
                focus: true
                validator: RegularExpressionValidator { regularExpression: /fruit basket/ }
                // validator: IntValidator { bottom:0; top: 2000}
            }
        }*/

        // TextField standar sebagai perbandingan
        /*TextField {
            placeholderText: "TextField Standar"
        }

        // TextField kustom dengan efek fokus yang lebih mencolok
        TextField {
            id: customField
            placeholderText: "Fokus Lebih Mencolok"

            // Ganti background default
            background: Rectangle {
                // Gunakan warna transparan untuk latar belakang
                color: "transparent"

                // Garis bawah yang akan kita modifikasi
                Rectangle {
                    width: parent.width
                    height: customField.activeFocus ? 2 : 1 // Garis lebih tebal saat fokus
                    color: customField.activeFocus ? Material.accent : "#888" // Warna aksen saat fokus
                    anchors.bottom: parent.bottom

                    // Animasi halus untuk perubahan warna dan tinggi
                    Behavior on color { ColorAnimation { duration: 200 } }
                    Behavior on height { NumberAnimation { duration: 200 } }
                }
            }
        }*/
    }

    Component.onCompleted: {
        if (action == "view") {
            root.title = "Detail Pengajar";
            isEdit = false;
        } else if (action == "edit")
            root.title = "Edit Pengajar";
        else
            return;

        // const pengajar = contextBridgeRef.getPengajarFromProxyIndex(pengajarId);
        const pengajar = contextBridgeRef.pengajarModel.getById(pengajarId);

        if (!pengajar) {
            console.log('Pengajar tidak ditemukan');
            return;
        }

        if (pengajar.nama)
            textFieldNama.text = pengajar.nama;

        if (pengajar.tipe) {
            if (pengajar.tipe === "dosen")
                radioDosen.checked = true;
            else if (pengajar.tipe === "asdos")
                radioAsdos.checked = true;
            // tipeField.currentIndex = tipeField.model.indexOf(pengajar.tipe);
        }

        // if (pengajar.waktu) waktuField.text = data.waktu;
    }
}
