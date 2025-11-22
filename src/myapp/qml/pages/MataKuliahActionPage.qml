import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

Page {
    id: root
    title: "Tambah Mata Kuliah"

    property StackView stackViewRef

    ColumnLayout {
        spacing: 10
        anchors.fill: parent

        TextField {
            id: textFieldNama
            placeholderText: qsTr("Mata Kuliah")
            Accessible.name: qsTr("Input Nama Pengajar")
            // Material.containerStyle: Material.Filled
            Material.containerStyle: Material.Outlined
            background.implicitHeight: 50
            background.implicitWidth: 250
        }

        ButtonGroup {
            id: tipePerkuliahan
            // 'checkedButton' akan berisi RadioButton yang sedang aktif
        }

        RowLayout {
            spacing: 15

            RadioButton {
                id: radioTeori
                text: qsTr("Teori")
                ButtonGroup.group: tipePerkuliahan
            }

            RadioButton {
                id: radioPraktek
                text: qsTr("Praktikum")
                ButtonGroup.group: tipePerkuliahan
            }
        }

        TextField {
            id: textFieldSks
            placeholderText: qsTr("Jumlah SKS")
            background.implicitHeight: 50
            background.implicitWidth: 250
        }

        TextField {
            id: textFieldSemester
            placeholderText: qsTr("Semester")
            background.implicitHeight: 50
            background.implicitWidth: 250
        }

        TextField {
            id: textFieldPengampu
            placeholderText: qsTr("Pengampu")
            background.implicitHeight: 50
            background.implicitWidth: 250
        }

        TextField {
            id: textFieldJumlahKelas
            placeholderText: qsTr("Jumlah Kelas")
            background.implicitHeight: 50
            background.implicitWidth: 250
        }

        Button {
            text: qsTr("Button")
            hoverEnabled: true
            ToolTip.delay: 300
            ToolTip.timeout: 5000
            ToolTip.visible: hovered
            ToolTip.text: qsTr("This tool tip is shown after hovering the button for a second.")
        }

        Button {
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
        }

        Popup {
            id: popup
            // x: 100; y: 100
            Layout.leftMargin: 100
            Layout.topMargin: 100
            implicitWidth: 200
            implicitHeight: 300
            modal: true
            focus: true
            closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent

            padding: 10

            contentItem: Text {
                text: "Content"
            }

            /*ColumnLayout {
                anchors.fill: parent
                CheckBox { text: qsTr("E-mail") }
                CheckBox { text: qsTr("Calendar") }
                CheckBox { text: qsTr("Contacts") }
            }*/

            /*parent: Overlay.overlay

            x: Math.round((parent.width - width) / 2)
            y: Math.round((parent.height - height) / 2)
            width: 100
            height: 100*/

            // visible: true
            //     anchors.centerIn: parent
            //     margins: 10
            //     closePolicy: Popup.CloseOnEscape
            //     ColumnLayout {
            //         TextField {
            //             placeholderText: qsTr("Username")
            //         }
            //         TextField {
            //             placeholderText: qsTr("Password")
            //             echoMode: TextInput.Password
            //         }
            //     }
        }

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
        TextField {
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
                    Behavior on color {
                        ColorAnimation {
                            duration: 200
                        }
                    }
                    Behavior on height {
                        NumberAnimation {
                            duration: 200
                        }
                    }
                }
            }
        }
    }

    Component.onCompleted: {
        radioTeori.checked = true;
    }
}
