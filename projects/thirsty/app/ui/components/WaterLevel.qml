pragma ComponentBehavior: Bound
import QtQuick
import ".."

Rectangle {
    id: root

    // Only stabilized controller values enter this component; no GPIO decoding.
    property var level: null
    property string sensorStatus: "unknown"
    property string accessibleName: "Water level"
    readonly property bool knownLevel: sensorStatus === "ok"
                                       && typeof level === "number"
                                       && Number.isInteger(level)
                                       && level >= 0 && level <= 5

    implicitWidth: Theme.componentsWaterLevelWidth
    implicitHeight: Theme.componentsWaterLevelHeight
    color: Theme.colorsSurface
    radius: Theme.componentsWaterLevelRounded
    border.width: knownLevel ? 0 : Theme.componentsWaterLevelBorderWidth
    border.color: Theme.componentsWaterLevelBorderColor
    antialiasing: false

    Accessible.role: Accessible.Indicator
    Accessible.name: accessibleName
    Accessible.description: knownLevel ? String(level) + " / 5" : sensorStatus

    Image {
        anchors.fill: parent
        visible: root.knownLevel
        source: root.knownLevel
                ? Qt.resolvedUrl("../../assets/icons/water-level-" + root.level + ".svg") : ""
        sourceSize.width: Math.round(width)
        sourceSize.height: Math.round(height)
        fillMode: Image.PreserveAspectFit
        smooth: false
        mipmap: false
        Accessible.ignored: true
    }

    Text {
        anchors.centerIn: parent
        visible: !root.knownLevel
        text: "?"
        textFormat: Text.PlainText
        color: Theme.colorsPrimary
        font.family: Theme.fontFamily
        font.pixelSize: Theme.typographyHeadingFontSize
        font.weight: Theme.typographyHeadingFontWeight
        font.letterSpacing: Theme.typographyHeadingLetterSpacing
    }
    // Sensor-status copy and its red treatment belong to the containing screen.
}
