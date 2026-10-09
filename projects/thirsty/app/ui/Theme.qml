pragma Singleton
import QtQuick

QtObject {
    id: theme

    // Naming: flatten each DESIGN.md YAML path to lower camelCase, retaining
    // the components prefix; '-' and '_' delimit words. Whole typography-role
    // aliases expand into one property per scalar, with their source paths below.
    // px -> reference-canvas numbers; 400 -> Font.Normal; 0em -> zero pixels.
    // Auto line heights are deliberately absent. Italic is component-owned.
    readonly property color colorsPrimary: "#000000" // colors.primary
    readonly property color colorsSurface: "#FFFFFF" // colors.surface
    readonly property color colorsSecondary: "#E1E1E1" // colors.secondary
    readonly property color colorsWater: "#0000FF" // colors.water
    readonly property color colorsError: "#FF0000" // colors.error
    readonly property color colorsAction: "#FF00FF" // colors.action

    readonly property string typographyHeadingFontFamily: "JetBrains Mono" // typography.heading.fontFamily
    readonly property int typographyHeadingFontSize: sizeXl // typography.heading.fontSize -> size.xl
    readonly property int typographyHeadingFontWeight: Font.Normal // typography.heading.fontWeight: 400
    readonly property real typographyHeadingLetterSpacing: 0 // typography.heading.letterSpacing: 0em
    readonly property string typographyBodyFontFamily: "JetBrains Mono" // typography.body.fontFamily
    readonly property int typographyBodyFontSize: sizeL // typography.body.fontSize -> size.l
    readonly property int typographyBodyFontWeight: Font.Normal // typography.body.fontWeight: 400
    readonly property real typographyBodyLineHeight: 1.2 // typography.body.lineHeight (proportional)
    readonly property real typographyBodyLetterSpacing: 0 // typography.body.letterSpacing: 0em
    readonly property string typographyTaskFontFamily: "JetBrains Mono" // typography.task.fontFamily
    readonly property int typographyTaskFontSize: sizeL // typography.task.fontSize -> size.l
    readonly property int typographyTaskFontWeight: Font.Normal // typography.task.fontWeight: 400
    readonly property real typographyTaskLineHeight: 1.2 // typography.task.lineHeight (proportional)
    readonly property real typographyTaskLetterSpacing: 0 // typography.task.letterSpacing: 0em
    readonly property string typographyWarningFontFamily: "JetBrains Mono" // typography.warning.fontFamily
    readonly property int typographyWarningFontSize: 20 // typography.warning.fontSize: 20px
    readonly property int typographyWarningFontWeight: Font.Normal // typography.warning.fontWeight: 400
    readonly property real typographyWarningLetterSpacing: 0 // typography.warning.letterSpacing: 0em

    readonly property int roundedNone: 0 // rounded.none: 0px
    readonly property int sizeS: 4 // size.s: 4px
    readonly property int sizeM: 8 // size.m: 8px
    readonly property int sizeL: 16 // size.l: 16px
    readonly property int sizeXl: 40 // size.xl: 40px
    readonly property int sizeXxl: 96 // size.xxl: 96px

    readonly property int componentsWaterLevelWidth: 94 // components.water_level.width: 94px
    readonly property int componentsWaterLevelHeight: 94 // components.water_level.height: 94px
    readonly property int componentsWaterLevelPadding: 2 // components.water_level.padding: 2px
    readonly property int componentsWaterLevelRounded: roundedNone // components.water_level.rounded -> rounded.none
    readonly property color componentsWaterLevelBorderColor: colorsPrimary // components.water_level.borderColor -> colors.primary
    readonly property int componentsWaterLevelBorderWidth: 2 // components.water_level.borderWidth: 2px
    readonly property color componentsWaterLevelActiveColor: colorsWater // components.water_level.activeColor -> colors.water
    readonly property color componentsWaterLevelEmptyColor: colorsError // components.water_level.emptyColor -> colors.error

    readonly property int componentsAgentIconWidth: sizeL // components.agent_icon.width -> size.l
    readonly property int componentsAgentIconHeight: sizeL // components.agent_icon.height -> size.l
    readonly property color componentsAgentIconActiveColor: colorsPrimary // components.agent_icon.activeColor -> colors.primary
    readonly property color componentsAgentIconInactiveColor: colorsSecondary // components.agent_icon.inactiveColor -> colors.secondary
    readonly property color componentsAgentIconErrorColor: colorsError // components.agent_icon.errorColor -> colors.error

    readonly property string componentsAgentTaskTypographyFontFamily: typographyTaskFontFamily // components.agent-task.typography.fontFamily -> typography.task.fontFamily
    readonly property int componentsAgentTaskTypographyFontSize: typographyTaskFontSize // components.agent-task.typography.fontSize -> typography.task.fontSize -> size.l
    readonly property int componentsAgentTaskTypographyFontWeight: typographyTaskFontWeight // components.agent-task.typography.fontWeight -> typography.task.fontWeight
    readonly property real componentsAgentTaskTypographyLineHeight: typographyTaskLineHeight // components.agent-task.typography.lineHeight -> typography.task.lineHeight
    readonly property real componentsAgentTaskTypographyLetterSpacing: typographyTaskLetterSpacing // components.agent-task.typography.letterSpacing -> typography.task.letterSpacing
    readonly property color componentsAgentTaskTextColor: colorsPrimary // components.agent-task.textColor -> colors.primary
    readonly property string componentsAgentTaskFontStyle: "italic" // components.agent-task.fontStyle

    readonly property string componentsAgentActionTypographyFontFamily: typographyTaskFontFamily // components.agent-action.typography.fontFamily -> typography.task.fontFamily
    readonly property int componentsAgentActionTypographyFontSize: typographyTaskFontSize // components.agent-action.typography.fontSize -> typography.task.fontSize -> size.l
    readonly property int componentsAgentActionTypographyFontWeight: typographyTaskFontWeight // components.agent-action.typography.fontWeight -> typography.task.fontWeight
    readonly property real componentsAgentActionTypographyLineHeight: typographyTaskLineHeight // components.agent-action.typography.lineHeight -> typography.task.lineHeight
    readonly property real componentsAgentActionTypographyLetterSpacing: typographyTaskLetterSpacing // components.agent-action.typography.letterSpacing -> typography.task.letterSpacing
    readonly property string componentsAgentActionFontStyle: "italic" // components.agent-action.fontStyle
    readonly property int componentsAgentActionGap: sizeL // components.agent-action.gap -> size.l

    readonly property string componentsAgentErrorTypographyFontFamily: typographyWarningFontFamily // components.agent-error.typography.fontFamily -> typography.warning.fontFamily
    readonly property int componentsAgentErrorTypographyFontSize: typographyWarningFontSize // components.agent-error.typography.fontSize -> typography.warning.fontSize
    readonly property int componentsAgentErrorTypographyFontWeight: typographyWarningFontWeight // components.agent-error.typography.fontWeight -> typography.warning.fontWeight
    readonly property real componentsAgentErrorTypographyLetterSpacing: typographyWarningLetterSpacing // components.agent-error.typography.letterSpacing -> typography.warning.letterSpacing
    readonly property color componentsAgentErrorTextColor: colorsError // components.agent-error.textColor -> colors.error
    readonly property int componentsAgentErrorGap: sizeM // components.agent-error.gap -> size.m

    readonly property string componentsAgentOutputTypographyFontFamily: typographyBodyFontFamily // components.agent-output.typography.fontFamily -> typography.body.fontFamily
    readonly property int componentsAgentOutputTypographyFontSize: typographyBodyFontSize // components.agent-output.typography.fontSize -> typography.body.fontSize -> size.l
    readonly property int componentsAgentOutputTypographyFontWeight: typographyBodyFontWeight // components.agent-output.typography.fontWeight -> typography.body.fontWeight
    readonly property real componentsAgentOutputTypographyLineHeight: typographyBodyLineHeight // components.agent-output.typography.lineHeight -> typography.body.lineHeight
    readonly property real componentsAgentOutputTypographyLetterSpacing: typographyBodyLetterSpacing // components.agent-output.typography.letterSpacing -> typography.body.letterSpacing
    readonly property color componentsAgentOutputTextColor: colorsPrimary // components.agent-output.textColor -> colors.primary

    readonly property int componentsUserTextWidth: 931 // components.user-text.width: 931px
    readonly property int componentsUserTextHeight: 62 // components.user-text.height: 62px
    readonly property string componentsUserTextTypographyFontFamily: typographyBodyFontFamily // components.user-text.typography.fontFamily -> typography.body.fontFamily
    readonly property int componentsUserTextTypographyFontSize: typographyBodyFontSize // components.user-text.typography.fontSize -> typography.body.fontSize -> size.l
    readonly property int componentsUserTextTypographyFontWeight: typographyBodyFontWeight // components.user-text.typography.fontWeight -> typography.body.fontWeight
    readonly property real componentsUserTextTypographyLineHeight: typographyBodyLineHeight // components.user-text.typography.lineHeight -> typography.body.lineHeight
    readonly property real componentsUserTextTypographyLetterSpacing: typographyBodyLetterSpacing // components.user-text.typography.letterSpacing -> typography.body.letterSpacing
    readonly property int componentsUserTextPadding: sizeL // components.user-text.padding -> size.l
    readonly property int componentsUserTextRounded: roundedNone // components.user-text.rounded -> rounded.none
    readonly property color componentsUserTextBorderColor: colorsPrimary // components.user-text.borderColor -> colors.primary
    readonly property int componentsUserTextBorderWidth: 2 // components.user-text.borderWidth: 2px

    readonly property int componentsUserButtonWidth: 46 // components.user-button.width: 46px
    readonly property int componentsUserButtonHeight: 62 // components.user-button.height: 62px
    readonly property string componentsUserButtonTypographyFontFamily: typographyBodyFontFamily // components.user-button.typography.fontFamily -> typography.body.fontFamily
    readonly property int componentsUserButtonTypographyFontSize: typographyBodyFontSize // components.user-button.typography.fontSize -> typography.body.fontSize -> size.l
    readonly property int componentsUserButtonTypographyFontWeight: typographyBodyFontWeight // components.user-button.typography.fontWeight -> typography.body.fontWeight
    readonly property real componentsUserButtonTypographyLineHeight: typographyBodyLineHeight // components.user-button.typography.lineHeight -> typography.body.lineHeight
    readonly property real componentsUserButtonTypographyLetterSpacing: typographyBodyLetterSpacing // components.user-button.typography.letterSpacing -> typography.body.letterSpacing
    readonly property color componentsUserButtonBackgroundColor: colorsAction // components.user-button.backgroundColor -> colors.action
    readonly property color componentsUserButtonTextColor: colorsPrimary // components.user-button.textColor -> colors.primary
    readonly property int componentsUserButtonPadding: sizeL // components.user-button.padding -> size.l
    readonly property int componentsUserButtonRounded: roundedNone // components.user-button.rounded -> rounded.none
    readonly property color componentsUserButtonBorderColor: colorsPrimary // components.user-button.borderColor -> colors.primary
    readonly property int componentsUserButtonBorderWidth: 2 // components.user-button.borderWidth: 2px

    readonly property int componentsAvatarWidth: 208 // components.avatar.width: 208px
    readonly property int componentsAvatarHeight: 149 // components.avatar.height: 149px
    readonly property color componentsAvatarColor: colorsPrimary // components.avatar.color -> colors.primary
    readonly property int componentsQrCodeWidth: 208 // components.qr_code.width: 208px
    readonly property int componentsQrCodeHeight: 208 // components.qr_code.height: 208px

    // Runtime resources, not additional YAML tokens. Resolve relative to THIS
    // singleton rather than a screen/component's directory. Both faces retain
    // the normal family name; font.italic selects the bundled italic face.
    readonly property FontLoader regularFont: FontLoader {
        source: Qt.resolvedUrl("../assets/fonts/JetBrainsMono-Regular.ttf")
    }
    readonly property FontLoader italicFont: FontLoader {
        source: Qt.resolvedUrl("../assets/fonts/JetBrainsMono-Italic.ttf")
    }
    readonly property string fontFamily: regularFont.status === FontLoader.Ready
                                         ? regularFont.name : "monospace"
    readonly property url avatarSource: Qt.resolvedUrl("../assets/icons/avatar.svg")
    readonly property url agentRunningSource: Qt.resolvedUrl("../assets/icons/agent-running.svg")
    readonly property url agentErrorSource: Qt.resolvedUrl("../assets/icons/agent-error.svg")
}
