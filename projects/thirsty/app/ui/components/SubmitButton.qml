import QtQuick
import ".."

Item {
    id: root
    objectName: "submitButton"

    property string submissionText: ""
    property bool submissionEnabled: true
    property bool compositionActive: false
    property string accessibleName: "Submit app idea"
    readonly property bool canSubmit: enabled && submissionEnabled && !compositionActive
                                      && submissionText.trim().length > 0
    signal submitted(string text)
    signal activity()

    implicitWidth: Theme.componentsUserButtonWidth
    implicitHeight: Theme.componentsUserButtonHeight
    enabled: submissionEnabled && !compositionActive && submissionText.trim().length > 0
    activeFocusOnTab: true

    function submit() {
        if (!canSubmit)
            return;
        activity();
        submitted(submissionText.replace(/[\r\n\u2028\u2029]+/g, " ").trim());
    }

    Accessible.role: Accessible.Button
    Accessible.name: accessibleName
    Accessible.onPressAction: root.submit()

    Rectangle {
        anchors.fill: parent
        color: root.canSubmit ? Theme.componentsUserButtonBackgroundColor : Theme.colorsSecondary
        radius: Theme.componentsUserButtonRounded
        border.width: Theme.componentsUserButtonBorderWidth
        border.color: Theme.componentsUserButtonBorderColor
        antialiasing: false
    }
    Rectangle {
        // External 2px focus state specified in DESIGN, not an invented token.
        anchors.fill: parent
        anchors.margins: -2
        visible: root.activeFocus
        color: "transparent"
        border.width: 2
        border.color: Theme.colorsAction
        antialiasing: false
    }
    Text {
        anchors.fill: parent
        anchors.margins: Theme.componentsUserButtonPadding
        text: ">"
        textFormat: Text.PlainText
        color: Theme.componentsUserButtonTextColor
        font.family: Theme.fontFamily
        font.pixelSize: Theme.componentsUserButtonTypographyFontSize
        font.weight: Theme.componentsUserButtonTypographyFontWeight
        font.letterSpacing: Theme.componentsUserButtonTypographyLetterSpacing
        lineHeight: Theme.componentsUserButtonTypographyLineHeight
        lineHeightMode: Text.ProportionalHeight
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        Accessible.ignored: true
    }
    MouseArea {
        anchors.fill: parent
        onPressed: {
            root.forceActiveFocus(Qt.MouseFocusReason);
            root.activity();
        }
        onClicked: root.submit()
    }
    Keys.onPressed: function(event) {
        root.activity();
        if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter || event.key === Qt.Key_Space) {
            event.accepted = true;
            if (!event.isAutoRepeat)
                root.submit();
        }
    }
    Keys.onReleased: function(event) {
        // There is deliberately no second, key-release activation path.
        if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter || event.key === Qt.Key_Space)
            event.accepted = true;
    }
}
