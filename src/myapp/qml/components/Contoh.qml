import QtQuick

Rectangle {
    width: 100; height: 100
    color: "red"
    focus: true
    Keys.onPressed: (event)=> {
        if (event.key == Qt.Key_A) {
            console.log('Key A was pressed');
            event.accepted = true;
        }
    }
}
