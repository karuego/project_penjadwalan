import QtQuick
import QtQuick.Controls

import "."

HomeForm {
    property StackView stackView

    signal navigateTo(string page)
    signal userlogout(string page)

    button1 {
        anchors.centerIn: parent
        onClicked: {
            //console.log("Halo")
            // stackView.push(Qt.createComponent("DosenPage.ui.qml"))
            navigateTo(Constants.dosenPage)
        }
    }
}
