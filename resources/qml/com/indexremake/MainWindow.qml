import QtQuick.Controls
import QtQuick

import com.indexremake

ApplicationWindow {
    visible: true

    ListView {
        objectName: "documentsList"

        model: MainPresenter.documentsListModel
    }
}
