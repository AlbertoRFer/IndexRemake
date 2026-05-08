import QtQuick

ListView {
    objectName: "DocSummaryList"
    delegate: Item {
        id: delegateRoot
        width: ListView.view.width
        height: 40

        required property string title

        Text {
            id: titleText
            text: delegateRoot.title
        }
    }
}
