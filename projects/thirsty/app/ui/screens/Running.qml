pragma ComponentBehavior: Bound
import QtQuick
import ".."
import "../components"

FocusScope {
    id: root
    required property var experience
    objectName: "runningScreen"

    function scrollToLatest() {
        // Repeater insertion and wrapped text polish can settle on separate
        // turns. Content-height changes schedule this same final positioning.
        Qt.callLater(function() {
            transcript.contentY = Math.max(0, transcript.contentHeight - transcript.height);
        });
    }

    onVisibleChanged: {
        if (visible)
            scrollToLatest();
    }

    Flickable {
        id: transcript
        objectName: "transcriptView"
        x: Theme.sizeXxl
        y: Theme.sizeXxl
        width: 952
        height: root.height - 2 * Theme.sizeXxl
        clip: true
        contentWidth: width
        contentHeight: messages.implicitHeight
        flickableDirection: Flickable.VerticalFlick
        boundsBehavior: Flickable.StopAtBounds
        Accessible.name: root.experience.copy.running_title
        onContentHeightChanged: root.scrollToLatest()

        Column {
            id: messages
            width: transcript.width
            spacing: Theme.sizeL

            Repeater {
                model: root.experience.transcript
                onItemAdded: root.scrollToLatest()
                onItemRemoved: root.scrollToLatest()

                AgentMessage {
                    required property var model
                    width: messages.width
                    messageType: model.type
                    messageVariant: model.variant
                    messageText: model.text
                    animationEnabled: root.experience.state === "running"
                                      && y + height > transcript.contentY
                                      && y < transcript.contentY + transcript.height
                }
            }

            Column {
                width: messages.width
                visible: root.experience.state === "finished"
                spacing: Theme.sizeL
                onVisibleChanged: root.scrollToLatest()

                RepositoryHandoff {
                    width: parent.width
                    qrSource: root.experience.qrSource
                    repositoryUrl: root.experience.repositoryUrl
                    label: root.experience.copy.repository_label
                }
                Text {
                    width: parent.width
                    text: root.experience.copy.finished_prompt
                    textFormat: Text.PlainText
                    wrapMode: Text.Wrap
                    color: Theme.colorsAction
                    font.family: Theme.fontFamily
                    font.pixelSize: Theme.typographyBodyFontSize
                    font.weight: Theme.typographyBodyFontWeight
                    font.letterSpacing: Theme.typographyBodyLetterSpacing
                    lineHeight: Theme.typographyBodyLineHeight
                    lineHeightMode: Text.ProportionalHeight
                }
            }
        }
    }

    WaterLevel {
        objectName: "waterIndicator"
        x: 1088
        y: Theme.sizeXxl
        width: Theme.sizeXxl
        height: Theme.sizeXxl
        level: root.experience.waterLevel
        sensorStatus: root.experience.sensorStatus
        accessibleName: root.experience.copy.water_label
                        + (sensorStatus === "unknown" ? ": " + root.experience.copy.sensor_unknown_label
                           : sensorStatus === "fault" ? ": " + root.experience.copy.sensor_fault_label : "")
    }
}
