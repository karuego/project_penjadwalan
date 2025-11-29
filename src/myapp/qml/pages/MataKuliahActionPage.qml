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

    property string action: "add"
    property int matakuliahId: -1
    property bool isEdit: true
    property string tipeMatakuliah

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
            id: rowDosen

            Label {
                text: qsTr("Dosen Pengampu :")
            }

            ComboBox {
                id: comboBoxDosen
                Layout.preferredWidth: 300
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
            id: rowAsdos
            visible: radioPraktek.checked

            Label {
                text: qsTr("Asisten Dosen :      ")
            }

            ComboBox {
                id: comboBoxAsdos
                Layout.preferredWidth: 300
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
            text: root.action == 'edit' ? qsTr("Perbarui") : qsTr("Simpan")
            hoverEnabled: true
            ToolTip.delay: 300
            ToolTip.timeout: 5000
            ToolTip.visible: hovered
            ToolTip.text: qsTr("Menyimpan data mata kuliah ke database")

            onClicked: {
                const nama = textFieldNama.text.trim();
                const tipe = radioTeori.checked ? "teori" : radioPraktek.checked ? "praktek" : "unknown";
                const sks = textFieldSks.text
                const semester = textFieldSemester.text
                const kelas = textFieldJumlahKelas.text
                const dosenId = comboBoxDosen.currentValue
                const asdosId = comboBoxAsdos.currentValue

                const pengampuId = tipe === "teori" ? dosenId : asdosId;

                let result = null;
                if (root.action === "edit") {
                    result = root.matakuliahModelRef.update(root.matakuliahId, nama, semester, kelas, pengampuId);
                } else {
                    result = root.matakuliahModelRef.add(nama, tipe, sks, semester, kelas, dosenId, asdosId);
                }

                if (result.success) {
                    root.snackbarRef.showLong("Data mata kuliah berhasil disimpan.", ()=>{});
                    root.stackViewRef.pop();
                } else {
                    root.snackbarRef.showLong(`Gagal menyimpan data mata kuliah: ${result.message}`, ()=>{});
                }
            }
        }
    }

    Component.onCompleted: {
        if (action == "view") {
            root.title = "Detail Pengajar";
            isEdit = false;
        } else if (action == "edit")
            root.title = "Edit Pengajar";
        else
            return;

        textFieldNama.readOnly = true;
        textFieldSks.readOnly = true;
        radioTeori.enabled = false;
        radioPraktek.enabled = false;

        // const pengajar = contextBridgeRef.getPengajarFromProxyIndex(pengajarId);
        // const pengajar = contextBridgeRef.pengajarModel.getById(pengajarId);
        const matkul = root.matakuliahModelRef.getById(root.matakuliahId);

        if (!matkul) {
            console.log('Mata Kuliah tidak ditemukan');
            root.snackbarRef.showLong("Error: Mata Kuliah tidak ditemukan.", ()=>{});
            return;
        }

        if (matkul.nama)
            textFieldNama.text = matkul.nama;

        if (matkul.tipe) {
            root.tipeMatakuliah = matkul.tipe;
            radioPraktek.text = "Praktikum";

            if (matkul.tipe === "teori") {
                radioTeori.checked = true;

                rowDosen.visible = true;
                rowAsdos.visible = false;
                comboBoxDosen.currentValue = matkul.pengampu.id;
            } else if (matkul.tipe === "praktek") {
                radioPraktek.checked = true;

                rowDosen.visible = false;
                rowAsdos.visible = true;
                comboBoxAsdos.currentValue = matkul.pengampu.id;
            }
            // tipeField.currentIndex = tipeField.model.indexOf(pengajar.tipe);
        }

        if (matkul.sks)
            textFieldSks.text = matkul.sks;
        if (matkul.semester)
            textFieldSemester.text = matkul.semester;
        if (matkul.kelas)
            textFieldJumlahKelas.text = matkul.kelas;
    }
}
