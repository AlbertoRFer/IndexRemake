import QtQuick.Controls
import QtQuick

import com.indexremake

ApplicationWindow {
    visible: true
    width: 400
    height: 600
    title: "Indice"

    Page {
        anchors.fill: parent
        DocumentSummaryView {
            objectName: "docSummaryList"
            width: parent.width
            height: parent.height

            model: MainPresenter.documentsListModel
        }
    }
}
