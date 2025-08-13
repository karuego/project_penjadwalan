import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Material

import Theme 1.0
import "helpers/MaterialIcons.js" as MIcons
import "components"

ApplicationWindow {
    id: window
    visible: true
    width: 800
    height: 600
    title: qsTr("Aplikasi Penjadwalan w/ Simulated Annealing")
    Material.theme: Material.Light

    header: ToolBar {
        HoverButton {
            iconName: "arrow_back"
            hoverText: "Kembali"

            anchors.margins: 10
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter

            // Tampilkan tombol ini hanya jika ada halaman untuk kembali
            visible: stackView.depth > 1
            onClicked: stackView.pop()
        }

        Label {
            // Menampilkan judul halaman aktif
            text: stackView.currentItem.title

            // anchors.centerIn: parent
            anchors.fill: parent
            horizontalAlignment: Qt.AlignHCenter
            verticalAlignment: Qt.AlignVCenter

            elide: Label.ElideRight
            font.pixelSize: 20
        }

        // Tombol di pojok kanan untuk info
        ToolButton {
            text: "help"
            font.pixelSize: 24
            font.family: AppTheme.materialFont
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            onClicked: infoDialog.open() // Membuka dialog
        }

        // IconButton {
        //     iconName: "help"
        //     anchors.right: parent.right
        //     anchors.verticalCenter: parent.verticalCenter
        //     onClicked: infoDialog.open()
        //     tooltipText: "Info"
        // }
    }

    // StackView adalah area di mana halaman-halaman akan ditampilkan
    StackView {
        id: stackView
        anchors.fill: parent
        anchors.margins: 8

        // Halaman awal yang ditampilkan saat aplikasi pertama kali berjalan
        initialItem: "pages/HomePage.qml"
    }

    Dialog {
        id: infoDialog
        title: "Informasi"
        modal: true // Mencegah interaksi dengan window di belakangnya
        anchors.centerIn: parent
        standardButtons: Dialog.Ok // Tombol OK standar

        Label {
            text: "Aplikasi ini dibuat dengan QML."
        }
    }
}
