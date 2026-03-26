# Complete Raspberry Pi 5 Big Bird build: every part with links

**All 11 components can be sourced for roughly $120–$165 total** — well under the $333 budget. Every item below is currently in stock from a trusted seller, with Amazon Prime options prioritized. The guide includes a budget pick and best-value pick where meaningful differences exist, plus direct product URLs. Estimated total using recommended picks: **~$140**.

---

## 1. Big Bird plush — the trickiest find

No major retailer currently sells an official Sesame Street Big Bird plush at 24+ inches in this price range. The largest official ones top out at **22 inches**. A generic yellow bird plush hits the size requirement for less money.

**Budget pick (meets 24" requirement):** Jrystar 24" Yellow Duck Stuffed Animal — ~$20–30, Amazon Prime
- URL: https://www.amazon.com/Jrystar-Stuffed-Animals-Birthday-Christmas/dp/B0FB369SBS
- Soft, fluffy 24" yellow duck plush. Non-weighted, lightweight PP cotton fill — easy to open along a seam and stuff with electronics. Ships vacuum-compressed; fluffs to full size.

**Best value pick (closest real Big Bird):** Jay Franco Weighted Sesame Street Big Bird Plush Pillow Buddy, 22" — ~$30–35, Amazon Prime
- URL: https://www.amazon.com/Jay-Franco-Weighted-Sesame-Street/dp/B0DJC7WLXW
- Official Sesame Street licensed, 22 inches (2 inches short of the 24" goal), **2.5 lbs weighted**. Also available at Walmart for $29.98: https://www.walmart.com/ip/Sesame-Street-Fuzzy-Big-Bird-Plush-Pillow-Buddy-Kids-Super-Soft-Stuffed-Pillow/13327818538

**Recommendation:** The Jrystar 24" generic yellow duck is the pragmatic winner — it meets the size requirement, is lightweight (easier to mod), and costs less. If the Big Bird look matters more than exact size, the Jay Franco 22" pillow buddy is the best licensed option available.

---

## 2. The 7-inch HDMI display needs careful selection for Pi 5

The Pi 5 outputs via micro-HDMI, so the display must either include a micro-HDMI adapter or you need the separate cable from Item 5. IPS panels matter here since the display will likely be viewed at an angle.

**Budget pick:** HMTECH 7" IPS Non-Touch, 800×480 — ~$28–34, Amazon Prime
- URL: https://www.amazon.com/HMTECH-Raspberry-Pi-Monitor-Non-Touch/dp/B09MFNLRQQ
- IPS panel, **178° viewing angles**, USB-powered, includes bracket/stand. Lists Pi 5 compatibility. Resolution is 800×480 (functional but not crisp for text). Does not include micro-HDMI cable.

**Recommended pick:** GeeekPi 7" IPS Non-Touch, **1024×600** — ~$33–40, Amazon Prime ✅ verified in stock
- URL: https://www.amazon.com/GeeekPi-Raspberry-1024x600-Display-Portable/dp/B0CHRD7CQ3
- IPS panel, USB-powered, includes stand, **includes micro-HDMI adapter in box**. Explicitly lists Pi 5 in product title. The 1024×600 resolution makes a real difference for readability. This is the clear best value — only $5–6 more than the HMTECH for meaningfully better resolution and an included adapter.

---

## 3. Two 100mm red arcade buttons with GPIO-ready contacts

These are commodity arcade parts. The key requirements are **momentary** (not latching), **normally-open microswitch** with bare wire terminals (not USB encoder), and **mounting hardware included**.

**Recommended pick (buy 2):** EG STARTS 100mm Big Dome LED Arcade Button, Red — ~$9–11 each, Amazon Prime ✅ verified in stock
- URL: https://www.amazon.com/EG-STARTS-Buttons-Illuminated-Machine/dp/B01LZMANZ7
- **100mm (4") diameter** dome button. Includes 12V LED, bulb holder, fixing ring/mounting nut, and microswitch. Standard **4.8mm crimp terminals** on the microswitch for GPIO wiring. Thousands of reviews, the go-to arcade button on Amazon. Total for 2: **~$18–22**.

**Alternative (5V LED version):** Easyget 5V 100mm Red Dome LED Button — ~$7–10 each
- URL: https://www.amazon.com/Easyget-Shaped-Illuminated-Self-resetting-Projects/dp/B00XRC9URW
- Same form factor but with a **5V LED** instead of 12V — easier to power from a Pi's GPIO if you want the LED lit. Slightly cheaper.

**Premium alternative:** Adafruit Massive Arcade Button 100mm Red (#1185) — $9.95
- URL: https://www.adafruit.com/product/1185
- Gold-standard quality, well-documented for Pi projects. Check stock — was recently out of stock at Adafruit.

---

## 4. A tiny speaker that fits inside a stuffed animal

The speaker needs to be compact, USB-powered or rechargeable, and connect via 3.5mm aux. Speech clarity matters more than bass.

**Budget pick:** SparkFun Hamburger Mini Speaker — $7.95
- URL: https://www.sparkfun.com/hamburger-mini-speaker.html
- Also on Amazon: https://www.amazon.com/SparkFun-Hamburger-Mini-Speaker/dp/B072BNLC1M
- **~2" diameter**, 3W output, 3.5mm aux input, **built-in rechargeable battery** (charges via mini-USB). Extremely compact — perfect for stuffing inside a plush. Two volume levels. No drivers needed. The battery means one fewer wire to route inside the plush.

**Best value pick:** Adafruit USB Powered Speakers — $9.95 ✅ verified in stock (21 units)
- URL: https://www.adafruit.com/product/1363
- USB-powered (200–400mA), **3.5mm stereo input**, built-in volume control wheel. Adafruit specifically tested these for Raspberry Pi frequency response. It's a pair of speakers — use one inside the plush. Louder and more consistent than battery-powered options since it draws continuous USB power.

**Recommendation:** The SparkFun Hamburger is ideal for the stuffed-animal use case — its tiny size and built-in battery minimize wiring complexity. The Adafruit speakers are better if you want maximum volume and don't mind USB power routing.

---

## 5. Micro-HDMI to HDMI cable

A straightforward cable. The Pi 5 uses micro-HDMI (Type D) output.

**Budget pick:** Anbear Micro HDMI to HDMI Cable, 3ft — ~$5–7, Amazon Prime
- URL: https://www.amazon.com/Micro-Cable-Anbear-Support-Compatible/dp/B088RB2QG9
- 4K@60Hz, HDMI 2.0, gold-plated connectors. Gets the job done.

**Best value pick:** UGREEN Micro HDMI to HDMI Cable, 3ft — ~$8–10, Amazon Prime
- URL: https://www.amazon.com/UGREEN-Adapter-Ethernet-Compatible-Raspberry/dp/B06WWQ7KLV
- **Explicitly lists Raspberry Pi 5** in product description. Triple-shielded, UGREEN brand quality. Worth the extra $3 for reliability.

**Note:** If you buy the GeeekPi display (Item 2), it includes a micro-HDMI adapter, so this cable becomes optional. But a dedicated cable is more reliable than an adapter for a permanent installation.

---

## 6. Female-to-female jumper wires for GPIO

**Recommended pick:** ELEGOO 120-piece Dupont Wire Kit — ~$6–7, Amazon Prime ✅ verified in stock
- URL: https://www.amazon.com/Elegoo-EL-CP-004-Multicolored-Breadboard-arduino/dp/B01EV70C78
- Includes **40 female-to-female** + 40 male-to-female + 40 male-to-male wires. All **20cm (8") length**, 2.54mm pitch, 10 rainbow colors. Amazon's #19 bestseller in internal components with **12,500+ reviews** at 4.7 stars. The extra M/F and M/M wires are a bonus for prototyping.

**Alternative (longer wires):** Adafruit Premium F/F Jumper Wires, 40×12" — $3.95 + shipping
- URL: https://www.adafruit.com/product/793
- **12-inch (300mm) length** gives more routing flexibility inside an enclosure. Higher-quality connectors than generic Dupont wires.

---

## 7. Short 3.5mm audio cable

**Budget pick:** YCS Basics 1-Foot 3.5mm Stereo Cable — ~$3–4, Amazon Prime
- URL: https://www.amazon.com/YCS-Basics-Stereo-Headphone-Smartphone/dp/B00A6VYPFE
- Basic, functional, 1-foot length. No frills needed for an internal connection.

**Best value pick:** CableCreation 3.5mm Aux Cable, 1.5ft — ~$4–6, Amazon Prime
- URL: https://www.amazon.com/CableCreation-Auxiliary-Compatible-Headphones-iPhones/dp/B01K3WX4FW
- Cotton-braided exterior, aluminum alloy shell, gold-plated slim connectors, double shielding. The 1.5ft length is ideal for routing inside a stuffed animal.

---

## 8. Pi 5 camera ribbon cable — the 22-pin connector is critical

The Pi 5 uses a **22-pin 0.5mm pitch** FPC connector, completely different from the 15-pin 1.0mm pitch on older Pi models. Using the wrong cable will not physically fit. The cable adapts from the Pi 5's 22-pin side to the Camera Module 3's standard 15-pin connector.

**Recommended pick:** Adafruit Raspberry Pi 5 FPC Camera Cable, 300mm (#5819) — **$3.16** ✅ verified in stock (71 units)
- URL: https://www.adafruit.com/product/5819
- Official Raspberry Pi cable. **22-pin 0.5mm to 15-pin 1.0mm**, 300mm long. At $3.16, this is an extraordinary value. Also available in 200mm ($2.70, product #5818) and 500mm ($2.50, product #5820).

**Amazon alternative:** Waveshare CSI FPC Cable for Pi 5, 300mm — ~$5–7, Amazon Prime
- URL: https://www.amazon.com/waveshare-CSI-Cable-Pi5-Camera/dp/B0CX1SFD44
- Same 22-pin to 15-pin specs with EMI shielding on both sides. Good option if consolidating your order on Amazon.

**SparkFun alternative:** Raspberry Pi 5 Camera Cable, 300mm — ~$1.50
- URL: https://www.sparkfun.com/raspberry-pi-5-camera-cable-300mm.html

---

## 9. USB-C right-angle adapter for clean cable routing

The Pi 5 draws up to **27W via USB-C**, so the adapter must support sufficient power delivery. Cheap data-only adapters won't work.

**Recommended pick:** AuviPal 90° USB-C Adapter, 2-pack — ~$8–10, Amazon Prime
- URL: https://www.amazon.com/AuviPal-Degree-Adapter-Extender-Notebook/dp/B0B8X6H96S
- USB4, **100W Power Delivery** (far exceeds Pi 5's 27W), 40Gbps data, aluminum shell. Includes both up-angle and down-angle variants. The 2-pack gives you a spare.

**Budget pick:** URWOOW USB-C Right Angle Adapter, 2-pack — ~$6–8, Amazon Prime
- URL: https://www.amazon.com/URWOOW-L-Shape-Degree-Adapter-Extension/dp/B07JGYBCT1
- 100W PD, plastic housing. Functional and cheaper.

---

## 10. Wooden box for mounting the arcade buttons

The mounting surface needs to be large enough for a **100mm (4-inch) hole** with clearance. A 6×4" box is too tight — the button diameter alone is 4 inches.

**Recommended pick:** Woiworco Unfinished Wooden Box with Hinged Lid, 12"×9.2"×3.3" — ~$10–13, Amazon Prime
- URL: Search Amazon for "Woiworco unfinished wooden box 12 inch" — brand page: https://www.amazon.com/stores/Woiworco/page/FCE447E1-D52B-4B71-BF59-71E094730E17
- Natural pine wood, hinged lid with clasp. The **12"×9.2" lid** provides ample surface for one or two 100mm button holes with plenty of clearance. The 3.3" depth houses the button mechanism and wiring underneath.

**Budget pick:** Creative Hobbies Unfinished Wood Craft Box, 6"×4"×2" — ~$7–9, Amazon Prime
- URL: https://www.amazon.com/Creative-Hobbies-Unfinished-Wood-Craft/dp/B08TKD4Y83
- ⚠️ **Warning:** A 4" hole on a 4"-wide surface leaves zero margin. Only viable if using a smaller 60mm button or if you mount the button on the longer 6" dimension at an angle.

---

## 11. Power strip

**Recommended pick:** Amazon Basics 6-Outlet Surge Protector, 6ft Cord, Black — ~$10, Amazon Prime ✅ verified in stock
- URL: https://www.amazon.com/Amazon-Basics-Protector-Extension-Protection/dp/B00TP1C51M
- (White version: https://www.amazon.com/Amazon-Basics-Protector-Extension-Protection/dp/B00TP1C1UC)
- 6 outlets (1 transformer-spaced), **790-joule surge protection**, 15A circuit breaker, LED indicator, wall-mountable. 23,000+ ratings at 4.7 stars. The standard-bearer for basic power strips.

---

## Budget summary and total cost estimate

| # | Item | Recommended product | Est. price | Seller |
|---|------|-------------------|-----------|--------|
| 1 | Big Bird plush (24") | Jrystar Yellow Duck 24" | ~$25 | Amazon |
| 2 | 7" HDMI display | GeeekPi 1024×600 IPS | ~$36 | Amazon |
| 3 | Arcade buttons ×2 | EG STARTS 100mm Red LED | ~$20 | Amazon |
| 4 | Small speaker | SparkFun Hamburger Mini | $7.95 | SparkFun |
| 5 | Micro-HDMI cable | UGREEN 3ft | ~$9 | Amazon |
| 6 | Jumper wires | ELEGOO 120-piece kit | ~$7 | Amazon |
| 7 | 3.5mm audio cable | CableCreation 1.5ft | ~$5 | Amazon |
| 8 | Pi 5 camera cable | Adafruit 22-pin 300mm | $3.16 | Adafruit |
| 9 | USB-C right-angle | AuviPal 2-pack | ~$9 | Amazon |
| 10 | Wooden box | Woiworco 12"×9.2" | ~$12 | Amazon |
| 11 | Power strip | Amazon Basics 6-outlet | ~$10 | Amazon |
| | **Estimated total** | | **~$144** | |

The all-budget-picks total drops to roughly **$120** by choosing the Anbear HDMI cable ($6), YCS audio cable ($3), SparkFun camera cable ($1.50), and the generic duck plush ($20). Either way, you're well under the $333 ceiling with **~$190+ remaining** for the Raspberry Pi 5, Camera Module 3, SD card, power supply, and any other components.

## Compatibility checklist before you buy

Three items require Pi 5-specific verification at checkout. The **GeeekPi display** explicitly lists Pi 5 and includes a micro-HDMI adapter. The **camera cable** must say "22-pin" or "Pi 5" — the Adafruit #5819 is confirmed correct. The **USB-C right-angle adapter** must support power delivery, not just data — both the AuviPal and URWOOW support 100W PD, which comfortably exceeds the Pi 5's 27W draw. Double-check each product listing at purchase time, as Amazon sellers occasionally swap variants under the same ASIN.