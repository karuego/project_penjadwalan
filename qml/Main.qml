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
    // Material.theme: Material.Dark
    // Material.accent: Material.Blue

    header: ToolBar {
        // background: Rectangle {
        //     color: Material.color(Material.Indigo)
        // }
        // RowLayout {
        //     anchors.fill: parent

        HoverButton {
            id: hoverBackButton
            iconName: "arrow_back"
            hoverText: qsTr("Kembali")

            anchors.margins: 10
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter

            // Tampilkan tombol ini hanya jika ada halaman untuk kembali
            visible: stackView.depth > 1
            focus: visible
            onClicked: stackView.pop()

            ToolTip.delay: 1000
            ToolTip.timeout: 5000
            ToolTip.visible: this.hovered
            ToolTip.text: qsTr("Kembali ke halaman sebelumnya")
            Keys.onReleased: ev => {
                if (ev.key != Qt.Key_Escape) return;
                window.contentItem.forceActiveFocus()
                ev.accepted = true
            }
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
            // font.pixelSize: 24
            font.pixelSize: activeFocus || hovered ? 32 : 24
            font.family: AppTheme.materialFont
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            onClicked: infoDialog.open()

            Behavior on font.pixelSize { NumberAnimation { duration: 150 } }
        }

        // IconButton {
        //     iconName: "help"
        //     anchors.right: parent.right
        //     anchors.verticalCenter: parent.verticalCenter
        //     onClicked: infoDialog.open()
        //     tooltipText: "Info"
        // }

        // }
    }

    // StackView adalah area di mana halaman-halaman akan ditampilkan
    StackView {
        id: stackView
        anchors.fill: parent
        anchors.topMargin: 16
        anchors.bottomMargin: 24
        anchors.leftMargin: 24
        anchors.rightMargin: 24

        // Halaman awal yang ditampilkan saat aplikasi pertama kali berjalan
        initialItem: "pages/HomePage.qml"

        Keys.onPressed: (ev) => {
            if (ev.key == Qt.Key_Backspace && stackView.depth > 1) {
                hoverBackButton.clicked()
                ev.accepted = true;
            } else if (ev.key == Qt.Key_Escape) {
                window.contentItem.forceActiveFocus();
                ev.accepted = true;
            }
        }
    }

    Dialog {
        id: infoDialog
        title: qsTr("Informasi")
        modal: true // Mencegah interaksi dengan window di belakangnya
        anchors.centerIn: parent
        standardButtons: Dialog.Ok // Tombol OK standar

        Label {
            text: qsTr("Aplikasi ini dibuat dengan QML.")
        }
    }

    Component.onCompleted: {
        // Setelah semua komponen di window ini selesai dimuat,
        // paksa fokus ke komponen dengan id 'myFirstButton'.
        // hoverBackButton.forceActiveFocus()
    }
}
