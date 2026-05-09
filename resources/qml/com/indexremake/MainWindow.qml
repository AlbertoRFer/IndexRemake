import QtQuick
import QtQuick.Controls

import com.indexremake.bridge
import com.indexremake.browse
import com.indexremake.core

ApplicationWindow {
    visible: true
    width: 1100
    height: 700
    minimumWidth: 800
    minimumHeight: 500
    title: Lang.appTitle
    color: Theme.surface0

    Page {
        anchors.fill: parent
        background: Rectangle {
            color: "transparent"
        }

        Rectangle {
            id: headerBar
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            height: Theme.headerBarHeight
            color: Theme.surface1

            Rectangle {
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                height: 1
                color: Theme.borderSubtle
            }

            Text {
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: Theme.leftMargin
                text: Lang.browseTitle
                font.family: Theme.fontFamily
                font.pixelSize: Theme.textSizeHeading
                font.weight: Font.DemiBold
                color: Theme.textPrimary
            }
        }

        DocumentSummaryView {
            objectName: "docSummaryList"
            anchors.top: headerBar.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            model: MainPresenter.documentsListModel
        }
    }
}
