import QtQuick.Controls
import QtQuick

import com.indexremake

ApplicationWindow {
    visible: true

    MainPresenter {
        id: mainPresenter
    }

    ListView {
        objectName: "documentsList"

        model: mainPresenter.documentsListModel
    }
}
