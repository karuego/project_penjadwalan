import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Material

import Theme 1.0
import "components"

//import "helpers/MaterialIcons.js" as MIcons

ApplicationWindow {
    id: root
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
                if (ev.key != Qt.Key_Escape)
                    return;
                root.contentItem.forceActiveFocus();
                ev.accepted = true;
            }
        }

        Label {
            // Menampilkan judul halaman aktif
            // qmllint disable missing-property
            text: stackView.currentItem?.title ?? ""
            // qmllint enable missing-property

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

            Behavior on font.pixelSize {
                NumberAnimation {
                    duration: 150
                }
            }
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
        onCurrentItemChanged: {
            if (!currentItem)
                return;

            if ("stackViewRef" in currentItem)
                currentItem.stackViewRef = stackView;
            if ("confirmDialogRef" in currentItem)
                currentItem.confirmDialogRef = confirmDialog;
            if ("alertDialogRef" in currentItem)
                currentItem.alertDialogRef = alertDialog;
        }

        Keys.onPressed: ev => {
            if (ev.key == Qt.Key_Backspace && stackView.depth > 1) {
                hoverBackButton.clicked();
                ev.accepted = true;
            } else if (ev.key == Qt.Key_Escape) {
                root.contentItem.forceActiveFocus();
                ev.accepted = true;
            }
        }
    }

    Dialog {
        id: infoDialog
        title: qsTr("Informasi")
        modal: true
        anchors.centerIn: parent
        standardButtons: Dialog.Ok
        width: parent.width / 2
        height: parent.height / 1.5

        Column {
            Label {
                text: qsTr("Aplikasi ini dibuat dengan QML.")
            }

            Image {
                source: "../assets/icon.jpg"
                width: 100
                height: 100
                Layout.alignment: Qt.AlignHCenter
                fillMode: Image.PreserveAspectCrop
            }
        }
    }

    CustomDialog {
        id: alertDialog
        title: qsTr("Peringatan")
        anchors.centerIn: parent
        standardButtons: Dialog.Ok
        // width: parent.width / 2
        // height: parent.height / 1.5
    }

    CustomDialog {
        id: confirmDialog
        anchors.centerIn: parent
    }

    /*TextArea {
        id: logArea
        readOnly: true
        textFormat: TextEdit.PlainText
        wrapMode: TextEdit.Wrap
    }

    Connections {
        target: LogBridge
        function onLogMessage(msg) {
            logArea.append(msg);
        }
    }*/

    Component.onCompleted:
    // Setelah semua komponen di window ini selesai dimuat,
    // paksa fokus ke komponen dengan id 'myFirstButton'.
    // hoverBackButton.forceActiveFocus()
    {}
}
