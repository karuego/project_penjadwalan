import QtQuick
import Theme 1.0 // qmllint disable import
// import "../helpers/MaterialIcons.js" as MIcons

Text {
    id: root

    property alias name: root.text
    property alias size: root.font.pixelSize
    property int animationDuration: 200

    text: "help"
    font.family: AppTheme.materialFont
    font.pixelSize: 24
    color: "#333"

    // Atur ukuran Text agar pas dengan ukuran ikon
    width: paintedWidth
    height: paintedHeight

    Behavior on color { ColorAnimation { duration: root.animationDuration } }
}
