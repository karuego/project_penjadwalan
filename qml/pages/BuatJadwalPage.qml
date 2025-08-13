import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

Page {
    title: "Pembuatan Jadwal"

    Column {
        spacing: 10
        anchors.fill: parent

        Button {
            text: "Lihat Jadwal Teori"
            onClicked: stackView.push("JadwalTeoriPage.qml")
        }

        Button {
            text: "Lihat Jadwal Praktek"
            onClicked: stackView.push("JadwalPraktekPage.qml")
        }
    }
}
