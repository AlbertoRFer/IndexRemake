import QtQuick.Controls
import QtQuick

import com.indexremake

ApplicationWindow {
    visible: true

    ListView {
        objectName: "documentsList"
        width: parent.width
        height: 600
        model: MainPresenter.documentsListModel

        delegate: ItemDelegate {
            width: ListView.view.width
            text: model.display
        }
    }
}
