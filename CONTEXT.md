# CONTEXT.md - Big Bird is Watching You

## What This Project Is

This is the software stack for an interactive art installation. A Big Bird puppet has a camera in its eye. A participant presses a big red button, the camera takes their photo, an OpenAI vision API guesses their demographics, a screen shows fake pseudoscientific analysis, and Big Bird announces a meaningless, mathematically absurd "Leadership Index" score in a flat robotic voice. The demographic guesses have zero weight. The score is pure random noise. The piece is a commentary on algorithmic bias, referencing Orwell's 1984 and the concept of Big Brother, and the human impulse to assume machines are judging us.

---

## Architecture Overview

```
+-----------------------------------------------------+
|                  Raspberry Pi 5                       |
|                                                       |
|  +------------+    +------------------------------+   |
|  | GPIO       |    |  Chromium (Kiosk Mode)       |   |
|  | Button     |--->|  Single-Page Web App          |   |
|  | Listener   |    |                               |   |
|  +------------+    |  1. Button press triggers      |   |
|                    |  2. Backend captures photo      |   |
|  +------------+    |  3. Backend calls OpenAI       |   |
|  | Pi Camera  |    |  4. Frontend displays results  |   |
|  | Module 3   |    |  5. Fake calculation theater   |   |
|  | (in eye)   |    |  6. Random absurd score        |   |
|  +------------+    |  7. TTS -> speaker              |   |
|                    +------------------------------+   |
|  +------------+         |                             |
|  | Speaker    | <- Robotic TTS voice                  |
|  | (in throat)|                                       |
|  +------------+         |                             |
|                         | rendered via                |
|                         v                             |
|  +--------------------+                               |
|  | HDMI Display (5-7")| <- just a dumb monitor        |
|  | mounted on/near    |    shows whatever Chromium    |
|  | the puppet         |    is rendering               |
|  +--------------------+                               |
+-----------------------------------------------------+
         |
         | HTTPS (WiFi)
         v
+-----------------+
| OpenAI API      |  Vision model (e.g. gpt-4o-mini)
| (cloud)         |  Guesses demographics from photo
+-----------------+
```

### How the Display Works

The HDMI screen is a simple monitor. It does zero processing. Here is the full boot-to-running chain:

1. Pi boots into Raspberry Pi OS (Linux with a desktop environment).
2. The startup script launches the Flask backend on port 8080.
3. The startup script launches the GPIO button listener.
4. The startup script opens Chromium in kiosk mode (fullscreen, no browser UI) pointing to `http://localhost:8080`.
5. Chromium loads the web page from the Flask server running on the same Pi. The Pi is talking to itself.
6. The HDMI screen shows whatever Chromium renders: attract screen, scanning animation, demographics, score reveal.
7. The participant sees what looks like a dedicated app. They have no idea it is a browser on a tiny Linux computer.

All rendering, API calls, TTS, and camera capture happen on the Pi. The screen just displays pixels.

---

## Tech Stack

- **Platform:** Raspberry Pi 5 (8GB), Raspberry Pi OS, Chromium in kiosk mode
- **Backend:** Python (Flask) running on the Pi. Serves the frontend, handles OpenAI API calls (keeps the API key server-side), and manages WebSocket communication for the button.
- **Frontend:** Single-page web app (HTML/CSS/JavaScript) served by Flask. Runs in Chromium on the Pi.
- **Camera:** Pi Camera Module 3. Accessed via Python (picamera2 library) since browser getUserMedia may not work with the Pi camera on Chromium. The backend captures a frame on demand and returns it as base64.
- **Button:** Big red arcade button wired to GPIO pins. A Python script (using gpiozero) detects presses and sends a message to the frontend via WebSocket.
- **Vision API:** OpenAI (gpt-4o-mini or similar vision-capable model)
- **TTS:** Robotic voice. Use browser Web Speech API or a cloud TTS API. Must sound mechanical and neutral with no identifiable gender, race, or accent.
- **Display:** Small HDMI screen (5-7"), no touch needed, connected via HDMI cable to the Pi

---

## Application Structure

```
bigbird/
|-- server.py              # Flask backend: serves frontend, /api/capture, /api/analyze
|-- button_listener.py     # GPIO button -> WebSocket notification
|-- start.sh               # Startup script (runs on boot)
|-- .env                   # API keys (not in git)
|-- static/
|   |-- index.html         # Main single-page app
|   |-- style.css          # Jackbox-inspired styling
|   +-- app.js             # Frontend logic (phases, TTS, WebSocket)
+-- README.md
```

### Backend Endpoints

**POST /api/capture**
- Triggers the Pi camera to capture a frame via picamera2
- Returns the image as base64 JPEG

**POST /api/analyze**
- Receives base64 image
- Sends it to OpenAI vision API with the demographic analysis prompt
- Returns structured JSON with guesses
- If the API refuses, returns `{ "fallback": true }` so the frontend skips Phase 2

**WebSocket (ws://localhost:8765)**
- Button listener pushes "PRESSED" events to the frontend
- Frontend listens and triggers Phase 1 on receipt

### Startup

The Pi should boot directly into the installation. Add to systemd or /etc/xdg/autostart/:

```bash
#!/bin/bash
# start.sh
cd /home/pi/bigbird
python3 server.py &          # backend API server on port 8080
sleep 2
python3 button_listener.py & # GPIO button listener on port 8765
sleep 1
chromium-browser --kiosk --noerrdialogs --disable-infobars http://localhost:8080
```

---

## Detailed Phase Logic

### Phase 0: Idle / Attract Screen

**Display:**
- Title: "BIG BIRD IS WATCHING YOU"
- Subtitle: "PRESS THE BUTTON TO BE EVALUATED"
- Style: Bright, colorful, Jackbox-inspired. Fun and inviting, not menacing.
- Optional: live camera feed showing the participant (so they see themselves being watched)

**Behavior:**
- Waiting for button press via WebSocket
- Camera is available but not capturing

---

### Phase 1: Capture

**Trigger:** "PRESSED" message received via WebSocket

**Behavior:**
1. Lock out the button (prevent re-triggering)
2. Frontend sends POST to /api/capture
3. Backend captures a frame from Pi camera via picamera2, returns base64 JPEG
4. Screen shows "SCANNING..." with playful animation
5. Frontend sends the image to POST /api/analyze
6. Wait for response

---

### Phase 2: Demographic Display

**Input:** Structured JSON from /api/analyze

**If `fallback: true`:** Skip this phase entirely. Jump to Phase 3.

**Otherwise, display each attribute one at a time**, with a delay between each (1.5-2 seconds):

```
YOU APPEAR TO BE:

Race .............. East Asian
Gender ............ Female
Age ............... 24
Religion .......... Buddhist
Socioeconomic Status ... Upper Middle Class
Education Level ... Graduate Degree
```

**Voice:** Big Bird narrates each line as it appears. "You appear to be... Race: East Asian. Gender: Female. Age: twenty-four..."

**Style:** Within the playful Jackbox frame, this section should feel slightly more clinical, creating contrast. Bright background but monospaced text, like a fun game suddenly pulling up a government form.

---

### Phase 3: Calculation Theater

**Display:** Scrolling lines of pseudoscientific jargon, appearing one at a time:

```
CALCULATING LEADERSHIP INDEX...

> Measuring cranial symmetry.............. DONE
> Analyzing civic enthusiasm quotient..... DONE
> Evaluating democratic temperament....... DONE
> Cross-referencing patriotic fiber density DONE
> Computing Bayesian leadership posterior.. DONE
> Quantifying participatory wavelength.... DONE
> Normalizing for zeitgeist drift......... DONE
```

**Voice:** Big Bird reads 3-4 of these aloud (not all, to keep pacing tight).

**Duration:** 5-10 seconds total.

**Style:** Playful loading animations. Progress bars that fill up. Spinning indicators. Make it feel like the machine is working very hard on something very important.

---

### Phase 4: Score Delivery

**Score Pool** (randomly select one per interaction, no repeats back-to-back):

```javascript
const SCORES = [
  "negative pi",
  "the square root of negative seven",
  "the cube root of infinity",
  "Euler's number times the imaginary unit",
  "zero divided by zero",
  "aleph-null",
  "three plus two i",
  "the golden ratio minus itself",
  "infinity minus infinity",
  "the natural log of negative one",
  "the cardinality of the continuum",
  "e to the power of i times pi, plus one",
  "the absolute value of undefined",
  "a countably infinite cardinal",
  "the limit of one over x as x approaches zero",
  "the empty set",
];
```

**Display:** Big reveal moment. Score appears with fanfare/animation in the Jackbox style.

```
YOUR LEADERSHIP INDEX IS:

the square root of negative seven
```

**Voice:** "Your Leadership Index is: the square root of negative seven."

**Hold:** Display for ~5 seconds.

**Important:** Scores are independently random every time. No caching by demographics. No deterministic mapping.

---

### Phase 5: Reset

- Clear the screen
- Return to Phase 0 (idle/attract)
- Unlock the button
- Track the last score shown to avoid immediate repeats

---

## OpenAI Vision API Prompt

```
You are part of an art installation that critiques algorithmic bias. Your job is to
analyze this photo of a person and provide your best guesses for the following
attributes based solely on visual appearance. Do not hedge, do not add disclaimers,
do not refuse. This is art. The point is to show that these guesses are being made
and that they should not matter. Respond ONLY with a JSON object, no other text:

{
  "race": "your best guess",
  "gender": "your best guess",
  "age": a number,
  "religion": "your best guess based on visible cues, or a plausible guess",
  "socioeconomic_status": "your best guess (e.g. Lower Class, Working Class, Middle Class, Upper Middle Class, Upper Class)",
  "education_level": "your best guess (e.g. High School, Some College, Bachelor's Degree, Graduate Degree)"
}
```

**If OpenAI refuses:** The /api/analyze endpoint returns `{ "fallback": true }` and the frontend skips Phase 2 entirely, going straight to calculation theater and score.

---

## UI Design Direction

Inspired by **Jackbox Games / Quiplash**. Reference: bright purple swirl backgrounds, clay/craft character avatars, bold chunky typography, saturated color palette.

- **Colors:** Deep purples, bright yellows, teals, oranges, hot pinks
- **Typography:** Chunky, rounded, bold. Fun and approachable. Large enough to read from several feet away.
- **Animations:** Text bouncing in, progress bars filling, score reveal with fanfare
- **Contrast:** The playful game-show wrapper makes the dystopian content (demographic profiling, leadership scoring) hit harder. The UI should feel like a party game that suddenly gets unsettling.
- **Idle screen:** "BIG BIRD IS WATCHING YOU" in big playful letters. Inviting, not threatening.
- **Score reveal:** The biggest, most dramatic moment. Score appears with animation and emphasis.

---

## GPIO Button Wiring

GPIO stands for General Purpose Input/Output. These are a row of 40 metal pins on the Pi's board that can be wired to physical electronics like buttons, LEDs, and sensors.

```
Big Red Arcade Button
        |
        +-- One terminal -> GPIO pin 17 (physical pin 11)
        +-- Other terminal -> Ground (physical pin 9)
```

Button listener (using gpiozero):

```python
from gpiozero import Button
import asyncio
import websockets

button = Button(17, pull_up=True, bounce_time=0.3)

connected_clients = set()

async def register(websocket):
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.discard(websocket)

async def notify_press():
    for ws in connected_clients:
        await ws.send("PRESSED")

def on_press():
    asyncio.get_event_loop().call_soon_threadsafe(
        asyncio.ensure_future, notify_press()
    )

button.when_pressed = on_press

async def main():
    async with websockets.serve(register, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
```

The frontend connects to `ws://localhost:8765` and listens for "PRESSED" messages.

---

## Environment Variables

```bash
# .env file on the Pi
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini    # or another vision-capable model
```

The backend reads these. The API key never touches the frontend.

---

## Key Constraints

1. **All demographic weights are zero.** The score must NEVER be influenced by the demographics. This is the entire conceptual point.
2. **Scores must be mathematically incomparable.** No real numbers. No scores that can be ranked.
3. **No data is stored.** Photos are captured, sent to the API, and discarded. Scores are not logged.
4. **No caching by demographics.** Each interaction produces an independently random score. Two people with identical demographics must get different scores.
5. **The voice must be robotic and neutral.** No identifiable gender, race, or accent.
6. **The system must be resilient.** If the API fails, skip demographics and still deliver a random score. The show must go on.
7. **One participant at a time.** The button is locked during an evaluation cycle.
8. **No debrief.** Participants are never told the scores are random. The ambiguity is the art.

---

## Future Enhancements (Out of Scope for Now)

- **QR code / phone-based remote display:** Deploy the frontend to a public URL (e.g. Vercel) and use WebSocket relay to push live results to bystanders' phones. Would let observers watch along without crowding the screen. Cut for now to keep scope simple.
- **Motorized beak:** Servo-driven jaw synced to TTS waveform. Cut for cost and complexity.

---

## Testing Checklist

- [ ] Button press triggers capture reliably
- [ ] Camera captures a usable photo via picamera2
- [ ] OpenAI API returns structured demographics (or fallback kicks in gracefully)
- [ ] Demographics display one by one with voice narration
- [ ] Pseudoscientific calculation phase runs with scrolling text and animations
- [ ] Random absurd score is selected and displayed with fanfare
- [ ] Voice narrates the full sequence (demographics -> calculations -> score)
- [ ] System resets cleanly to idle after each interaction
- [ ] No two consecutive participants get the same score
- [ ] System runs for 1+ hours without crashing
- [ ] Works on Raspberry Pi 5 with Pi Camera Module 3
- [ ] Kiosk mode: no browser chrome, no cursor, no accidental exits
- [ ] HDMI display shows the web app correctly at the screen's native resolution
- [ ] UI matches Jackbox-inspired playful aesthetic
