import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

Popup {
    id: root

    property string text: ""
    property int duration: 2000

    property bool isTimerRunning: closeTimer.running
    property var closeActionFunc: null

    height: 60
    padding: 5

    // Non-modal, jangan tutup saat diklik di luar
    modal: false
    closePolicy: Popup.CloseOnEscape

    // Atur tampilan agar terlihat seperti snackbar
    background: Rectangle {
        color: "#333" // Warna latar Material Design
        radius: 4
    }

    contentItem: Label {
        text: root.text
        color: "white"
        padding: 16
    }

    // Gunakan Timer untuk menutup otomatis
    Timer {
        id: closeTimer
        interval: root.duration
        onTriggered: {
            root.close();

            if (root.closeActionFunc)
                root.closeActionFunc(); // qmllint disable use-proper-function
        }
    }

    // Atur animasi masuk dan keluar
    enter: Transition {
        NumberAnimation {
            property: "opacity"
            from: 0.0
            to: 1.0
            duration: 200
        }
        NumberAnimation {
            property: "y"
            from: root.parent.height
            to: root.parent.height - root.height - root.margins
            duration: 200
        }
    }

    exit: Transition {
        NumberAnimation {
            property: "opacity"
            from: 1.0
            to: 0.0
            duration: 200
        }
        NumberAnimation {
            property: "y"
            from: root.parent.height - root.height - root.margins
            to: root.parent.height
            duration: 200
        }
    }

    // Hentikan timer jika ditutup manual
    onClosed: {
        closeTimer.stop();
    }

    // Fungsi untuk menampilkan snackbar
    function show(message, closeActionFunc) {
        root.text = message;
        if (closeActionFunc)
            root.closeActionFunc = closeActionFunc;

        root.open();
        closeTimer.start();
    }

    // Fungsi untuk menampilkan snackbar
    function showLong(message, closeActionFunc) {
        root.text = message;
        root.duration = 5000; // Durasi lebih lama

        if (closeActionFunc)
            root.closeActionFunc = closeActionFunc;

        root.open();
        closeTimer.start();
    }

    // Fungsi untuk menampilkan snackbar
    function showDuration(duration, message, closeActionFunc) {
        root.text = message;
        root.duration = duration; // Atur durasi sesuai parameter

        if (closeActionFunc)
            root.closeActionFunc = closeActionFunc;

        root.open();
        closeTimer.start();
    }
}
