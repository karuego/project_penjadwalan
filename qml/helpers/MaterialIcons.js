// helpers/MaterialIcons.js
// Pemetaan nama ikon -> Unicode Material Icons
// Referensi: https://fonts.google.com/icons

var icons = {
    "arrow_back":       "\uE5C4",
    "arrow_forward":    "\uE5C8",
    "home":             "\uE88A",
    "menu":             "\uE5D2",
    "search":           "\uE8B6",
    "settings":         "\uE8B8",
    "close":            "\uE5CD",
    "check":            "\uE5CA"
}

function get(name) {
    return icons[name] || ""
}
