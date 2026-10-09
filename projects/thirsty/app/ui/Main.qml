pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Window
import "."
import "screens"

Window {
    id: window
    objectName: "mainWindow"

    // Integration supplies these through QQmlApplicationEngine.setInitialProperties.
    property int appWidth: 1280
    property int appHeight: 720
    property bool appFullscreen: false
    readonly property var experience: controller
    property bool enterHeld: false

    width: appWidth
    height: appHeight
    visible: true
    visibility: appFullscreen ? Window.FullScreen : Window.Windowed
    title: "thirsty"
    // A release may go to another application after focus loss. Autorepeat is
    // still rejected by the shortcut when this window becomes active again.
    onActiveChanged: {
        if (!active)
            enterHeld = false;
    }
    color: Theme.colorsSurface

    function releaseEnter(event) {
        if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter) {
            if (!event.isAutoRepeat)
                enterHeld = false;
            event.accepted = true;
        }
    }

    Shortcut {
        sequences: ["Return", "Enter"]
        context: Qt.WindowShortcut
        autoRepeat: false
        enabled: !inputScreen.visible || !inputScreen.inputMethodComposing
        onActivated: {
            if (window.enterHeld)
                return;
            window.enterHeld = true;
            window.experience.activity();
            if (window.experience.state === "start")
                window.experience.start();
            else if (window.experience.state === "input")
                inputScreen.submit();
            else if (window.experience.state === "finished")
                window.experience.reset();
        }
    }

    FocusScope {
        id: canvas
        width: 1280
        height: 720
        x: (window.width - width) / 2
        y: (window.height - height) / 2
        scale: Math.min(window.width / width, window.height / height)
        transformOrigin: Item.Center
        focus: true
        Keys.onReleased: function(event) { window.releaseEnter(event); }

        Start {
            anchors.fill: parent
            experience: window.experience
            visible: experience.state === "start"
            focus: visible
        }
        Input {
            id: inputScreen
            anchors.fill: parent
            experience: window.experience
            visible: experience.state === "input"
            onEnterReleased: function(event) { window.releaseEnter(event); }
        }
        Running {
            anchors.fill: parent
            experience: window.experience
            visible: experience.state !== "start" && experience.state !== "input"
            focus: visible
        }
    }
}
