import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

//import QtQuick.Dialogs

Dialog {
    id: dialog
    Material.theme: Material.Light
    modal: true // Mencegah interaksi dengan window di belakangnya

    property string titleStr: ""
    property string messageStr: ""
    property var acceptedCallbackFunc: function () {}
    property var rejectedCallbackFunc: function () {}

    title: dialog.titleStr
    standardButtons: Dialog.Ok | Dialog.Cancel

    contentItem: Column {
        spacing: 8

        Label {
            id: msgLabel
            text: dialog.messageStr
            wrapMode: Text.WordWrap
            // wrapMode: Text.Wrap
        }
    }

    // qmllint disable use-proper-function
    onRejected: rejectedCallbackFunc()
    onAccepted: acceptedCallbackFunc()
    // qmllint enable use-proper-function

    function openWithCallback(titleStr, messageStr, onAccept, onReject) {
        if (titleStr)
            dialog.titleStr = titleStr;
        dialog.messageStr = messageStr;

        acceptedCallbackFunc = onAccept || function () {};
        rejectedCallbackFunc = onReject || function () {};

        open();
    }
}
