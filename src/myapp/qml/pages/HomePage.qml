import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

Page {
    id: root
    title: qsTr("Halaman Utama")

    property StackView stackViewRef

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 8

        RowLayout {
            spacing: 16

            Button {
                text: qsTr("Daftar Waktu")
                Layout.fillWidth: true
                onClicked: root.stackViewRef.push("WaktuPage.qml")

                scale: activeFocus || hovered ? 1.05 : 1.0
                Behavior on scale {
                    NumberAnimation {
                        duration: 150
                    }
                }
            }

            Button {
                text: qsTr("Daftar Pengajar")
                Layout.fillWidth: true
                onClicked: root.stackViewRef.push("PengajarPage.qml")
                Material.roundedScale: Material.ExtraSmallScale

                scale: activeFocus || hovered ? 1.05 : 1.0
                Behavior on scale {
                    NumberAnimation {
                        duration: 150
                    }
                }
            }
        }

        RowLayout {
            spacing: 16

            Button {
                text: qsTr("Daftar Mata Kuliah")
                Layout.fillWidth: true
                onClicked: root.stackViewRef.push("MataKuliahPage.qml")
                Material.roundedScale: Material.ExtraSmallScale

                scale: activeFocus || hovered ? 1.05 : 1.0
                Behavior on scale {
                    NumberAnimation {
                        duration: 150
                    }
                }
            }

            Button {
                text: qsTr("Daftar Ruangan")
                Layout.fillWidth: true
                onClicked: root.stackViewRef.push("RuanganPage.qml")
                scale: activeFocus || hovered ? 1.05 : 1.0
                Behavior on scale {
                    NumberAnimation {
                        duration: 150
                    }
                }
            }
        }

        RowLayout {
            Button {
                text: qsTr("Buat Jadwal")
                Layout.fillWidth: true
                onClicked: root.stackViewRef.push("JadwalPage.qml")
                Material.roundedScale: Material.NotRounded
                scale: activeFocus || hovered ? 1.05 : 1.0
                Behavior on scale {
                    NumberAnimation {
                        duration: 150
                    }
                }
            }
        }
    }
}
