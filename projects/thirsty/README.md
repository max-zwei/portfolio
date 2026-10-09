# thirsty

`thirsty` is an artwork built around a fake app-creating agent. A visitor describes an app through text chat, and the agent responds with staged development messages, such as “Working on creating the backend”. These messages are part of the performance: the agent is not actually writing code or building the requested app.

The chat is connected to a physical installation: a fake water-cooled server whose water drips away over time. Five physical switches detect the water level. When the water drops below the lowest switch, the agent interrupts its staged work and asks for a refill.

## Current status

- Native Python/PySide6/Qt Quick kiosk implemented, with real controller, mock/live sensor adapters, local script, original Figma assets, licensed local fonts and locally generated QR.
- Workstation evidence: 364 tests passed; 98 runtime theme values match DESIGN; native interaction/QR smoke and 100 accelerated QML/controller/mock sessions completed. See [validation](docs/validation.md) for methods and limits.
- Target hardware remains Raspberry Pi 3 Model A+, HDMI screen, Bluetooth keyboard and five JO-GL534 switches. **No physical Pi or installation checks have been performed.**
- Deployment and calibration tooling is implemented; hardware setup, service acceptance, physical calibration and installation soak remain blocked. Passive contacts, wet=1 polarity and configured pins remain unverified.
- Owner copy review is pending. The chosen QR URL is `https://zwei.berlin/app-repo`; redirect publication is pending and `output/app/` is empty.
- [PRODUCT.md](./PRODUCT.md) records all 11 issues and the blocking installation/approval checklist.
- User feedback sets the visitor-facing copy direction: use the submitted idea as the app description and only “Mobile App” as its generic name, with no fake/staged disclosure or PocketPlan branding. Begin with an output plan, then interleave task and action messages. This changes the performance's presentation, not its deterministic staged architecture.
- Visual feedback uses the nine supplied original SVG assets, 100ms running-dot animation, an action-colored Start heading, and a transcript inset 96px from the top/left with 96px below its viewport; the water indicator stays fixed. Post-feedback verification passed 364 tests in 2.69 seconds and a warning-free native Cocoa QML journey; geometry, animation and Start/plan visuals were checked. The 100-session report above is earlier evidence, not a rerun of the feedback changes; see [validation](docs/validation.md#user-feedback-verification).

## Experience

1. **Start.** Press ENTER on the Bluetooth keyboard.
2. **Describe an app.** Enter an idea and submit with ENTER.
3. **Follow the staged work.** Messages appear in a scrolling transcript; the water indicator stays fixed.
4. **Refill.** At water level 0, progress pauses. Default: resume at the same position after level ≥1 remains valid for two seconds.
5. **Receive the output.** Read the staged-work summary and scan a QR code linking to a pre-existing app repository.
6. **Next visitor.** Default: ENTER or 60 seconds after completion returns to Start.

Refill and reset timings are configurable defaults to tune during installation. Real sensing and physical water depletion control a deterministic performance; no app, code or repository is generated.

## Run the native application

From this project directory, with Python 3.11 or newer:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
python -m app --mode mock
```

This launches the complete native kiosk with mock sensing, not a browser, shell or stub. Use `python -m app --mode mock --fullscreen` for fullscreen, or `thirsty --mode mock` after installation. ENTER starts the visitor journey. Configuration defaults resolve from this directory; `--device` and `--script` accept explicit configuration paths. `python -m app --help` lists options, including `--mock-file` for externally controlled mock readings. Use `python -m app`, not `python -m app.main`.

**Safe default:** mock mode without a readings file starts with unknown sensing and pauses when an idea is submitted. It does not assume a full tank. For a complete interactive demo, create an explicit full-tank reading and launch:

```sh
printf '%s\n' '{"raw_bits":[1,1,1,1,1]}' > /tmp/thirsty-sensors.json
python -m app --mode mock --mock-file /tmp/thirsty-sensors.json
```

In a second terminal, simulate draining below the lowest switch:

```sh
printf '%s\n' '{"raw_bits":[0,0,0,0,0]}' > /tmp/thirsty-sensors.json
```

Then simulate a refill to level 1:

```sh
printf '%s\n' '{"raw_bits":[1,0,0,0,0]}' > /tmp/thirsty-sensors.json
```

Allow the default 200 ms pattern stabilization plus the two-second valid-water hold before progress resumes. These are physical raw bits ordered bottom → top under the provisional wet=1 polarity, not a calibrated hardware claim. The script takes 120 seconds of active progress, excluding water/sensor pauses; completion shows the summary and QR, and ENTER resets for the next visitor.

To run the software suite: `python -m pytest`. These are reproducible commands, not a claim that this documentation edit ran them.

Live mode is explicit (`--mode live`), requires GPIO dependencies and verified device settings, and never silently falls back to mock readings. Do not connect unverified sensors or treat workstation launch as approval to apply deployment changes. Follow [device setup](docs/device.md), [systemd deployment](deploy/systemd/README.md) and [operator procedures](docs/operator.md) for guarded installation and calibration.

The runtime has no cloud dependency: all script, assets and QR generation are local. Opening the QR destination still requires the visitor's phone to have connectivity and the pending redirect/destination to be published.

### macOS: installed Cocoa plugin is not found

If Qt reports `Could not find the Qt platform plugin "cocoa"`, an installed plugin may have macOS's hidden-file flag set. This occurred in the local virtual environment: Qt excluded the hidden plugin from discovery. Clearing that flag restored native startup without reinstalling Qt:

```sh
chflags -R nohidden .venv
.venv/bin/python -m app --mode mock --mock-file /tmp/thirsty-sensors.json
```

This changes file visibility flags only inside the virtual environment; it does not remove quarantine attributes or alter system security settings. The `.venv` directory remains a dot-directory. Other causes of the same error require checking the installed Qt plugin and its dependencies rather than assuming this fix applies.

## Technology and architecture

| Part        | Selected direction                                                                                        |
| ----------- | --------------------------------------------------------------------------------------------------------- |
| OS          | Raspberry Pi OS Lite, 32-bit                                                                              |
| Application | One Python 3 process; Qt event loop                                                                       |
| Interface   | PySide6 / Qt Quick / QML; fullscreen HDMI; three Figma screens                                            |
| Sensors     | GPIO Zero; five digital inputs; normalized water levels 0–5                                               |
| Input       | Bluetooth keyboard; OS pairing/trust and physical reconnect acceptance pending                            |
| Content     | Local JSON messages, timings, settings and repository URL                                                 |
| Design      | Full DESIGN token mapping in `Theme.qml` (not CSS); local JetBrains Mono fonts and original Figma artwork |
| Startup     | systemd autostart and restart-on-failure                                                                  |

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
- [PRODUCT.md](./PRODUCT.md): implementation status, shared contracts and outstanding device acceptance.
- [docs/validation.md](./docs/validation.md): exercised workstation evidence, screenshots and physical acceptance limits.
- [docs/operator.md](./docs/operator.md): calibration, recovery and installation procedures.
- [docs/copy-review.md](./docs/copy-review.md): copy review and remaining owner approval.
- `config/script-provenance.json`: source-event/quote provenance for the authored performance.
- `app/assets/provenance.json`: original Figma exports and bundled font provenance; font notices remain with the assets.
- [Figma Interface](https://www.figma.com/design/Vly8oZbSYachZu9ecP58h8/thirsty?node-id=0-1): Start, Input and Running layouts.
- [Figma Design System](https://www.figma.com/design/Vly8oZbSYachZu9ecP58h8/thirsty?node-id=9-214): reusable visual components.

## License

A project license has not been specified. This documentation does not establish permission to reuse the code, documentation, design or original Figma artwork. Bundled JetBrains Mono fonts retain their applicable SIL Open Font License notices; font licensing does not license the artwork or project as a whole.
