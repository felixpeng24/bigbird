# Big Bird Pi 5 art installation: complete parts list

Every component below has been verified for compatibility and availability. The total build cost runs **roughly $135–175** depending on options chosen. Nearly everything ships Amazon Prime; the one exception (camera cable from Adafruit) is the cheapest and most reliable option for that critical part.

---

## 1. Big Bird plush — the body of the puppet

**★ Top Pick: Jay Franco Sesame Street Big Bird Fuzzy Pillow Buddy (Non-Weighted)**
- **Price:** $29.00
- **Seller:** Target
- **URL:** https://www.target.com/p/jay-franco-sesame-street-big-bird-fuzzy-pillow-buddy/-/A-93968164
- **Size:** 22 inches tall

This pillow-style plush is the best option currently on the market. It's **100% polyester microfiber** with uniform soft fill — no weighted beads — making it trivially easy to cut open along a seam and create a cavity for electronics. The flat, wide pillow body is almost purpose-built for hiding hardware inside. At 22 inches it falls just 2 inches short of the stated 24" minimum, but **no mass-market Big Bird plush currently exists at 24"+ in the $20–60 range**. The legs and body crest can be extended with yellow craft fabric if strict height matters. Also available on Amazon (search ASIN for Jay Franco Big Bird Pillow Buddy, ~$25–32, Prime eligible).

⚠️ **Avoid** the weighted version (B0DJC7WLXW, ~$37) — it has 2.5 lbs of beads inside that you'd need to fully remove before inserting electronics.

---

## 2. The display: a 7-inch IPS screen with everything included

**★ Best Value: GeeekPi 7-Inch 1024×600 IPS Non-Touch Display**
- **Price:** ~$33–38
- **Seller:** Amazon (Prime eligible)
- **URL:** https://www.amazon.com/GeeekPi-Raspberry-1024x600-Display-Portable/dp/B0CHRD7CQ3
- **Resolution:** 1024×600 IPS, 178° viewing angles, 60Hz

This is the strongest pick because it checks every box. **Explicitly Pi 5 compatible**, USB-C powered (no wall adapter needed), IPS panel for wide viewing angles, and — critically — the package includes a micro-HDMI to HDMI adapter, an HDMI cable, a USB power cable, and two stands. That bundled adapter could save you the separate cable purchase below. Plug-and-play, no drivers required.

**Budget Alternative: HMTECH 7-Inch 800×480 IPS Non-Touch**
- **Price:** ~$26–32
- **Seller:** Amazon (Prime eligible)
- **URL:** https://www.amazon.com/HMTECH-Raspberry-Pi-Monitor-Non-Touch/dp/B09MFNLRQQ

Lower resolution but still IPS, still Pi 5 compatible. Does **not** include a micro-HDMI adapter — you'll need the cable from Item 5. Solid 4.2-star rating across 500+ reviews.

---

## 3. Two 100mm red arcade buttons with LEDs

**★ Top Pick: EG STARTS 100mm Big Dome Convex LED Push Button — Red**
- **Price:** ~$7–10 each (buy 2)
- **Seller:** Amazon (Prime eligible)
- **URL:** https://www.amazon.com/EG-STARTS-Buttons-Illuminated-Machine/dp/B01LZMANZ7

This is the go-to 100mm arcade button on Amazon. **Momentary/auto-reset** (not latching), **normally-open microswitch** with wireable 4.8mm crimp terminals, built-in **12V LED backlight**, red dome, and includes all mounting hardware (nut, gasket, bracket). Requires an **88mm mounting hole** — easily cut or drilled into the wooden craft box. EG STARTS is the dominant arcade parts brand on Amazon with strong reviews.

**Alternative for easier LED wiring: Easyget 5V 100mm LED Dome Button — Red**
- **Price:** ~$8–12 each
- **URL:** https://www.amazon.com/Easyget-Shaped-Illuminated-Self-resetting-Projects/dp/B00XRC9URW

Same form factor but the LED runs at **5V instead of 12V**, which means you can power it directly from the Pi's GPIO 5V pin without needing a separate power supply. Worth the slight premium if you want illuminated buttons without extra wiring complexity.

---

## 4. A tiny speaker that hides inside the puppet

**★ Top Pick: Milcraft Mini Speaker with 3.5mm Aux Input**
- **Price:** ~$10–13
- **Seller:** Amazon (likely Prime eligible)
- **URL:** https://www.amazon.com/I-VOM-Wireless-Portable-Cellphone-Rechargeable/dp/B07KQ44VGQ
- **Dimensions:** 1.8 × 1.8 × 1.3 inches

At under 2 inches on each side, this fits easily inside a stuffed animal. It has a **3.5mm aux input** for direct connection to the Pi's headphone jack — no Bluetooth pairing or drivers needed. USB rechargeable with a **10+ hour battery**, so it runs all day without being tethered. The 3W driver is clearly audible from 3–5 feet.

---

## 5. Micro-HDMI to HDMI cable

**★ Top Pick: Cable Matters Micro HDMI to HDMI Cable — 3 ft**
- **Price:** ~$7–9
- **Seller:** Amazon (Prime eligible)
- **URL:** https://www.amazon.com/Cable-Matters-High-Speed-Micro/dp/B0DMG4XMLG

Type D micro-HDMI to Type A standard HDMI, **HDMI 2.0 rated at 4K@60Hz**, 3-foot length. Cable Matters is a reliable US brand. **Note:** If you buy the GeeekPi display (Item 2), it already includes a micro-HDMI adapter, so you may not need this separately — but having a dedicated short cable is cleaner than using an adapter on a full-size HDMI cable.

**2-Pack Option:** https://www.amazon.com/Cable-Matters-2-Pack-Speed-Resolution/dp/B00DRMV10Q (~$9–11, useful as a spare)

---

## 6. Jumper wires for connecting buttons to GPIO

**★ Top Pick: ELEGOO 120-Piece Multicolored Dupont Wire Kit**
- **Price:** ~$6–7
- **Seller:** Amazon (Prime eligible)
- **URL:** https://www.amazon.com/Elegoo-EL-CP-004-Multicolored-Breadboard-arduino/dp/B01EV70C78
- **Contents:** 40 female-to-female + 40 male-to-male + 40 male-to-female, all 20cm

This is the best-selling jumper wire kit on Amazon with 14,000+ ratings. You get **40 female-to-female wires at 20cm** — exactly what's needed to connect arcade button microswitches to Pi GPIO pins. The extra male-to-male and male-to-female wires are a free bonus for prototyping. Standard **2.54mm Dupont connectors** fit the Pi's GPIO header perfectly. Color-coded and individually separable.

---

## 7. Short 3.5mm audio cable

**★ Top Pick: CableCreation 3.5mm Aux Cable — 1.5 ft**
- **Price:** ~$5–7
- **Seller:** Amazon (Prime eligible)
- **URL:** https://www.amazon.com/CableCreation-Auxiliary-Compatible-Headphones-iPhones/dp/B01K3WX4FW

Male-to-male 3.5mm TRS, braided nylon jacket, double-shielded, 24K gold-plated connectors. The 1.5-foot length is ideal for connecting the Pi's headphone jack to the speaker inside the puppet — long enough to reach but short enough to avoid tangles.

**Shorter Alternative: FosPower 1 ft Aux Cable** — https://www.amazon.com/FosPower-Stereo-Auxiliary-iPhone-Samsung/dp/B0100NK0VU (~$5–7)

---

## 8. Pi 5 camera ribbon cable — the compatibility-critical part

**★ Top Pick: Official Raspberry Pi 5 FPC Camera Cable — 300mm (Adafruit #5819)**
- **Price:** $3.16
- **Seller:** Adafruit
- **URL:** https://www.adafruit.com/product/5819
- **In Stock:** Yes (71 units as of research)

This is the **official Raspberry Pi Foundation camera cable** designed specifically for the Pi 5. It's a **22-pin 0.5mm pitch connector** on the Pi 5 end and a **15-pin 1.0mm pitch connector** on the camera module end. This is exactly the adapter needed because all current Pi cameras (Camera Module 3, V2, HQ Camera) still use the old 15-pin connector while the Pi 5 board uses the newer, smaller 22-pin port. At $3.16, it's the cheapest item on this list.

**Longer option (recommended for more routing flexibility inside the puppet):**
- **500mm version:** https://www.adafruit.com/product/5820 — **$2.50** (yes, the longer cable is actually cheaper)

**Amazon alternative: Waveshare CSI FPC Cable for Pi 5 — 300mm**
- **URL:** https://www.amazon.com/waveshare-CSI-Cable-Pi5-Camera/dp/B0CX1SFD44 (~$6–8, Prime eligible)
- Same 22-pin to 15-pin spec. Worth it if you want everything in one Amazon order.

---

## 9. USB-C right-angle adapter for clean cable routing

**★ Top Pick: 90° USB-C Male to Female Adapter (3-Pack)**
- **Price:** ~$5–7
- **Seller:** Amazon (Prime eligible)
- **URL:** https://www.amazon.com/Adapter-Degree-Type-C-Support-Transfer/dp/B08TZY4MSR

A simple L-shaped adapter that redirects the Pi 5's USB-C power cable at 90 degrees. Supports **100W PD charging** (far more than the Pi 5 needs), so there's zero risk of power delivery issues. The 3-pack means you have spares. Low-profile design keeps things tidy inside the puppet.

---

## 10. A wooden box for mounting the arcade button

**★ Top Pick: VIKOS Unfinished Pine Wood Box with Hinged Lid — 6.7" × 5.1" × 3.1"**
- **Price:** ~$9–10
- **Seller:** Amazon (Prime eligible)
- **URL:** https://www.amazon.com/VIKOS-Products-Unfinished-Unpainted-Storage/dp/B09HGQBNHZ

The **6.7" × 5.1" top surface** comfortably fits a 100mm arcade button (which needs an 88mm mounting hole) with clearance on all sides. Solid pine is easy to drill with a standard hole saw. The **hinged lid** is a major bonus: drill the button hole through the lid and use the box interior to house wiring and connections neatly. The 3.1" depth provides room for the button hardware underneath.

**Larger Alternative: KYLER Unfinished Pine Box — 8" × 6" × 3"**
- **URL:** https://www.amazon.com/KYLER-Unfinished-Pine-Wood-Box/dp/B09KNBWSLT (~$10–13)
- More room if you want to mount two buttons on one surface.

**Plastic Alternative: ABS Project Enclosure — 8.82" × 5.47" × 3.62"**
- **URL:** https://www.amazon.com/Plastic-Enclosure-EX-ELECTRONIX-EXPRESS/dp/B094NWJ7W5 (~$10–13)
- Better for a more industrial look; ABS is equally easy to drill.

---

## 11. Power strip to run the whole installation

**★ Top Pick: Amazon Basics 6-Outlet Surge Protector — 6 ft Cord**
- **Price:** ~$10–12
- **Seller:** Amazon (Prime, sold by Amazon)
- **URL:** https://www.amazon.com/Amazon-Basics-Protector-Extension-Protection/dp/B00TP1C51M

Six outlets, 6-foot cord, **790-joule surge protection**, 15-amp circuit breaker, LED indicator. This is the best-selling basic power strip on Amazon for a reason — it's cheap, reliable, and has thousands of positive reviews. Handles more outlets and cord length than this project needs, giving you flexibility for the display, Pi power supply, and any other peripherals.

**Upgrade with USB: Yintar 6-Outlet + 3 USB Ports**
- **URL:** https://www.amazon.com/Yintar-Protector-Outlets-Extension-Essentials/dp/B08MTBCXWX (~$10–13)
- Adds 2 USB-A and 1 USB-C charging port. Handy if you want to power the Pi or charge the speaker directly from the strip.

---

## Estimated total cost and ordering strategy

| # | Item | Top Pick Price | Seller |
|---|------|---------------|--------|
| 1 | Big Bird Plush (22") | $29.00 | Target |
| 2 | 7" IPS Display | ~$35.00 | Amazon |
| 3 | Arcade Buttons ×2 | ~$16.00 | Amazon |
| 4 | Mini Speaker | ~$12.00 | Amazon |
| 5 | Micro-HDMI Cable | ~$8.00 | Amazon |
| 6 | Jumper Wires (120pc) | ~$6.50 | Amazon |
| 7 | 3.5mm Audio Cable | ~$6.00 | Amazon |
| 8 | Pi 5 Camera Cable (500mm) | $2.50 | Adafruit |
| 9 | USB-C Right-Angle (3pk) | ~$6.00 | Amazon |
| 10 | Wooden Mounting Box | ~$9.50 | Amazon |
| 11 | Power Strip | ~$11.00 | Amazon |
| | **Estimated Total** | **~$141.50** | |

All Amazon items should be Prime eligible. The single Adafruit item ($2.50 camera cable) ships from New York; consider adding the 300mm cable ($3.16) as a spare to make Adafruit's shipping worthwhile, or substitute the Waveshare Amazon option (~$7) to keep everything in one order.

**One money-saving note:** The GeeekPi display already includes a micro-HDMI adapter and HDMI cable. If that adapter works well for your setup, you can skip the separate micro-HDMI cable (Item 5) and save ~$8. A dedicated cable is cleaner, but the bundled adapter is functional.