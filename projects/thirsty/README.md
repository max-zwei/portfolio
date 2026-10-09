# thirsty

`thirsty` is an artwork built around a fake app-creating agent. A visitor describes an app through text chat, and the agent responds with staged development messages, such as “Working on creating the backend”. These messages are part of the performance: the agent is not actually writing code or building the requested app.

The chat is connected to a physical installation: a fake water-cooled server whose water drips away over time. Five physical switches detect the water level. When the water drops below the lowest switch, the agent interrupts its staged work and asks for a refill.

## Current status

- Architecture selected; implementation not started.
- Hardware: Raspberry Pi 3 Model A+, HDMI screen, Bluetooth keyboard, five JO-GL534 switches.
- Passive switches and wet=1 are working assumptions, pending physical testing.
- [PRODUCT.md](./PRODUCT.md) contains implementation issues, dependencies, defaults and acceptance checks.

## Experience

1. **Start.** Press ENTER on the Bluetooth keyboard.
2. **Describe an app.** Enter an idea and submit with ENTER.
3. **Follow the staged work.** Messages appear in a scrolling transcript; the water indicator stays fixed.
4. **Refill.** At water level 0, progress pauses. Default: resume at the same position after level ≥1 remains valid for two seconds.
5. **Receive the output.** Read the staged-work summary and scan a QR code linking to a pre-existing app repository.
6. **Next visitor.** Default: ENTER or 60 seconds after completion returns to Start.

Refill and reset timings are configurable defaults to tune during installation. Real sensing and physical water depletion control a deterministic performance; no app, code or repository is generated.

## Technology and architecture

| Part        | Selected direction                                                                |
| ----------- | --------------------------------------------------------------------------------- |
| OS          | Raspberry Pi OS Lite, 32-bit                                                      |
| Application | One Python 3 process; Qt event loop                                               |
| Interface   | PySide6 / Qt Quick / QML; fullscreen HDMI; three Figma screens                    |
| Sensors     | GPIO Zero; five digital inputs; normalized water levels 0–5                       |
| Input       | Bluetooth keyboard paired and trusted in the OS; reconnect verified on the device |
| Content     | Local JSON messages, timings, settings and repository URL                         |
| Design      | DESIGN tokens mapped to QML; local JetBrains Mono fonts and Figma artwork         |
| Startup     | systemd autostart and restart-on-failure                                          |

- Sensor reader → experience controller → interface; keyboard actions return to the controller.
- Prefer Qt's direct fullscreen display backend; verify compatibility and memory use on the 512 MB Pi before deployment.
- All visitor interaction runs offline. Wi-Fi is optional for maintenance; Bluetooth stays enabled.
- The QR code is generated locally. Visitors need connectivity on their phones to open its destination.
- Session state stays in memory; process restart or power loss returns to Start.

## Sensor wiring assumption

- Each sensor: passive two-wire contact, to be verified before connection.
- Circuit: **Pi 3.3 V → switch → GPIO input with pull-down**; GPIO inputs must not receive 5 V.
- Initial polarity: closed/wet = 1; open/dry = 0. Configure inversion per switch after testing.
- Order switches bottom → top; accept only continuous wet levels from the bottom.
- Level 0 means below the lowest switch; it does not prove the container has no residual water.
- Wiring, filtering, calibration and fault handling: [PRODUCT.md §4](./PRODUCT.md#4-sensor-assumptions-and-calibration).

## Bill of materials

| Category          | Item                              | Details / source                                                                                                                                                                                                                                                          |
| ----------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Display           | HDMI screen                       | Target interface: 1280 × 720, 16:9; exact screen and supported mode to verify                                                                                                                                                                                             |
| Input             | Bluetooth keyboard                | Visitor text input; layout, power and reconnect behavior to verify                                                                                                                                                                                                        |
| Computing         | Raspberry Pi 3 Model A+           | 512 MB RAM; onboard Bluetooth; HDMI output                                                                                                                                                                                                                                |
| Power and storage | Pi power supply and microSD card  | Pi specification: 5 V / 2.5 A via micro USB; exact supply/card and screen power arrangement to confirm                                                                                                                                                                    |
| Sensing           | 5 × JO-GL534 water-level switches | Supplied ratings, unverified: 10 W max switching power; DC 100 V max switching voltage; 0.5 A max switching current; DC 220 V max breakdown voltage; PP; operating temperature −10–85 °C; max temperature resistance 85 °C. Contact ratings are not GPIO supply voltages. |
| Wiring            | Leads and connectors              | Five GPIO inputs with pull-downs; final pin map and cable behavior to verify                                                                                                                                                                                              |
| Server enclosure  | 3D-printed server rack            | [MicroLab mini modular home server rack — print files](https://www.printables.com/model/1173286-microlab-mini-modular-home-server-rack/files)                                                                                                                             |
| Server enclosure  | LAN cables                        | For the server-rack assembly                                                                                                                                                                                                                                              |
| Water containers  | Transparent upper box             | Eurobox                                                                                                                                                                                                                                                                   |
| Water containers  | Black lower box                   | Eurobox                                                                                                                                                                                                                                                                   |
| Refilling         | Watering can                      | For refilling the installation                                                                                                                                                                                                                                            |

Sources: [Pi 3 A+ specifications](https://datasheets.raspberrypi.com/rpi3/raspberry-pi-3-a-plus-product-brief.pdf), [GPIO Zero switch wiring](https://gpiozero.readthedocs.io/en/stable/api_input.html#button). Sourcing links and supplied sensor ratings do not establish tested installation compatibility.

## Documentation

- [DESIGN.md](./DESIGN.md): visual tokens, Figma references and QML mapping.
- [PRODUCT.md](./PRODUCT.md): orchestrator-ready implementation backlog, shared contracts and device acceptance.
- [Figma Interface](https://www.figma.com/design/Vly8oZbSYachZu9ecP58h8/thirsty?node-id=0-1): Start, Input and Running layouts.
- [Figma Design System](https://www.figma.com/design/Vly8oZbSYachZu9ecP58h8/thirsty?node-id=9-214): reusable visual components.

## License

A project license has not been specified. This documentation does not establish permission to reuse the code, documentation, design or artwork. Bundled third-party fonts and assets must retain their applicable license notices.
