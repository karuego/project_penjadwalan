pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

import "."

// Window {
//     width: 640
//     height: 480
//     visible: true
//     title: qsTr("Penjadwalan")
// }
ApplicationWindow {
    id: window
    visible: true
    width: 800
    height: 600
    title: "Aplikasi Penjadwalan"

    // Material.theme: Material.Dark
    // Material.theme: Material.Light
    Material.theme: Material.System
    Material.accent: Material.Blue

    property alias stackView: stackView

    // StackView adalah area di mana halaman-halaman akan ditampilkan
    StackView {
        id: stackView
        objectName: "mainStackView"
        anchors.fill: parent

        // Halaman awal yang ditampilkan saat aplikasi pertama kali berjalan
        // initialItem: "Home.qml"
        // initialItem: Home {}
        //initialItem: asdComponent
        initialItem: homeComponent

        Component {
            id: asdComponent
            Loader {
                source: Constants.homePage
                onLoaded: {
                    item.onNavigateTo.connect(function (page) {
                        stackView.push(page)
                    })
                }
            }
        }
    }

    Component {
        id: homeComponent
        Home {
            // Pass reference stackView ke Home
            // stackView: window.stackView
            stackView: window.stackView

            onNavigateTo: function (page) {
                stackView.push(page)
            }

            onUserlogout: function () {
                // Clear user data
                // Reset to Login page
                stackView.clear()
                stackView.push("Login.qml")
            }
        }
    }

    Component {
        id: dialogComponent
        Dialog {
            title: "Custom Dialog"
            // ...
        }
    }


    /*Button {
        onClicked: {
            // Buat instance baru secara dinamis
            const dialog = dialogComponent.createObject(parent)
            dialog.open()


            var component = Qt.createComponent("MightFailComponent.qml")
            if (component.status === Component.Error) {
                console.log("Failed to load:", component.errorString())
                // App tetap jalan, show error message
                errorDialog.show("Feature not available")
            } else {
                stackView.push(component)
            }
        }
    }*/

    // Footer berisi tombol navigasi


    /*footer: Frame {
        RowLayout {
            anchors.fill: parent

            Button {
                text: "Home"
                Layout.fillWidth: true
                onClicked: {
                    // Mendorong halaman baru ke tumpukan.
                    // Jika halaman sudah ada, ia akan kembali ke sana.
                    stackView.push("HomePage.qml")
                }
            }

            Button {
                text: "Pengaturan"
                Layout.fillWidth: true
                onClicked: {
                    stackView.push("SettingsPage.qml")
                }
            }
        }
    }*/
}
