import QtQuick
import Theme 1.0
import "../helpers/MaterialIcons.js" as MIcons

Rectangle {
    id: root

    signal clicked

    property bool extend: false
    property bool pressed: false
    property bool hovered: mouseArea.containsMouse ? true : false
    property string hoverText: ""

    property alias iconName: icon.name
    property alias iconSize: icon.size

    property int animationDuration: 300

    // Lebar tombol akan menyesuaikan saat teks muncul
    // width: contentRow.width + 24
    //width: mouseArea.containsMouse ? (icon.width + labelText.width + 28) : (icon.width + 22)
    width: root.hovered ? (icon.width + labelText.width + 28) : (icon.width + 22)
    height: contentRow.height + 10 // Tambahkan sedikit padding vertikal
    radius: height / 2

    // Klip konten agar tidak keluar dari batas tombol saat animasi
    clip: true

    //color: mouseArea.containsMouse ? "#f0f0f0" : "transparent"
    // color: root.hovered ? "#f0f0f0" : "transparent"
    // color: mouseArea.pressed || (activeFocus && keys.spacePressed) ? "#c0c0c0" : "#e9e9e9"
    color: if (root.hovered) {
        if (mouseArea.pressed || (activeFocus && root.pressed))
            "#c0c0c0"
        // else "#e9e9e9"
        else "#f0f0f0"
    } else "transparent"

    focus: true
    activeFocusOnTab: true
    onActiveFocusChanged: root.hovered = activeFocus

    Row {
        id: contentRow
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.rightMargin: 8
        spacing: 8

        Icon {
            id: icon
            //color: mouseArea.containsMouse ? "#555" : "#fff"
            color: root.hovered ? "#555" : "#fff"
        }

        Text {
            id: labelText
            font.pixelSize: 15
            // font.bold: true
            color: "#333"
            anchors.verticalCenter: parent.verticalCenter

            //opacity: mouseArea.containsMouse ? 1 : 0
            opacity: root.hovered ? 1 : 0
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
        onEntered: root.hovered = true
        onExited: root.hovered = false
        onClicked: root.pressed = true
        onReleased: {
            root.pressed = false
            root.clicked()
        }

        // Lacak posisi mouse setiap saat
        /*onPositionChanged: (mouse) => {
            // Temukan anak di bawah posisi mouse saat ini
            var child = parentRow.childAt(mouse.x, mouse.y)
            // Simpan anak yang ditemukan ke properti
            parentRow.currentlyHovered = child;
        }

        // Reset saat mouse meninggalkan area induk
        onExited: parentRow.currentlyHovered = null
        */
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

    // Aksi saat tombol Enter/Spasi ditekan ketika fokus
    Keys.onPressed: (ev) => action(ev, true)
    Keys.onReleased: (ev) => {
        if (action(ev, false))
            root.clicked()
    }

    function action(event, value: bool): bool {
        const keys = [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Space]
        for (const key of keys) {
            if (event.key != key) continue
            root.pressed = value
            event.accepted = true
            return true
        }
        return false
    }

    // Connections bertugas "mendengarkan" sinyal dari target
    /*Connections {
        target: root // Dengarkan sinyal dari root (diri sendiri)

        // Nama fungsi harus 'on' + nama sinyal dengan huruf besar
        function onClicked() {
            console.log("Aksi internal terdeteksi melalui Connections!");
        }
    }*/

    /*Component.onCompleted: {
        root.clicked.connect(() => {
            console.log("Aksi internal terdeteksi melalui signal.connect()!");
        })
    }*/

    onClicked: console.log("Aksi internal terdeteksi!");
}
