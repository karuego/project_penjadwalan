import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

Page {
    title: "Daftar Waktu Kuliah"

    Column {
        spacing: 10
        anchors.fill: parent

        Button {
            text: "Tambah Waktu Kuliah"
            onClicked: stackView.push("TambahWaktuPage.qml")
        }
    }
}
