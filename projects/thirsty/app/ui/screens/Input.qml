import QtQuick
import ".."
import "../components"

FocusScope {
    id: root
    required property var experience
    objectName: "inputScreen"
    property alias text: input.text
    property alias inputField: input
    property alias submitButton: button
    readonly property bool inputMethodComposing: input.inputMethodComposing
    signal enterReleased(var event)

    function submit() {
        input.submit();
    }

    onVisibleChanged: {
        if (visible) {
            input.text = experience.idea;
            input.forceActiveFocus(Qt.OtherFocusReason);
        }
    }
    Component.onCompleted: {
        if (visible)
            input.forceActiveFocus(Qt.OtherFocusReason);
    }

    Column {
        x: Theme.sizeXxl
        y: Theme.sizeXxl
        width: root.width - 2 * Theme.sizeXxl
        spacing: Theme.sizeL

        Text {
            width: parent.width
            text: root.experience.copy.input_title
            textFormat: Text.PlainText
            wrapMode: Text.Wrap
            color: Theme.colorsPrimary
            font.family: Theme.fontFamily
            font.pixelSize: Theme.typographyHeadingFontSize
            font.weight: Theme.typographyHeadingFontWeight
            font.letterSpacing: Theme.typographyHeadingLetterSpacing
        }
        Text {
            width: parent.width
            text: root.experience.copy.input_prompt
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

    Text {
        x: Theme.sizeXxl
        y: controls.y - height - Theme.sizeL
        width: controls.width
        text: root.experience.validationError
        visible: text.length > 0
        textFormat: Text.PlainText
        wrapMode: Text.Wrap
        color: Theme.colorsError
        font.family: Theme.fontFamily
        font.pixelSize: Theme.typographyBodyFontSize
        font.weight: Theme.typographyBodyFontWeight
        font.letterSpacing: Theme.typographyBodyLetterSpacing
        lineHeight: Theme.typographyBodyLineHeight
        lineHeightMode: Text.ProportionalHeight
    }

    Row {
        id: controls
        x: Theme.sizeXxl
        y: 562
        width: root.width - 2 * Theme.sizeXxl
        spacing: Theme.sizeL

        UserInput {
            id: input
            width: controls.width - button.width - controls.spacing
            placeholderText: root.experience.copy.input_placeholder
            accessibleName: root.experience.copy.input_title
            submissionEnabled: root.visible && root.experience.state === "input"
            onSubmitted: function(text) { root.experience.submit(text); }
            onActivity: root.experience.activity()
            Keys.onReleased: function(event) { root.enterReleased(event); }
        }
        SubmitButton {
            id: button
            submissionText: input.text
            submissionEnabled: input.submissionEnabled
            compositionActive: input.inputMethodComposing
            accessibleName: root.experience.copy.input_submit_label
            onSubmitted: input.submit()
            onActivity: root.experience.activity()
            Keys.onReleased: function(event) {
                root.enterReleased(event);
                if (event.key === Qt.Key_Space)
                    event.accepted = true;
            }
        }
    }
}
