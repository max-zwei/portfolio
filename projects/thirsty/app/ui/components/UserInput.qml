import QtQuick
import ".."

FocusScope {
    id: root

    property alias text: editor.text
    property string placeholderText: ""
    property string accessibleName: "Describe an app"
    property bool submissionEnabled: true
    readonly property bool inputMethodComposing: editor.inputMethodComposing
    readonly property bool canSubmit: enabled && submissionEnabled
                                      && !inputMethodComposing && text.trim().length > 0
    signal submitted(string text)
    signal activity()

    implicitWidth: Theme.componentsUserTextWidth
    implicitHeight: Theme.componentsUserTextHeight

    function normalizedText(value) {
        return value.replace(/[\r\n\u2028\u2029]+/g, " ");
    }

    // All activation paths share this guard. Validation errors and session
    // transitions belong to the controller/screen, not the editable component.
    function submit() {
        if (!canSubmit)
            return;
        activity();
        submitted(normalizedText(text).trim());
    }

    Rectangle {
        anchors.fill: parent
        color: Theme.colorsSurface
        radius: Theme.componentsUserTextRounded
        border.color: Theme.componentsUserTextBorderColor
        border.width: Theme.componentsUserTextBorderWidth
        antialiasing: false
    }
    Rectangle {
        // DESIGN's additional keyboard state, not a new source token. The 2px
        // stroke lies wholly outside the field and never changes its footprint.
        anchors.fill: parent
        anchors.margins: -2
        color: "transparent"
        border.color: Theme.colorsAction
        border.width: 2
        visible: editor.activeFocus
        antialiasing: false
    }

    TextInput {
        id: editor
        objectName: "ideaInput"
        anchors.fill: parent
        anchors.margins: Theme.componentsUserTextPadding
        focus: true
        activeFocusOnTab: true
        selectByMouse: true
        clip: true
        verticalAlignment: TextInput.AlignVCenter
        color: Theme.colorsPrimary
        selectionColor: Theme.colorsAction
        selectedTextColor: Theme.colorsPrimary
        font.family: Theme.fontFamily
        font.pixelSize: Theme.componentsUserTextTypographyFontSize
        font.weight: Theme.componentsUserTextTypographyFontWeight
        font.letterSpacing: Theme.componentsUserTextTypographyLetterSpacing
        // TextInput is single-line; its line is vertically centered in the
        // padded box. Multi-line body/task text uses proportional 1.2 spacing.
        Accessible.name: root.accessibleName
        Accessible.description: root.placeholderText

        onTextEdited: {
            const normalized = root.normalizedText(text);
            if (normalized !== text) {
                const normalizedCursor = root.normalizedText(text.slice(0, cursorPosition)).length;
                text = normalized;
                cursorPosition = normalizedCursor;
            }
            root.activity();
        }
        Keys.onPressed: function(event) {
            root.activity();
            if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter) {
                // Let the input method handle composition; never turn its
                // confirmation key into a visitor-session submission.
                event.accepted = !inputMethodComposing;
                if (!event.isAutoRepeat && !inputMethodComposing)
                    root.submit();
            }
        }
        TapHandler {
            onTapped: root.activity()
        }
    }

    Text {
        anchors.fill: editor
        visible: editor.text.length === 0 && !editor.inputMethodComposing
        text: root.placeholderText
        textFormat: Text.PlainText
        color: Theme.colorsPrimary
        font: editor.font
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
        Accessible.ignored: true
    }
}
