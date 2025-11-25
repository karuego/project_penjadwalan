import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

import "../components"
import "../helpers/Hari.js" as Hari

Page {
    id: root
    title: "Tambah Pengajar"
    Material.accent: Material.Blue

    property StackView stackViewRef
    property CustomDialog confirmDialogRef
    property CustomDialog alertDialogRef
    property Snackbar snackbarRef

    readonly property size textFieldSize: Qt.size(250, 50)
    readonly property size buttonSize: Qt.size(120, 50)

    property string action: "add"
    property string pengajarId: "-1"

    property var contextBridgeRef: contextBridge // qmllint disable unqualified
    property var pengajarModelRef: contextBridgeRef.pengajarModel

    // Properti untuk menyimpan daftar semua hari
    property var allDays: contextBridgeRef.namaNamaHariDict
    // Properti untuk menyimpan daftar hari yang TERSEDIA untuk dipilih
    property variant availableDays: []

    property bool isEdit: true
    property string tipePengajar

    ColumnLayout {
        spacing: 8
        anchors.fill: parent

        ButtonGroup {
            id: tipePengajarGroup
            // 'checkedButton' akan berisi RadioButton yang sedang aktif
        }

        RowLayout {
            spacing: 15

            Label {
                text: qsTr("Tipe Pengajar :")
                font.pixelSize: 14
                font.bold: true
            }

            RowLayout {
                spacing: 15
                visible: root.isEdit

                RadioButton {
                    id: radioDosen
                    text: qsTr("Dosen")
                    checked: true
                    ButtonGroup.group: tipePengajarGroup
                    enabled: root.isEdit
                }

                RadioButton {
                    id: radioAsdos
                    text: qsTr("Asisten Dosen")
                    ButtonGroup.group: tipePengajarGroup
                    enabled: root.isEdit
                }
            }

            Label {
                visible: !root.isEdit
                text: radioDosen.checked ? radioDosen.text : radioAsdos.text
                font.pixelSize: 14
                Layout.alignment: Qt.AlignVCenter
            }
        }

        TextField {
            id: textFieldId
            readOnly: !root.isEdit
            placeholderText: radioDosen.checked ? qsTr("NIDN") : radioAsdos.checked ? qsTr("NIM") : qsTr("Id")
            Accessible.name: qsTr("Input ID Pengajar")

            validator: RegularExpressionValidator {
                // Regex ini hanya mengizinkan digit (0-9).
                // ^      -> Awal string
                // [0-9]* -> Nol atau lebih karakter dari 0 sampai 9
                // $      -> Akhir string
                regularExpression: /^[0-9]*$/
            }

            // Material.containerStyle: Material.Filled
            Material.containerStyle: Material.Outlined
            background.implicitHeight: root.textFieldSize.height
            background.implicitWidth: root.textFieldSize.width
        }

        TextField {
            id: textFieldNama
            readOnly: !root.isEdit
            placeholderText: radioDosen.checked ? qsTr("Nama Dosen") : radioAsdos.checked ? qsTr("Nama Asisten Dosen") : qsTr("Nama Pengajar")
            Accessible.name: qsTr("Input Nama Pengajar")
            // Material.containerStyle: Material.Filled
            Material.containerStyle: Material.Outlined
            background.implicitHeight: root.textFieldSize.height
            background.implicitWidth: root.textFieldSize.width
        }

        Label {
            text: qsTr("Pilih waktu yang dikecualikan :")
            font.pixelSize: 14
            font.bold: true
            visible: root.isEdit
        }

        Label {
            text: qsTr("Daftar waktu yang dikecualikan :")
            font.pixelSize: 14
            font.bold: true
            visible: !root.isEdit
        }

        RowLayout {
            id: tambahWaktu
            spacing: 8
            visible: root.isEdit
            enabled: root.isEdit

            ComboBox {
                id: comboBoxHari
                background.implicitHeight: root.textFieldSize.height
                background.implicitWidth: root.textFieldSize.width
                model: root.availableDays
                textRole: "hari"
                valueRole: "idx"
            }

            Button {
                id: btnTambahWaktu
                text: qsTr("Tambah")
                enabled: comboBoxHari.count > 0
                hoverEnabled: true
                Layout.alignment: Qt.AlignRight
                implicitWidth: root.buttonSize.width

                ToolTip.delay: 300
                ToolTip.timeout: 5000
                ToolTip.visible: hovered
                ToolTip.text: qsTr("This tool tip is shown after hovering the button for a second.")

                onClicked: {
                    // Pastikan ada item yang bisa ditambahkan
                    if (comboBoxHari.currentIndex > -1) {
                        // Menambahkan objek ke ListModel
                        selectedDaysModel.append({
                            "idx": comboBoxHari.currentValue,
                            "hari": comboBoxHari.currentText
                        });
                        // Perbarui ComboBox
                        root.updateAvailableDays();
                    }
                }
            }
        }

        // qmllint disable import missing-property
        SortFilterProxyModel {
            id: proxy
            model: selectedDaysModel
            sorters: [
                RoleSorter {
                    roleName: "idx"
                }
            ]
        }
        // qmllint enable

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
                    model: proxy

                    delegate: ItemDelegate {
                        id: item
                        width: ListView.view.width
                        // highlighted: ListView.isCurrentItem

                        required property int index
                        required property int idx
                        required property string hari
                        // required property string mulai
                        // required property string selesai

                        // text: item.hari

                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: 10
                            anchors.rightMargin: 5

                            Label {
                                id: hariLabel
                                text: item.hari
                                font.pixelSize: 14
                                // font.bold: true
                                Layout.fillWidth: true
                                elide: Text.ElideRight
                                verticalAlignment: Text.AlignVCenter
                            }

                            // Label {
                            //     id: jamLabel
                            //     text: item.mulai + " - " + item.selesai
                            //     anchors.top: hariLabel.bottom
                            //     anchors.topMargin: 2
                            //     font.pixelSize: 13
                            //     color: "#555"
                            // }

                            IconButton {
                                iconName: "delete"
                                iconColor: "red"
                                ToolTip.text: "Hapus"
                                Layout.rightMargin: 16
                                enabled: root.isEdit // qmllint disable unqualified
                                visible: enabled

                                onClicked: {
                                    // confirmDialog.openWithText(`Hapus waktu: "${hariLabel.text}: ${jamLabel.text}"`);
                                    root.deleteDay(item.idx); // qmllint disable unqualified
                                }
                            }
                        }
                    }
                }
            }
        }

        Button {
            id: btnFinale
            text: root.action == 'edit' ? qsTr("Perbarui") : qsTr("Simpan")
            Material.background: Material.Blue
            Layout.alignment: Qt.AlignRight
            implicitWidth: root.buttonSize.width * 1.5
            enabled: root.isEdit
            visible: root.isEdit

            // hoverEnabled: true
            ToolTip.delay: 300
            ToolTip.timeout: 5000
            // ToolTip.visible: hovered
            ToolTip.text: qsTr("This tool tip is shown after hovering the button for a second.")

            onClicked: {
                const old_id = root.pengajarId;
                const idn = textFieldId.text.trim();
                const nama = textFieldNama.text.trim();
                const tipe = radioDosen.checked ? "dosen" : radioAsdos.checked ? "asdos" : "unknown";
                const waktu = root.getSelectedDays().join(",");

                let result = null;
                if (root.action === "edit") {
                    result = root.pengajarModelRef.update(old_id, idn, nama, tipe, waktu);
                } else {
                    result = root.pengajarModelRef.add(idn, nama, tipe, waktu);
                }

                if (result.success) {
                    const message = root.action == 'edit' ? "Data pengajar berhasil diperbarui." : "Data pengajar berhasil disimpan.";
                    root.snackbarRef.showLong(message, ()=>{});
                    root.stackViewRef.pop();
                } else {
                    root.snackbarRef.showLong(`Gagal menyimpan data pengajar: ${result.message}`, ()=>{});
                }
            }
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

    ListModel {
        id: selectedDaysModel
    }

    function deleteDay(idx) {
        for (let i = 0; i < selectedDaysModel.count; i++) {
            if (selectedDaysModel.get(i).idx === idx) {
                selectedDaysModel.remove(i, 1);
                break;
            }
        }

        updateAvailableDays();
    }

    function getSelectedDays() {
        let selectedDays = [];
        for (let i = 0; i < selectedDaysModel.count; i++) {
            selectedDays.push(selectedDaysModel.get(i).idx);
        }
        return selectedDays;
    }

    // Fungsi untuk memperbarui daftar hari yang tersedia di ComboBox
    function updateAvailableDays() {
        // 1. Dapatkan semua 'idx' yang sudah dipilih dari ListModel
        const selectedDays = getSelectedDays();

        // 2. Filter 'allDays' berdasarkan 'idx' yang BELUM ada di 'selectedDays'
        availableDays = allDays.filter(function (dayObj) {
            return !selectedDays.includes(dayObj.idx);
        });

        // 3. Setel ulang indeks ComboBox jika item saat ini tidak lagi tersedia
        if (comboBoxHari.currentIndex >= availableDays.length) {
            comboBoxHari.currentIndex = 0;
        }
    }

    function setup() {
        if (action == "view") {
            root.title = "Detail Pengajar";
            isEdit = false;
        } else if (action == "edit")
            root.title = "Edit Pengajar";
        else
            return;

        // const pengajar = contextBridgeRef.getPengajarFromProxyIndex(pengajarId);
        // const pengajar = contextBridgeRef.pengajarModel.getById(pengajarId);
        const pengajar = root.pengajarModelRef.getById(root.pengajarId);

        if (!pengajar) {
            console.log('Pengajar tidak ditemukan');
            return;
        }

        if (pengajar.id) {
            textFieldId.text = pengajar.id;
        }

        if (pengajar.nama)
            textFieldNama.text = pengajar.nama;

        if (pengajar.tipe) {
            root.tipePengajar = pengajar.tipe;

            if (pengajar.tipe === "dosen")
                radioDosen.checked = true;
            else if (pengajar.tipe === "asdos")
                radioAsdos.checked = true;
            // tipeField.currentIndex = tipeField.model.indexOf(pengajar.tipe);
        }

        const waktu = pengajar.waktu.trim();
        const hariObjList = Hari.parseHariMap(waktu);

        for (const hariObj of hariObjList) {
            selectedDaysModel.append({
                "idx": hariObj.id,
                "hari": hariObj.nama
            });
        }
    }

    // Panggil fungsi ini saat komponen selesai dimuat untuk inisialisasi
    Component.onCompleted: {
        setup();
        updateAvailableDays();
    }
}
