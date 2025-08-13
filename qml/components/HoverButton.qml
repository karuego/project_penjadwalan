import QtQuick
import Theme 1.0
import "../helpers/MaterialIcons.js" as MIcons

Rectangle {
    id: root

    signal clicked
    property int animationDuration: 300

    property alias iconName: icon.name
    property alias iconSize: icon.size
    property string hoverText: ""

    // Lebar tombol akan menyesuaikan saat teks muncul
    // width: contentRow.width + 24
    width: mouseArea.containsMouse ? (icon.width + labelText.width + 28) : (icon.width + 22)
    height: contentRow.height + 10 // Tambahkan sedikit padding vertikal

    // Agar sudutnya membulat
    radius: height / 2

    // Warna awal transparan
    color: mouseArea.containsMouse ? "#f0f0f0" : "transparent"

    // Klip konten agar tidak keluar dari batas tombol saat animasi
    clip: true

    // Layout untuk menata ikon dan teks secara horizontal
    Row {
        id: contentRow
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.rightMargin: 8
        spacing: 8

        // Area Ikon
        Icon {
            id: icon
            color: mouseArea.containsMouse ? "#555" : "#fff"
        }

        Text {
            id: labelText
            font.pixelSize: 15
            // font.bold: true
            color: "#333"
            anchors.verticalCenter: parent.verticalCenter

            opacity: mouseArea.containsMouse ? 1 : 0
            // text: mouseArea.containsMouse ? root.hoverText : ""
            text: root.hoverText

            Behavior on opacity {
                NumberAnimation {
                    // Beri sedikit jeda agar animasi lebar dimulai lebih dulu
                    duration: root.animationDuration - 100
                }
            }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: root.clicked()
    }

    Behavior on color {
        ColorAnimation {
            duration: root.animationDuration - 100
        }
    }
    Behavior on width {
        NumberAnimation {
            duration: root.animationDuration
            easing.type: Easing.OutCubic
        }
    }
}
