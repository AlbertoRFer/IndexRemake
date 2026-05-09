import QtQuick

import com.indexremake.core

Rectangle {
    id: header

    required property int colNumberWidth
    required property int colMainUserWidth
    required property int colUsersWidth

    height: Theme.headerRowHeight
    color: Theme.surface0
    z: 2

    component HeaderLabel: Text {
        font.family: Theme.fontFamily
        font.pixelSize: Theme.textSizeLabel
        font.weight: Font.Medium
        color: Theme.textTertiary
    }

    Row {
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: Theme.leftMargin
        spacing: 0

        HeaderLabel {
            width: header.colNumberWidth
            text: Lang.colNumber
        }
        HeaderLabel {
            width: header.colMainUserWidth
            text: Lang.colMainUser
        }

        HeaderLabel {
            width: header.colUsersWidth
            text: Lang.colUsers
            horizontalAlignment: Text.AlignHCenter
        }

        HeaderLabel {
            text: Lang.colTitle
        }
    }

    Rectangle {
        anchors.bottom: parent.bottom
        width: parent.width
        height: 1
        color: Theme.borderSubtle
    }
}
