import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

// import "../helpers"
import "../helpers/MaterialIcons.js" as MIcons
import "../components"
import Theme 1.0

Page {
    id: pageTambahPengajar
    title: "Tambah Pengajar"
    // Material.theme: Material.Light
    Material.accent: Material.Blue

    readonly property size textFieldSize: Qt.size(250, 50)

    ColumnLayout {
        anchors.fill: parent

        TextField {
            id: textFieldNama
            placeholderText: qsTr("Nama Pengajar")
            Accessible.name: qsTr("Input Nama Pengajar")
            // Material.containerStyle: Material.Filled
            Material.containerStyle: Material.Outlined
            background.implicitHeight : textFieldSize.height
            background.implicitWidth: textFieldSize.width
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
                ButtonGroup.group: tipePengajarGroup
            }

            RadioButton {
                id: radioAsdos
                text: qsTr("Asisten Dosen")
                ButtonGroup.group: tipePengajarGroup
            }
        }

        TextField {
            id: textFieldSks
            placeholderText: qsTr("Jumlah SKS")
            background.implicitHeight : textFieldSize.height
            background.implicitWidth: textFieldSize.width
        }

        TextField {
            id: textFieldSemester
            placeholderText: qsTr("Semester")
            background.implicitHeight : textFieldSize.height
            background.implicitWidth: textFieldSize.width
        }

        TextField {
            id: textFieldPengampu
            placeholderText: qsTr("Pengampu")
            background.implicitHeight : textFieldSize.height
            background.implicitWidth: textFieldSize.width
        }

        TextField {
            id: textFieldJumlahKelas
            placeholderText: qsTr("Jumlah Kelas")
            background.implicitHeight : textFieldSize.height
            background.implicitWidth: textFieldSize.width
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
            x: 100
            y: 100
            width: 200
            height: 300
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
                    Behavior on color { ColorAnimation { duration: 200 } }
                    Behavior on height { NumberAnimation { duration: 200 } }
                }
            }
        }
    }

    Component.onCompleted: {
        radioDosen.checked = true
    }
}
