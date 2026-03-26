# Big Bird Pi 5 Art Installation — Hardware Spec & Compatibility Sheet

**Status: ✅ ALL GREENLIT — No blocking issues remain.**

This document is the definitive hardware reference for a Raspberry Pi 5 art installation housed inside a Big Bird plush puppet. Every component has been spec-checked and cross-verified for compatibility. Hand this to Claude Code as the source of truth for wiring, GPIO pin assignments, software configuration, and physical integration.

---

## Project overview

An interactive Big Bird puppet powered by a Raspberry Pi 5. The puppet sees visitors via a camera, speaks through a small speaker, displays content on a 7″ screen, and responds to a large arcade button press. All electronics are housed inside or mounted to the puppet body.

---

## Complete parts list (17 components)

### Amazon cart (14 items)

| # | Product | ASIN | Role | ~Price |
|---|---------|------|------|--------|
| 1 | Jay Franco Weighted Sesame Street Big Bird Plush | B0DJC7WLXW | Enclosure / puppet shell | ~$25 |
| 2 | GeeekPi 7″ 1024×600 IPS Display (non-touch) | B0CHRD7CQ3 | Visual output | ~$37 |
| 3 | EG STARTS 100mm Illuminated Arcade Button | B01LZMANZ7 | User input (microswitch only; LED unused) | ~$8 |
| 4 | I-VOM / Milcraft Mini Speaker (3W, aux + BT) | B07KQ44VGQ | Audio output | ~$10 |
| 5 | Cable Matters 8K Micro HDMI to HDMI 2.1 Cable | B0DDKBYH1X | Pi 5 → Display video | ~$10 |
| 6 | Elegoo 120-piece Dupont Jumper Wires | B01EV70C78 | GPIO wiring | ~$7 |
| 7 | ~~CableCreation 3.5mm TRS Aux Cable (1.5 ft, male-to-male)~~ **REMOVED** | ~~B01K3WX4FW~~ | ~~Was: USB audio adapter → Speaker~~ | — |
| 7 | **Tan QY 3.5mm Male-to-Female Audio Extension Cable (1 ft)** | **B07XD6ZGNN** | **Audio extension: USB adapter → Speaker's built-in male plug** | ~$6 |
| 8 | Yintar Surge Protector Power Strip (6 AC + 3 USB) | B08MTBCXWX | Power distribution hub | ~$15 |
| 9 | AuviPal 90° USB-C Adapter (2-pack, USB4) | B0B8X6H96S | Right-angle power input for Pi 5 | ~$9 |
| 10 | Waveshare CSI FPC Cable 200mm (22-pin to 15-pin) | B0D49DYL1X | Pi 5 CSI → Camera Module 3 | ~$6 |
| 11 | Plugable USB Audio Adapter (USB-A to 3.5mm) | B00NMXY2MO | Audio output (Pi 5 has no 3.5mm jack) | ~$8 |
| 12 | CableCreation Short Micro USB Cable (6 inch) | B013G4EAEI | Continuous speaker charging | ~$5 |
| 13 | **iUniker ICE Peak Active Cooler for Raspberry Pi 5** | **B0FRZ6JHRT** | **Thermal management (fan + heatsink)** | ~$9 |

### Official Raspberry Pi accessories (3 items, purchased separately)

| # | Product | Source | Role |
|---|---------|--------|------|
| 14 | Raspberry Pi 5 (4 GB or 8 GB) | raspberrypi.com | Main compute board |
| 15 | Raspberry Pi Camera Module 3 (standard) | raspberrypi.com | Computer vision input |
| 16 | Raspberry Pi 27W USB-C Power Supply | raspberrypi.com | Power for Pi 5 |

---

## Per-component specs

### 1. Jay Franco Weighted Big Bird Plush (Enclosure)

| Spec | Detail |
|---|---|
| Dimensions | 22″ × 12″ × 7.5″ (L × W × H) |
| Weight | 2.5 lb (weighted beads, non-removable) |
| Material | 100% polyester microfiber outer, 100% polyester fill + weighted beads |
| Closure | Sealed — no zipper; must cut seam to insert electronics |
| Care | Spot clean only, not machine washable |
| Certification | OEKO-TEX Standard 100 |
| Build notes | Beads must be displaced/partially removed to create cavity for electronics. Polyester is non-conductive. Ensure ventilation path for Pi 5 heat dissipation. |

### 2. GeeekPi 7″ IPS Display

| Spec | Detail |
|---|---|
| Panel | 7″ IPS TFT LCD, 1024 × 600 @ 60 Hz, non-touch |
| Viewing angle | 178° |
| Video input | Full-size HDMI Type A |
| Power | USB-C, 5V, ~500 mA |
| Dimensions | ~165 × 100 × 5 mm |
| Weight | ~230 g |
| In box | LCD panel, USB-C power cable, full-size HDMI cable, micro-HDMI-to-HDMI adapter, 2× stands |
| Config needed | `/boot/firmware/config.txt`: `hdmi_group=2`, `hdmi_mode=87`, `hdmi_cvt 1024 600 60 3 0 0 0` |

### 3. EG STARTS 100mm Arcade Button

| Spec | Detail |
|---|---|
| Dome diameter | 100 mm |
| Mounting hole | 88 mm |
| Material | Transparent PVC dome + ABS housing |
| Microswitch | Momentary NO (Normally Open), 1M cycle life |
| Microswitch terminals | 4.8 mm spade (COM and NO) |
| LED | 12V DC — **NOT USED in this build** |
| LED terminals | 6.3 mm spade — **left unwired** |
| In box | Dome + housing, locking ring, 12V LED, microswitch |
| Wiring | Solder regular wire directly to microswitch tabs. No crimp connectors needed. |

### 4. I-VOM / Milcraft Mini Speaker

| Spec | Detail |
|---|---|
| Driver | 27 mm, 8Ω impedance, 3W max |
| SNR | >90 dB |
| Audio input | 3.5 mm aux (retractable cable in base) |
| Bluetooth | Yes (version unspecified; not used in this build) |
| Charging | Micro USB |
| Battery | Rechargeable Li-ion (capacity unspecified), 8+ hours |
| Volume control | None on device — must control from Pi software |
| Dimensions | ~50 × 50 × 50 mm (half a credit card footprint) |
| In box | Speaker, manual (Micro USB cable may not be included — using CableCreation cable instead) |
| Build notes | Aux input and Micro USB charging are separate ports; simultaneous playback + charging works. Speaker stays plugged in for continuous multi-day operation. |

### 5. Cable Matters Micro HDMI to HDMI Cable

| Spec | Detail |
|---|---|
| Connector A | Micro HDMI Type D male |
| Connector B | Standard HDMI Type A male |
| HDMI version | 2.1 (48 Gbps, backward compatible) |
| Max resolution | 8K@60Hz / 4K@240Hz |
| Features | Dynamic HDR, eARC, ALLM, VRR, HDCP 2.3 |
| Conductor | 100% bare copper, gold-plated connectors |
| Jacket | Braided |
| Length | ~3.3 ft (1 m) |
| In box | 1× cable |

### 6. Elegoo Dupont Jumper Wires

| Spec | Detail |
|---|---|
| Quantity | 120 total: 40× M-F, 40× M-M, 40× F-F |
| Wire length | 20 cm (8″) each |
| Pin pitch | 2.54 mm (standard GPIO header pitch) |
| Wire gauge | ~28 AWG |
| Conductor | Copper-clad aluminum, PVC insulation |
| Use in build | Female-to-female wires connect GPIO header pins to soldered leads from the arcade button microswitch |

### 7. Tan QY 3.5mm Male-to-Female Audio Extension Cable (REPLACES CableCreation male-to-male)

**IMPORTANT: The original CableCreation male-to-male aux cable (B01K3WX4FW) was REMOVED from the cart.** The Milcraft speaker has a built-in retractable 3.5mm male plug on its base. The Plugable USB audio adapter has a 3.5mm female output jack. A male-to-male cable cannot connect these — you need a male-to-female extension so the speaker's built-in male plug can insert into the female end.

| Spec | Detail |
|---|---|
| ASIN | B07XD6ZGNN |
| Connectors | 3.5 mm TRS **male** to 3.5 mm TRS **female** (3-pole, stereo) |
| Length | 1 ft (0.3 m) |
| Shielding | 4-layer (enamelled copper core, cotton thread, TPE jacket, nylon braid) |
| Bend life | 10,000+ cycles |
| In box | 1× cable |
| Audio chain | Plugable adapter (female jack) ← extension male end ... extension female end ← speaker's built-in male plug |

### 8. Yintar Surge Protector Power Strip

| Spec | Detail |
|---|---|
| AC outlets | 6 (1 widely-spaced at 1.8″ gap) |
| AC rating | 1250W / 10A, 100–240 VAC |
| USB-A ports | 2× at 5V / 2.4A each |
| USB-C port | 1× at 5V / 3A (basic, no PD — NOT used for Pi) |
| Surge protection | 1680 Joules, <1 ns response |
| Cord | 6 ft, 45° flat angled plug |
| Dimensions | 11.59″ × 1.89″ × 1.14″ |
| Housing | Metal |
| Safety | ETL Listed, 10A circuit breaker |
| Use in build | AC outlet #1 → Pi 27W PSU; USB-A #1 → speaker charging cable |

### 9. AuviPal 90° USB-C Adapter

| Spec | Detail |
|---|---|
| Connector | USB-C male → USB-C female, 90° right angle |
| USB standard | USB4 (Thunderbolt 3/4 compatible) |
| Data speed | 40 Gbps |
| Power delivery | 100W (20V/5A) |
| Video | 8K@60Hz passthrough |
| Dimensions | 0.75″ × 0.5″ × 0.32″ |
| Shell | Aluminum alloy |
| Durability | 10,000+ plug cycles |
| In box | 2× adapters (1 up-angle, 1 down-angle) |
| Compatibility | USB4 spec requires full 24-pin wiring including CC pins. As a passive adapter, it transparently passes all PD profiles including the Pi 5's 5.1V/5A negotiation. This is a non-issue — the adapter is a straight pin-to-pin passthrough with nothing inside to block any voltage profile. |

### 10. Waveshare CSI Cable (200mm)

| Spec | Detail |
|---|---|
| Pi 5 end | 22-pin, 0.5 mm pitch FPC |
| Camera end | 15-pin, 1.0 mm pitch FPC |
| Length | 200 mm |
| EMI shielding | Black EMI film on both sides |
| Type | CSI (camera) only — NOT interchangeable with DSI (display) |
| In box | 1× FPC cable |

### 11. Plugable USB Audio Adapter

| Spec | Detail |
|---|---|
| USB connector | USB Type-A male |
| USB version | USB 1.1 (12 Mbps — sufficient for audio) |
| Audio chip | SSS1629 |
| Sample rate | 48 kHz / 16-bit |
| Headphone jack | 3.5 mm TRS (green ring) |
| Microphone jack | 3.5 mm TRS (red ring) |
| Power | USB bus-powered, ≤500 mA |
| Dimensions | 10.6 × 28 × 28.8 mm |
| Weight | 4.25 g |
| Driver | None required — USB Audio Class, plug-and-play |
| In box | Adapter, manual |
| Pi 5 support | Explicitly supported. Auto-detected as "USB Audio Device" on Raspberry Pi OS. |

### 12. CableCreation 6-inch Micro USB Cable

| Spec | Detail |
|---|---|
| Connector A | USB Type-A male |
| Connector B | Micro USB-B male |
| Length | 6 inches (15 cm) |
| Wire gauge | 24 AWG (thicker than typical 28 AWG) |
| Charging current | Up to 2.4A |
| Shielding | Triple-shielded |
| Jacket | PVC + cotton braid |
| In box | 1× cable |
| Use | Plugs into power strip USB-A port → speaker Micro USB for continuous charging |

### 13. iUniker ICE Peak Active Cooler for Raspberry Pi 5

| Spec | Detail |
|---|---|
| ASIN | B0FRZ6JHRT |
| Fan type | 35 × 10 mm blower fan, PWM speed control (auto-adjusts based on CPU temp) |
| Heatsink | Aluminum, covers CPU area |
| Height added to Pi 5 | ~10–15 mm above the board |
| Stays within Pi footprint | Yes (85 × 56 mm) |
| Mounting | 2 screws directly into Pi 5 board (screws included) |
| Thermal interface | Pre-applied thermal grease — peel release paper and mount |
| Power connector | **Pi 5's dedicated 4-pin JST-SH fan header** (upper right of board, between GPIO header and USB 2 ports) |
| Power source | 5V from the Pi 5 board — no separate cable or power supply needed |
| Performance | Keeps CPU under 56°C under stress; 20–30°C cooler than passive cooling |
| In box | ICE Peak cooler with fan, thermal pads, 2× mounting screws |
| Build notes | The fan cable is pre-attached to the cooler — just plug it into the JST fan header. Cut a small vent hole in the puppet fabric so the fan can exhaust hot air. This is critical for multi-day operation inside an insulated polyester plush. |

### 14. Raspberry Pi 5

| Spec | Detail |
|---|---|
| SoC | BCM2712, quad-core Cortex-A76 @ 2.4 GHz |
| GPU | VideoCore VII @ 800 MHz |
| RAM | 1 / 2 / 4 / 8 / 16 GB LPDDR4X-4267 |
| PCB | 85 × 56 mm |
| Weight | ~46 g |
| HDMI | 2× micro HDMI Type D (dual 4Kp60, HDMI 2.0) |
| USB | 2× USB 3.0 + 2× USB 2.0 (all Type-A) |
| GPIO | 40-pin, 2.54 mm pitch, 3.3V logic |
| CSI/DSI | 2× 22-pin, 0.5 mm pitch FFC |
| Audio | NO 3.5 mm jack — HDMI or USB audio only |
| Power | USB-C, 5V/5A (27W) via USB PD recommended |
| Network | Gigabit Ethernet, 802.11ac Wi-Fi, Bluetooth 5.0/BLE |
| Fan header | 4-pin JST-SH, 1 mm pitch, PWM-capable |
| Operating temp | 0–70°C |
| In box | Board only |

### 15. Raspberry Pi Camera Module 3

| Spec | Detail |
|---|---|
| Sensor | Sony IMX708, 11.9 MP (4608 × 2592) |
| Pixel size | 1.4 µm |
| Autofocus | Phase Detection (PDAF) |
| Video modes | 1080p50, 720p100, 480p120 |
| FoV (standard) | 66° H × 41° V (75° diagonal), f/1.8 |
| Connector | 15-pin, 1.0 mm pitch FPC |
| Dimensions | 25 × 24 × 11.5 mm |
| Operating temp | 0–50°C |
| In box | Camera module, 200 mm ribbon (15-to-15 pin, for Pi 4) |

### 16. Raspberry Pi 27W USB-C Power Supply

| Spec | Detail |
|---|---|
| Primary PD profile | 5.1V / 5A (25.5W) — used by Pi 5 |
| Other PD profiles | 9V/3A, 12V/2.25A, 15V/1.8A (all max 27W) |
| Input | 100–240 VAC, 50/60 Hz |
| Cable | 1.2 m, 17 AWG, integrated (not detachable) |
| Connector | USB-C male |
| Efficiency | >91% |
| In box | PSU only |

---

## Compatibility matrix — ALL GREEN

Every interface in this build has been verified. No blocking issues remain.

| # | Interface | Status | Notes |
|---|-----------|--------|-------|
| 1 | Pi 5 micro HDMI → Display full HDMI | ✅ | Cable Matters micro-to-full HDMI cable (HDMI 2.1, backward compatible). Single cable, no adapter needed. |
| 2 | Pi 5 CSI (22-pin) → Camera (15-pin) | ✅ | Waveshare 22-to-15-pin FPC cable, 200 mm, EMI shielded. Purpose-built for this connection. |
| 3 | Pi 5 audio output (no 3.5mm jack) | ✅ | Plugable USB audio adapter adds 3.5 mm output via USB-A. Plug-and-play on Pi OS. |
| 4 | USB audio adapter → Speaker | ✅ | Tan QY 1 ft **male-to-female** 3.5 mm extension cable. The male end plugs into the Plugable adapter's female output jack. The speaker's built-in retractable male plug inserts into the cable's female end. This replaced the original male-to-male cable which was incompatible with the speaker's built-in male plug. |
| 5 | Speaker continuous charging | ✅ | CableCreation 6″ Micro USB cable from power strip USB-A port (5V/2.4A) to speaker Micro USB. Simultaneous aux playback + USB charging confirmed (separate ports). |
| 6 | Pi 5 power delivery | ✅ | Official 27W PSU (5.1V/5A PD) plugs into power strip AC outlet. AuviPal USB4 90° adapter transparently passes PD negotiation — it's a passive pin-to-pin adapter with full 24-pin wiring, so there is nothing inside it that could block any voltage profile. |
| 7 | Arcade button → GPIO | ✅ | Solder regular wire directly to microswitch COM and NO terminals. Connect other ends to a GPIO pin and GND using Dupont female connectors on the Pi header. No crimp connectors or spade adapters needed — soldering bypasses the terminal-size mismatch entirely. The microswitch is just two contacts; it works at any voltage including 3.3V GPIO with internal pull-up enabled. |
| 8 | Arcade button LED | ✅ (skipped) | LED requires 12V. User decided not to use the LED. Leave LED terminals unwired. No 12V supply needed. |
| 9 | Power strip USB-C for Pi 5 | ✅ (avoided) | Strip's USB-C outputs only 5V/3A (15W), insufficient for Pi 5. User correctly uses AC outlet + official 27W PSU instead. |
| 10 | Display resolution config | ✅ | Non-standard 1024×600 resolution requires `/boot/firmware/config.txt` edits. See Software Configuration section below. |
| 11 | Speaker volume | ✅ | No hardware volume on speaker. Controlled via ALSA/PipeWire from Pi. See Software Configuration section below. |
| 12 | Thermal management | ✅ | **RESOLVED** — iUniker ICE Peak Active Cooler mounts directly to Pi 5 with 2 screws, plugs into the Pi's 4-pin JST fan header, draws power from the board (no separate cable). PWM auto-adjusts fan speed. Keeps CPU under 56°C under stress. Cut a small vent hole in the puppet fabric for airflow. Camera Module 3 (50°C ceiling) benefits from the cooled enclosure air. |

---

## Wiring topology

```
                          ┌─────────────────────────────────────┐
                          │       YINTAR POWER STRIP             │
                          │                                      │
  Wall outlet ──────────► │  AC #1 ──► Pi 27W PSU               │
                          │               │                      │
                          │               ▼                      │
                          │         AuviPal 90° adapter          │
                          │               │                      │
                          │               ▼                      │
                          │         RASPBERRY PI 5               │
                          │         (+ iUniker cooler on fan hdr)│
                          │                                      │
                          │  USB-A #1 ──► Micro USB cable ──►    │
                          │               Speaker (charging)     │
                          └──────────────────────────────────────┘

                    ┌──────────────── RASPBERRY PI 5 ────────────────┐
                    │                                                 │
                    │  4-pin JST fan header ──► iUniker ICE Peak     │
                    │                           Active Cooler        │
                    │                           (PWM, auto speed)    │
                    │                                                 │
                    │  Micro HDMI ──► Cable Matters cable ──►        │
                    │                  GeeekPi 7" Display            │
                    │                  (powered via its own USB-C    │
                    │                   from strip USB-A or AC)      │
                    │                                                 │
                    │  CSI (22-pin) ──► Waveshare FPC cable ──►      │
                    │                   Camera Module 3 (15-pin)     │
                    │                                                 │
                    │  USB-A port ──► Plugable USB Audio Adapter     │
                    │                   │                             │
                    │                   ▼ (green 3.5mm female jack)  │
                    │                 Tan QY extension cable          │
                    │                 (male into adapter)             │
                    │                   │                             │
                    │                   ▼ (3.5mm female end)         │
                    │                 Speaker's built-in male plug ──┤
                    │                                                 │
                    │  GPIO pin ──────► wire (soldered) ──►          │
                    │                   Arcade button microswitch NO │
                    │  GND pin ───────► wire (soldered) ──►          │
                    │                   Arcade button microswitch COM│
                    └─────────────────────────────────────────────────┘
```

---

## GPIO wiring for arcade button

The arcade button microswitch has two relevant terminals: **COM** (Common) and **NO** (Normally Open). The 12V LED terminals (6.3mm spade) are left completely unwired.

### Physical wiring

1. **Solder** a length of regular hookup wire (20–22 AWG stranded) to the microswitch **NO** terminal
2. **Solder** a second wire to the microswitch **COM** terminal
3. Attach a **female Dupont connector** to the free end of each wire (or solder directly to the connector)
4. Push the NO wire's Dupont connector onto **GPIO 17** (physical pin 11)
5. Push the COM wire's Dupont connector onto **GND** (physical pin 9, 14, 20, 25, 30, 34, or 39)

### Software configuration

Enable the Pi 5's internal pull-up resistor in code. When not pressed, GPIO reads HIGH (3.3V). When pressed, the microswitch shorts NO to COM, pulling GPIO to GND (LOW).

```python
from gpiozero import Button
from signal import pause

button = Button(17)  # GPIO17, internal pull_up=True by default

button.when_pressed = lambda: print("Button pressed!")
button.when_released = lambda: print("Button released!")

pause()
```

Any GPIO pin works — GPIO 17 is just a suggestion. Avoid GPIO pins 0, 1 (I2C), 14, 15 (UART), and 2, 3 (I2C1) if those buses are in use.

---

## Software configuration

### Display setup (`/boot/firmware/config.txt`)

```ini
# GeeekPi 7" 1024x600 display
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=87
hdmi_cvt 1024 600 60 3 0 0 0
```

Alternatively, clone GeeekPi's config script:
```bash
git clone https://github.com/geeekpi/lcd-config.git
cd lcd-config && sudo bash lcd-config.sh
```

### Audio output (Plugable USB adapter)

The adapter is auto-detected on Raspberry Pi OS. Set it as default:

```bash
# List audio devices
pactl list short sinks

# Set USB audio as default (name may vary)
pactl set-default-sink alsa_output.usb-GeneralPlus_USB_Audio_Device-00.analog-stereo

# Adjust volume (0–100%)
pactl set-sink-volume @DEFAULT_SINK@ 70%
```

Or via ALSA:
```bash
# Set volume
amixer -D hw:1 set Speaker 70%

# Test audio
aplay -D plughw:1,0 /usr/share/sounds/alsa/Front_Center.wav
```

If using Pi OS Lite (headless), install PipeWire manually:
```bash
sudo apt install pipewire pipewire-pulse wireplumber libspa-0.2-bluetooth
```

### Camera (libcamera)

```bash
# Test camera
libcamera-hello -t 5000

# Capture still
libcamera-still -o test.jpg

# Stream video
libcamera-vid -t 0 --inline --listen -o tcp://0.0.0.0:8888
```

The Camera Module 3 requires the `libcamera` stack (not legacy `raspicam`). It is pre-installed on current Raspberry Pi OS.

### Thermal monitoring

```bash
# Current CPU temperature
vcgencmd measure_temp

# Throttling status (0x0 = no throttling)
vcgencmd get_throttled

# Continuous monitoring
watch -n 1 vcgencmd measure_temp
```

Pi 5 thermal-throttles at 85°C. Camera Module 3 is rated to 50°C. The iUniker ICE Peak Active Cooler keeps the CPU under 56°C under stress. Cut a small vent hole in the puppet fabric near the cooler's exhaust for airflow.

---

## Power budget

| Component | Power draw | Source |
|-----------|-----------|--------|
| Raspberry Pi 5 (typical load) | 5–12 W | 27W PSU via AC outlet |
| iUniker ICE Peak Active Cooler | ~0.5–1 W | Pi 5 fan header (5V) |
| GeeekPi 7″ display | ~2.5 W | USB-C (from Pi USB-A or strip) |
| Camera Module 3 | ~1.5 W | Pi CSI bus |
| Plugable USB audio adapter | <0.5 W | Pi USB-A bus |
| I-VOM speaker (while charging) | ~2.5 W | Strip USB-A via Micro USB cable |
| **Total system** | **~13–20 W** | Well within 27W PSU + strip capacity |

The 27W PSU has ample headroom. The power strip's 1250W/10A AC capacity is far beyond what this build requires.

---

## Physical dimensions summary (for cavity planning)

| Component | Dimensions | Must fit inside puppet? |
|-----------|-----------|------------------------|
| Pi 5 PCB | 85 × 56 × 18.4 mm | Yes |
| iUniker ICE Peak Cooler | ~85 × 56 × 10–15 mm (sits on top of Pi 5, within footprint) | Yes (mounted on Pi 5 board) |
| Camera Module 3 | 25 × 24 × 11.5 mm | Yes (positioned at puppet's face/eye area) |
| GeeekPi display | ~165 × 100 × 5 mm | Mounted externally (belly screen) |
| Speaker | ~50 × 50 × 50 mm | Yes (positioned near puppet's mouth area) |
| Arcade button | 100 mm dome, 88 mm mounting hole | Mounted externally (body panel or separate mount) |
| Plugable USB adapter | 10.6 × 28 × 28.8 mm | Yes (plugged into Pi USB-A port) |
| AuviPal adapter | 19 × 12.7 × 8.1 mm | Yes (attached to Pi USB-C port) |
| Waveshare CSI cable | 200 mm length, ~15 mm wide | Yes (ribbon cable, easily routed) |
| Power strip | 11.59″ × 1.89″ × 1.14″ | No — sits outside/behind the puppet |
| 27W PSU | ~52 × 52 × 36 mm body + 1.2 m cable | PSU body outside puppet; cable routes in |

The puppet's 22″ × 12″ × 7.5″ interior (with beads displaced) provides roughly 170 × 130 × 80 mm of usable cavity after accounting for plush wall thickness — sufficient for the Pi 5 + cooler stack (~30 mm tall combined), speaker, camera, adapter, and all internal cabling.

---

## Notes for Claude Code

1. **All connections are wired (no Bluetooth used).** Audio goes through USB adapter + male-to-female extension cable. Speaker charging is wired Micro USB. The speaker has Bluetooth but it was deliberately not used due to poor Bluetooth reviews on this specific speaker.

2. **The aux cable was swapped from male-to-male to male-to-female.** The speaker has a built-in retractable 3.5mm male plug on its base. The Plugable USB adapter has a 3.5mm female output jack. A male-to-male cable couldn't connect these. The Tan QY male-to-female extension (B07XD6ZGNN) bridges them: male end into the adapter's female jack, speaker's built-in male plug into the cable's female end.

3. **The arcade button LED is not used.** No 12V supply is needed anywhere in this build. The microswitch operates standalone at 3.3V GPIO logic.

4. **The power strip's USB-C port is not used.** It only delivers 5V/3A (15W) which is insufficient for the Pi 5. The Pi is powered from the official 27W PSU plugged into an AC outlet on the strip.

5. **The AuviPal USB-C adapter is safe.** It's a passive USB4-rated adapter with full 24-pin wiring. It transparently passes PD negotiation. There is nothing active inside it that could block any voltage profile.

6. **Soldering is used for the arcade button.** Regular hookup wire is soldered directly to the microswitch spade terminals, bypassing any need for crimp connectors or spade adapters. The other end of each wire uses a female Dupont connector to plug onto the Pi 5 GPIO header.

7. **The Dupont jumper wires** (Elegoo, Item 6) serve as the connection between the Pi 5's GPIO header pins and external components. Their female connectors slide onto the 2.54 mm GPIO pins. For the arcade button specifically, they bridge the soldered wires to the GPIO header.

8. **Display power** can come from one of the Pi 5's USB-A ports (USB-C cable from display to Pi USB-A via adapter) or from the power strip's USB-A port. Either works — the display draws ~500 mA at 5V.

9. **Speaker has no volume buttons.** All volume control must be handled in software via ALSA or PipeWire/PulseAudio commands.

10. **Camera uses libcamera**, not the legacy raspicam stack. The Camera Module 3 with IMX708 sensor requires the modern libcamera API.

11. **Thermal management is resolved.** The iUniker ICE Peak Active Cooler (B0FRZ6JHRT) mounts to the Pi 5 with 2 screws, plugs into the board's 4-pin JST fan header, and draws power directly from the Pi. No separate power cable or supply needed. The fan automatically adjusts speed via PWM based on CPU temperature. **Cut a small vent hole in the puppet fabric** near the cooler's exhaust side to allow hot air to escape — without this, heat will recirculate inside the insulated plush.
