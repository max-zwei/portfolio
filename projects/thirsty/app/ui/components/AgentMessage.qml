import QtQuick
import ".."

Item {
    id: root

    // Transcript roles map explicitly: type/variant/text -> these nonreserved
    // names. Text is always literal Unicode, including emoji, never rich text.
    property string messageType: "output"
    property string messageVariant: "body"
    property string messageText: ""
    property bool animationEnabled: true

    // A single error row preserves config text: first line is the red headline,
    // everything after the first newline is the black body. Callers may override
    // either binding when their content already provides separate fields.
    readonly property int warningBreak: messageText.indexOf("\n")
    property string warningHeadline: warningBreak < 0 ? messageText : messageText.slice(0, warningBreak)
    property string warningBody: warningBreak < 0 ? "" : messageText.slice(warningBreak + 1)
    readonly property bool isWarning: messageType === "error" && messageVariant === "water_level"
    readonly property bool isAction: messageType === "action"
    readonly property bool isHeading: (messageType === "task" || messageType === "output")
                                      && messageVariant === "H1"
    readonly property real prefixWidth: isAction ? Theme.componentsAgentIconWidth + Theme.componentsAgentActionGap
                                       : isHeading ? headingMarker.implicitWidth + Theme.sizeM : 0

    implicitWidth: isWarning ? Math.max(warningHeadlineRow.implicitWidth, warningDescription.implicitWidth)
                            : prefixWidth + message.implicitWidth
    implicitHeight: isWarning ? warningContent.implicitHeight : message.implicitHeight

    Text {
        id: headingMarker
        visible: root.isHeading && !root.isWarning
        text: "#"
        textFormat: Text.PlainText
        color: message.color
        font: message.font
        lineHeight: message.lineHeight
        lineHeightMode: Text.ProportionalHeight
        Accessible.ignored: true
    }

    AgentIcon {
        visible: root.isAction && !root.isWarning
        iconState: root.messageVariant === "error" ? "error" : "running"
        animationEnabled: root.animationEnabled
        y: Math.round((message.font.pixelSize * message.lineHeight - height) / 2)
    }

    Text {
        id: message
        x: root.prefixWidth
        width: Math.max(0, root.width - x)
        visible: !root.isWarning
        text: root.messageText
        textFormat: Text.PlainText
        wrapMode: Text.Wrap
        color: root.messageType === "task" ? Theme.componentsAgentTaskTextColor
                                           : Theme.componentsAgentOutputTextColor
        font.family: Theme.fontFamily
        font.pixelSize: root.isAction ? Theme.componentsAgentActionTypographyFontSize
                        : root.messageType === "task" ? Theme.componentsAgentTaskTypographyFontSize
                        : Theme.componentsAgentOutputTypographyFontSize
        font.weight: root.isAction ? Theme.componentsAgentActionTypographyFontWeight
                     : root.messageType === "task" ? Theme.componentsAgentTaskTypographyFontWeight
                     : Theme.componentsAgentOutputTypographyFontWeight
        font.letterSpacing: root.isAction ? Theme.componentsAgentActionTypographyLetterSpacing
                            : root.messageType === "task" ? Theme.componentsAgentTaskTypographyLetterSpacing
                            : Theme.componentsAgentOutputTypographyLetterSpacing
        font.italic: root.isAction ? Theme.componentsAgentActionFontStyle === "italic"
                     : root.messageType === "task" && Theme.componentsAgentTaskFontStyle === "italic"
        lineHeight: root.isAction ? Theme.componentsAgentActionTypographyLineHeight
                    : root.messageType === "task" ? Theme.componentsAgentTaskTypographyLineHeight
                    : Theme.componentsAgentOutputTypographyLineHeight
        lineHeightMode: Text.ProportionalHeight
    }

    Column {
        id: warningContent
        visible: root.isWarning
        width: root.width
        spacing: Theme.componentsAgentErrorGap

        Item {
            id: warningHeadlineRow
            width: parent.width
            implicitWidth: warningIcon.width + Theme.sizeL + warningTitle.implicitWidth
            implicitHeight: Math.max(warningIcon.height, warningTitle.implicitHeight)

            FontMetrics {
                id: warningMetrics
                font: warningTitle.font
            }
            AgentIcon {
                id: warningIcon
                iconState: "error"
                y: Math.round((warningMetrics.height - height) / 2)
            }
            Text {
                id: warningTitle
                // Figma Running: icon x96..112, headline starts x128: 16px gap.
                x: warningIcon.width + Theme.sizeL
                width: Math.max(0, parent.width - x)
                text: root.warningHeadline
                textFormat: Text.PlainText
                wrapMode: Text.Wrap
                color: Theme.componentsAgentErrorTextColor
                font.family: Theme.fontFamily
                font.pixelSize: Theme.componentsAgentErrorTypographyFontSize
                font.weight: Theme.componentsAgentErrorTypographyFontWeight
                font.letterSpacing: Theme.componentsAgentErrorTypographyLetterSpacing
                // Natural font metrics: typography.warning has Auto line height.
            }
        }
        Text {
            id: warningDescription
            width: parent.width
            visible: text.length > 0
            text: root.warningBody
            textFormat: Text.PlainText
            wrapMode: Text.Wrap
            color: Theme.colorsPrimary
            font.family: Theme.fontFamily
            font.pixelSize: Theme.typographyBodyFontSize
            font.weight: Theme.typographyBodyFontWeight
            font.letterSpacing: Theme.typographyBodyLetterSpacing
            lineHeight: Theme.typographyBodyLineHeight
            lineHeightMode: Text.ProportionalHeight
        }
    }
}
