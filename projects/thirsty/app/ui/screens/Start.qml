import QtQuick
import ".."
import "../components"

FocusScope {
    id: root
    required property var experience
    objectName: "startScreen"

    Avatar {
        x: Theme.sizeXxl
        y: Theme.sizeXxl
    }

    Column {
        x: Theme.sizeXxl
        y: 435
        width: 869
        height: 189
        spacing: Theme.sizeL

        Text {
            width: parent.width
            text: root.experience.copy.start_title
            textFormat: Text.PlainText
            wrapMode: Text.Wrap
            color: Theme.colorsAction
            font.family: Theme.fontFamily
            font.pixelSize: Theme.typographyHeadingFontSize
            font.weight: Theme.typographyHeadingFontWeight
            font.letterSpacing: Theme.typographyHeadingLetterSpacing
        }
        Text {
            width: parent.width
            text: root.experience.copy.start_body
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
        Text {
            width: parent.width
            text: root.experience.copy.start_prompt
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
