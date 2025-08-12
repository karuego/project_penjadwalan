pragma Singleton
import QtQuick

QtObject {
    // Lokasi file font (TTF) di project
    // readonly property string fontFile: "fonts/MaterialIcons-Regular.ttf"
    // readonly property string fontFile: "fonts/MaterialSymbolsRounded-Regular.ttf"
    readonly property string fontFile: Qt.resolvedUrl("../fonts/MaterialSymbolsRounded-Regular.ttf")

    // Nama font di sistem setelah dimuat
    // readonly property string fontFamily: "Material Icons"
    // readonly property string fontFamily: fontLoader.name
    
    // Nama font setelah berhasil dimuat
    readonly property string fontFamily: fontLoader.status === FontLoader.Ready
                                         ? fontLoader.name
                                         : "sans-serif" // fallback font


    // Pemetaan nama ikon -> kode Unicode
    readonly property var icons: ({
        "arrow_back": "\uE5C4",
        "arrow_forward": "\uE5C8",
        "home": "\uE88A",
        "menu": "\uE5D2",
        "search": "\uE8B6",
        "settings": "\uE8B8",
        "close": "\uE5CD",
        "check": "\uE5CA"
    })

    function get(name) {
        return icons[name] || ""
    }

    // Muat font hanya sekali
    /*Component.onCompleted: {
        if (Qt.fontFamilies().indexOf(fontFamily) === -1) {
            // Qt.application.fontDatabase.addApplicationFont(fontFile)
            Qt.addApplicationFont(fontFile)
        }
    }*/
    /*FontLoader {
        id: fontLoader
        source: fontFile

        onStatusChanged: {
            if (status === FontLoader.Ready) {
                console.log("[MaterialIcons] Font loaded:", name)
            } else if (status === FontLoader.Error) {
                console.error("[MaterialIcons] Failed to load font:", fontFile)
            }
        }
    }*/
}
