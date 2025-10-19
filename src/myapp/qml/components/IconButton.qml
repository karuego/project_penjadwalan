import QtQuick
import QtQuick.Controls

import Theme 1.0
import "../helpers/MaterialIcons.js" as MIcons

Rectangle {
    id: root

    signal clicked

    // Teks yang muncul saat di-hover lama
    // property string tooltipText: "Hapus"

    property bool hoverEnabled: true
    property bool enabled: true

    property alias iconName: icon.name
    property alias iconSize: icon.size
    property alias iconColor: icon.color
    property alias animationDuration: icon.animationDuration

    // Ukuran area tombol (persegi)
    // property int buttonSize: iconSize
    property alias buttonWidth: root.width
    property alias buttonHeight: root.height
    property alias buttonRadius: root.radius

    width: 42
    height: 42
    radius: height / 2

    // Latar belakang transparan, berubah warna saat hover/ditekan
    // color: mouseArea.pressed ? "#cccccc" : mouseArea.containsMouse ? "#dfdfdf" : "transparent"
    color: "transparent"

    // ToolTip.text: "Hapus"
    // ToolTip.visible: true
    // ToolTip.delay: 500 // Jeda sebelum tooltip muncul

    // Animasi perubahan warna yang halus
    // Behavior on color { ColorAnimation { duration: 150 } }

    Icon {
        id: icon
        anchors.centerIn: parent
        color: mouseArea.containsMouse ? "#555" : "#fff"
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        onClicked: if (root.enabled) root.clicked()
        onEntered: if (root.hoverEnabled) {
            root.color = mouseArea.pressed ? "#cccccc" : "#dfdfdf"
        }
        onExited: if (root.hoverEnabled) root.color = "transparent"
    }
}
