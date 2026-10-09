import QtQuick
import ".."

Item {
    implicitWidth: Theme.componentsAvatarWidth
    implicitHeight: Theme.componentsAvatarHeight
    Accessible.ignored: true

    Image {
        anchors.fill: parent
        source: Theme.avatarSource
        sourceSize.width: Theme.componentsAvatarWidth
        sourceSize.height: Theme.componentsAvatarHeight
        fillMode: Image.PreserveAspectFit
        smooth: false
        mipmap: false
        Accessible.ignored: true
    }
}
