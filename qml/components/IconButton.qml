import QtQuick
import QtQuick.Controls

import Theme 1.0
import "../helpers/MaterialIcons.js" as MIcons

Rectangle {
    id: root

    signal clicked

    // Teks yang muncul saat di-hover lama
    // property string tooltipText: "Hapus"

    property alias iconName: icon.name
    property alias iconSize: icon.size
    property alias iconColor: icon.color

    // Ukuran area tombol (persegi)
    // property int buttonSize: iconSize

    height: 42
    width: 42
    radius: height / 2

    // Latar belakang transparan, berubah warna saat hover/ditekan
    color: mouseArea.pressed ? "#cccccc" : mouseArea.containsMouse ? "#dfdfdf" : "transparent"

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
        onClicked: root.clicked()
    }
}
