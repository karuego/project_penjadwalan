import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

Rectangle {
    id: root

    property int value: 0
    property int from: 0
    property int to: 99
    property int step: 1

    property int buttonSize: 22
    property int buttonRadius: 4
    property int iconSize: 18

    property size size: Qt.size(100, 55)

    height: size.height
    width: size.width
    radius: 5

    border.width: 1
    border.color: textField.activeFocus ? Material.accent : "#888"

    Behavior on border.color { ColorAnimation { duration: 200 } }

    RowLayout {
        anchors.fill: parent
        anchors.margins: 2

        TextInput {
            id: textField
            text: root.value.toString().padStart(2, '0')
            font.pixelSize: 16

            Layout.preferredHeight: root.size.height / 1.4
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Qt.AlignVCenter

            validator: IntValidator { bottom: root.from; top: root.to }
            onTextChanged: root.value = parseInt(text) || 0
            onAccepted: root.value = parseInt(text) || 0
        }

        ColumnLayout {
            IconButton {
                iconName: "add"
                iconColor: "black"
                iconSize: iconSize
                buttonWidth: root.buttonSize
                buttonHeight: root.buttonSize
                buttonRadius: root.buttonRadius
                animationDuration: 0
                // hoverEnabled: false
                enabled: root.value < root.to
                onEnabledChanged: iconColor = enabled ? "black" : "#ccc"
                onClicked: root.value += root.step
            }

            IconButton {
                iconName: "remove"
                iconColor: "black"
                iconSize: iconSize
                buttonWidth: root.buttonSize
                buttonHeight: root.buttonSize
                buttonRadius: root.buttonRadius
                animationDuration: 0
                // hoverEnabled: false
                enabled: root.value > root.from
                onEnabledChanged: iconColor = enabled ? "black" : "#ccc"
                onClicked: root.value -= root.step
            }
        }
    }
}
