pragma Singleton
import QtQuick

QtObject {
    // Browse view — column headers
    readonly property string colNumber: qsTr("#")
    readonly property string colTitle: qsTr("TITLE")
    readonly property string colUsers: qsTr("USERS")
    readonly property string colMainUser: qsTr("MAIN USER")

    // Browse view — empty state
    readonly property string emptyDocList: qsTr("No documents in this protocol")

    // Header bar
    readonly property string browseTitle: qsTr("Documents")

    // App
    readonly property string appTitle: qsTr("Protocol Manager")
}
