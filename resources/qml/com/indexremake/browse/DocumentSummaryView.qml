pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Controls

import com.indexremake.core

ListView {
    id: summaryList
    clip: true

    readonly property int colNumberWidth: 52
    readonly property int colMainUserWidth: 260
    readonly property int colUsersWidth: 120

    headerPositioning: ListView.OverlayHeader

    header: DocumentSummaryHeader {
        width: summaryList.width
        colNumberWidth: summaryList.colNumberWidth
        colMainUserWidth: summaryList.colMainUserWidth
        colUsersWidth: summaryList.colUsersWidth
    }

    delegate: DocumentSummaryRow {
        width: summaryList.width
        colNumberWidth: summaryList.colNumberWidth
        colMainUserWidth: summaryList.colMainUserWidth
        colUsersWidth: summaryList.colUsersWidth
    }

    // Empty list text
    Text {
        anchors.centerIn: parent
        visible: summaryList.count === 0
        text: Lang.emptyDocList
        font.family: Theme.fontFamily
        font.pixelSize: Theme.textSizeBody
        color: Theme.textTertiary
    }

    ScrollBar.vertical: ScrollBar {
        id: scrollBar
        policy: ScrollBar.AlwaysOn
        contentItem: Rectangle {
            implicitWidth: 10
            radius: Theme.radiusSmall
            color: scrollBar.hovered || scrollBar.pressed ? Theme.accent : Theme.scrollBarResting
            Behavior on color {
                ColorAnimation {
                    duration: Theme.durationFast
                }
            }
        }
    }
}
