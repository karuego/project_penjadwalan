import QtQuick
import QtQuick.Controls
import "../components"

Pane {
    Column {
        Label {
            text: "Ini halaman Tentang Aplikasi"
            anchors.centerIn: parent
        }

        HoverButton {
            iconName: "arrow_back"
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.margins: 10

            onClicked: StackView.view.pop()
        }
    }
}
