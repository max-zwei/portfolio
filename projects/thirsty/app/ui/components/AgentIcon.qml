pragma ComponentBehavior: Bound
import QtQuick
import ".."

Item {
    id: root
    property string iconState: "running"
    property bool animationEnabled: true
    property int step: 0

    // State=running.svg: 4px cells on a 16px canvas, separated by 2px.
    // Clockwise perimeter order begins at the upper-left cell. At step zero,
    // source cells 1, 2 and 3 are black; the other five are #E1E1E1.
    readonly property var perimeter: [
        Qt.point(0, 0), Qt.point(6, 0), Qt.point(12, 0), Qt.point(12, 6),
        Qt.point(12, 12), Qt.point(6, 12), Qt.point(0, 12), Qt.point(0, 6)
    ]

    implicitWidth: Theme.componentsAgentIconWidth
    implicitHeight: Theme.componentsAgentIconHeight
    Accessible.ignored: true // The neighboring message supplies status text.

    Image {
        anchors.fill: parent
        visible: root.iconState !== "running" || !root.animationEnabled
        source: root.iconState === "error" ? Theme.agentErrorSource : Theme.agentRunningSource
        sourceSize.width: Theme.componentsAgentIconWidth
        sourceSize.height: Theme.componentsAgentIconHeight
        fillMode: Image.PreserveAspectFit
        smooth: false
        mipmap: false
        // Supplied originals are used for static running and error states.
        Accessible.ignored: true
    }

    Item {
        id: cells
        anchors.centerIn: parent
        width: Math.min(root.width, root.height)
        height: width
        visible: root.iconState === "running" && root.animationEnabled

        Repeater {
            model: root.perimeter.length
            Rectangle {
                required property int index
                readonly property int sourceCell: (index - root.step + 8) % 8
                x: root.perimeter[index].x * cells.width / 16
                y: root.perimeter[index].y * cells.height / 16
                width: cells.width / 4
                height: cells.height / 4
                color: sourceCell >= 1 && sourceCell <= 3
                       ? Theme.componentsAgentIconActiveColor
                       : Theme.componentsAgentIconInactiveColor
                antialiasing: false
                Accessible.ignored: true
            }
        }
    }

    Timer {
        interval: 100
        repeat: true
        running: root.visible && root.animationEnabled && root.iconState === "running"
        onTriggered: root.step = (root.step + 1) % 8
        onRunningChanged: {
            if (!running)
                root.step = 0;
        }
    }
}
