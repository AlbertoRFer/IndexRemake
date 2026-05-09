import QtQuick
import com.indexremake.core

Item {
    id: root
    height: Theme.rowHeight

    required property int index

    // Data roles
    required property int number
    required property string title
    required property int userCount
    required property string userFirstName
    required property string userMiddleName
    required property string userLastName1
    required property string userLastName2

    // Layout
    required property int colNumberWidth
    required property int colMainUserWidth
    required property int colUsersWidth

    readonly property int colTitleWidth: width - colNumberWidth - colMainUserWidth - colUsersWidth

    readonly property string fullName: {
        let parts = [userFirstName, userMiddleName, userLastName1, userLastName2];
        return parts.filter(p => p.length > 0).join(" ");
    }

    component RowText: Text {
        font.family: Theme.fontFamily
        font.pixelSize: Theme.textSizeBody
        color: Theme.textPrimary
    }

    // Alternating row tint
    Rectangle {
        anchors.fill: parent
        color: root.index % 2 === 0 ? "transparent" : Theme.rowAlternateTint
    }

    // Hover highlight
    Rectangle {
        anchors.fill: parent
        color: Theme.textPrimary
        opacity: hoverHandler.hovered ? 0.04 : 0
        Behavior on opacity {
            NumberAnimation {
                duration: Theme.durationFast
            }
        }
    }

    // Selection: accent fill
    Rectangle {
        anchors.fill: parent
        color: Theme.accentSubtle
        visible: root.ListView.isCurrentItem
    }

    // Selection: left border
    Rectangle {
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: 3
        color: Theme.accent
        visible: root.ListView.isCurrentItem
    }

    // Row separator
    Rectangle {
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        height: 1
        color: Theme.borderSubtle
    }

    Row {
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: Theme.leftMargin
        anchors.right: parent.right
        anchors.rightMargin: Theme.leftMargin
        spacing: 0

        RowText {
            width: root.colNumberWidth
            text: root.number
        }

        RowText {
            width: root.colMainUserWidth
            text: root.fullName
            elide: Text.ElideRight
        }

        RowText {
            width: root.colUsersWidth
            text: root.userCount
            horizontalAlignment: Text.AlignHCenter
        }

        RowText {
            width: root.colTitleWidth
            text: root.title
            elide: Text.ElideRight
        }
    }

    HoverHandler {
        id: hoverHandler
    }

    TapHandler {
        onTapped: root.ListView.view.currentIndex = root.index
    }
}
