pragma Singleton
import QtQuick

QtObject {
    // Page paths
    readonly property string homePage: "Home.qml"
    readonly property string dosenPage: "Dosen.qml"
    readonly property string aboutPage: "pages/AboutPage.qml"

    // Component paths
    readonly property string userCard: "components/UserCard.qml"
    readonly property string customDialog: "components/CustomDialog.qml"

    // Asset paths
    readonly property string iconPath: "../assets/icons/"
    readonly property string imagePath: "../assets/images/"
}
