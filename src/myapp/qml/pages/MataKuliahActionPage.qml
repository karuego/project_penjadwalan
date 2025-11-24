import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

import "../components"
import Theme // qmllint disable import

Page {
    id: root
    title: "Tambah Mata Kuliah"

    property StackView stackViewRef
    property CustomDialog confirmDialogRef
    property CustomDialog alertDialogRef
    property Snackbar snackbarRef

    property var contextBridgeRef: contextBridge // qmllint disable unqualified
    property var pengajarModelRef: contextBridgeRef.pengajarModel
    property var matakuliahModelRef: contextBridgeRef.matakuliahModel

    ColumnLayout {
        spacing: 10
        anchors.fill: parent

        TextField {
            id: textFieldNama
            placeholderText: qsTr("Mata Kuliah")
            Accessible.name: qsTr("Input Nama Mata Kuliah")
            // Material.containerStyle: Material.Filled
            Material.containerStyle: Material.Outlined
            background.implicitHeight: 50
            background.implicitWidth: 250
        }

        ButtonGroup {
            id: tipePerkuliahan
            onClicked: {

            }
        }

        RowLayout {
            spacing: 15

            RadioButton {
                id: radioTeori
                text: qsTr("Teori")
                ButtonGroup.group: tipePerkuliahan
                checked: true
                onCheckedChanged: {
                    textFieldSks.text = "2"
                }
            }

            RadioButton {
                id: radioPraktek
                text: qsTr("Teori + Praktikum")
                ButtonGroup.group: tipePerkuliahan
                onCheckedChanged: {
                    textFieldSks.text = "3"
                }
            }
        }

        TextField {
            id: textFieldSks
            text: "2"
            placeholderText: qsTr("Jumlah SKS")
            background.implicitHeight: 50
            background.implicitWidth: 250
            validator: RegularExpressionValidator {
                regularExpression: /^[0-9]*$/
            }
        }

        TextField {
            id: textFieldSemester
            placeholderText: qsTr("Semester")
            background.implicitHeight: 50
            background.implicitWidth: 250
            validator: RegularExpressionValidator {
                regularExpression: /^[0-9]*$/
            }
        }

        TextField {
            id: textFieldJumlahKelas
            placeholderText: qsTr("Jumlah Kelas yang Memprogram")
            background.implicitHeight: 50
            background.implicitWidth: 250
            validator: RegularExpressionValidator {
                regularExpression: /^[0-9]*$/
            }
        }

        TextField {
            id: textFieldJumlahSesi
            visible: false
            placeholderText: qsTr("Jumlah Sesi Praktikum")
            background.implicitHeight: 50
            background.implicitWidth: 250
            validator: RegularExpressionValidator {
                regularExpression: /^[0-9]*$/
            }
        }

        // qmllint disable
        SortFilterProxyModel {
            id: proxyFilterDosen
            model: root.pengajarModelRef

            sorters: [
                RoleSorter {
                    roleName: "nama"
                    sortOrder: Qt.AscendingOrder
                }
            ]
            filters: [
                ValueFilter {
                    roleName: "tipe"
                    value: "dosen"
                }
            ]
        }
        // qmllint enable

        // qmllint disable
        SortFilterProxyModel {
            id: proxyFilterAsdos
            model: root.pengajarModelRef

            sorters: [
                RoleSorter {
                    roleName: "nama"
                    sortOrder: Qt.AscendingOrder
                }
            ]
            filters: [
                ValueFilter {
                    roleName: "tipe"
                    value: "asdos"
                }
            ]
        }
        // qmllint enable

        RowLayout {
            Label {
                text: qsTr("Dosen Pengampu :")
            }

            ComboBox {
                id: comboBoxDosen
                Layout.preferredWidth: 300
                editable: true
                model: proxyFilterDosen
                textRole: "nama"
                valueRole: "id_"
                onAccepted: {
                    if (find(editText) === -1)
                        model.append({text: editText})
                }
            }
        }

        RowLayout {
            visible: radioPraktek.checked

            Label {
                text: qsTr("Asisten Dosen :      ")
            }

            ComboBox {
                id: comboBoxAsdos
                Layout.preferredWidth: 300
                editable: true
                model: proxyFilterAsdos
                textRole: "nama"
                valueRole: "id_"
                onAccepted: {
                    if (find(editText) === -1)
                        model.append({text: editText})
                }
            }
        }

        Button {
            text: qsTr("Simpan")
            hoverEnabled: true
            ToolTip.delay: 300
            ToolTip.timeout: 5000
            ToolTip.visible: hovered
            ToolTip.text: qsTr("This tool tip is shown after hovering the button for a second.")

            onClicked: {
                const nama = textFieldNama.text.trim();
                const tipe = radioTeori.checked ? "teori" : radioPraktek.checked ? "praktek" : "unknown";
                const sks = textFieldSks.text
                const semester = textFieldSemester.text
                const kelas = textFieldJumlahKelas
                const sesi = textFieldJumlahSesi
                const dosenId = comboBoxDosen.currentValue
                const asdosId = comboBoxAsdos.currentValue

                let result = null;
                if (root.action === "edit") {
                    result = root.pengajarModelRef.update(old_id, idn, nama, tipe, waktu);
                } else {
                    result = root.pengajarModelRef.add(idn, nama, tipe, waktu);
                }

                if (result.success) {
                    root.snackbarRef.showLong("Data pengajar berhasil disimpan.", ()=>{});
                    root.stackViewRef.pop();
                } else {
                    root.snackbarRef.showLong(`Gagal menyimpan data pengajar: ${result.message}`, ()=>{});
                }
            }
        }
    }

    Component.onCompleted: {
        radioTeori.checked = true;
    }
}
