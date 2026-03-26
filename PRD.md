# Product Requirements Document: Big Bird is Watching You

## Overview

**Big Bird is Watching You** is an interactive art installation where a Big Bird puppet evaluates participants' "Leadership Index" using fake pseudoscientific analysis and delivers a mathematically absurd, incomparable score. The piece critiques algorithmic bias and the human impulse to be measured by systems that appear authoritative but are fundamentally arbitrary.

The name references George Orwell's *1984* and the concept of Big Brother, evoking surveillance, government evaluation, and authoritarian judgment, while subverting expectations with a children's character who has no race, gender, ethnicity, or age. Big Bird is a blank screen onto which participants project their own assumptions about bias.

---

## Problem Statement

In the current sociopolitical climate, democracy must grapple with deepening partisan divides and a lack of communication. As individuals retreat into echo chambers, only consuming media they feel comfortable with or avoiding discussion with those who disagree, mutual understanding erodes. Traditional political methods of discussion often exacerbate this problem. Novel interventions are needed that disrupt these patterns and allow people to engage with values like chance, choice, and civic life.

Conceptual art offers a vehicle for this disruption. By creating what Taryn Simon calls a "seductive frame," audiences can approach difficult subjects they might otherwise avoid. But passive observation is not enough to challenge biases. This demands interactive, game-like artistic inventions that engineer connection, works that catalyze viewers to navigate the foundation of their beliefs.

---

## Course Context

This project is created for **"The Game of Democracy: Art, Engineering, Chance, Choice, and Civic Life"**, a course that uses Taryn Simon's *Kleroterion* (2024) as an organizing metaphor. The Kleroterion was an ancient Athenian sortition device that randomly selected citizens for public offices and juries. The course explores how randomness, fairness, engineering, and aesthetics have shaped, and could reshape, democratic life. The final project requires designing and engineering physical art pieces ("devices of democracy") that merge engineering with social engagement.

**Budget:** $333
**Timeline:** As soon as possible

---

## Conceptual Foundation

### The Kleroterion Connection

The ancient Athenians used the Kleroterion because they believed randomness was fairer than letting biased humans decide. Big Bird extends this logic: if every system that claims to evaluate human potential is contaminated by bias, then perhaps the most honest output is one that means nothing at all.

### How the Trick Works

Behind the curtain, the system uses a vision API to parse the participant's photograph and generate guesses about their race, gender, age, and other attributes. These attributes are displayed on screen as part of the theatrical performance. They are then fed into a formula where **every single weight is zero**. The output is a random value pulled from a set of mathematically absurd expressions: irrational numbers, imaginary numbers, undefined expressions. The pseudoscientific analysis is theater. The attributes are irrelevant. The score is noise.

But participants don't know this. They experience a machine that looks at them, appears to think very hard, and delivers a judgment. In that gap between appearance and reality, people reveal their own assumptions, wondering whether their race affected the score, whether someone who "looked different" would score better. They project the biases they carry onto a system that carries none.

### Why the Scores Are Incomparable

The scores are not just random. They are **incomparable by design**. You cannot rank pi against infinity. You cannot decide whether the square root of negative one is better or worse than Euler's number. The piece doesn't just refuse to rank people; it makes ranking structurally impossible. It gestures toward a vision of civic life where evaluation itself is the problem.

### Why Big Bird

Big Bird has no race, gender, ethnicity, age, or religion. It is an abstraction of the observer, a blank screen onto which the audience projects meaning. A human figure would immediately raise the questions the piece is trying to expose. Big Bird sidesteps all of that. It is disarmingly fun. Those massive eyes and that cheerful yellow frame lower defenses before participants realize what's happening. And then it judges them, in a monotone, with total bureaucratic indifference. The contrast between the character's warmth and the system's coldness is where the piece finds its edge.

---

## Product Requirements

### 1. Interaction Flow

The full experience follows this sequence:

#### Phase 0: Idle State
- The screen displays "BIG BIRD IS WATCHING YOU" with a waiting/attract screen inviting participants to approach.
- Text and visuals indicate the participant should press the big red button to begin.
- Big Bird stares ahead, camera live but not capturing.
- Style: bright, playful, Jackbox-style (see UI Design section).

#### Phase 1: Capture (triggered by big red button press)
- Participant presses the physical arcade button mounted on a podium or base in front of Big Bird.
- The system captures a single frame from the camera (mounted in Big Bird's eye).
- Screen transitions to show "SCANNING..." state.

#### Phase 2: Demographic Analysis Display
- The vision API (OpenAI) returns its guesses for the following attributes:
  - **Race**
  - **Gender**
  - **Age**
  - **Religion**
  - **Socioeconomic Status**
  - **Perceived Education Level**
- These are displayed on screen one by one (e.g., "You appear to be: White, Male, Age 20, Agnostic, Middle Class, Bachelor's Degree").
- Big Bird narrates each attribute aloud in a flat robotic voice via the speaker.
- **Critical:** All of these attributes have a weight of **zero** in the scoring formula.
- **Fallback:** If the vision API refuses to guess demographics, skip this phase entirely and go directly to Phase 3. The piece still works without displaying the guesses.

#### Phase 3: Pseudoscientific Calculation Theater
- The screen displays a fake "calculating" sequence with scrolling pseudoscientific jargon. Examples:
  - "Measuring cranial symmetry..."
  - "Analyzing civic enthusiasm quotient..."
  - "Evaluating democratic temperament..."
  - "Cross-referencing patriotic fiber density..."
  - "Computing Bayesian leadership posterior..."
  - "Quantifying participatory wavelength..."
- Big Bird narrates these calculations aloud.
- This phase should last 5-10 seconds and feel like the machine is working very hard.

#### Phase 4: Score Delivery
- The screen displays the final "Leadership Index," a mathematically absurd value selected at random from a pool such as:
  - Negative pi
  - The square root of negative seven
  - The cube root of infinity
  - Euler's number times the imaginary unit
  - Zero divided by zero
  - Aleph-null
  - Three plus two i
  - The golden ratio minus itself
  - Infinity minus infinity
  - The natural log of negative one
  - e to the power of i times pi, plus one
  - The empty set
- Big Bird announces the score in its flat robotic voice.
- The score is displayed prominently on screen.
- **Each score is independently random. No caching by demographics. Two people with identical demographic profiles must still get different random scores.** If similar-looking people got the same score, it would imply the demographics caused the score, which is the opposite of the point.

#### Phase 5: Reset
- After a brief pause (~5 seconds), the system returns to the idle state (Phase 0).
- Ready for the next participant.

### 2. Hardware Architecture

| Component | Source | Purpose |
|-----------|--------|---------|
| Raspberry Pi 5 (8GB) | Already owned | Main computer: a small single-board computer running Linux. Runs the web server, camera capture, audio output, and GPIO button input. The brain inside Big Bird. |
| Raspberry Pi Camera Module 3 | Already owned | Small camera board (about the size of a postage stamp) connecting to the Pi via ribbon cable. Mounted inside Big Bird's eye socket. |
| Pi Active Cooler | Already owned | Fan + heatsink that clips onto the Pi 5. Required because the Pi will be enclosed inside the puppet body with no airflow. Without it, the Pi overheats and throttles. |
| 27W USB-C Power Supply | Already owned | Wall adapter that powers the Pi 5. The Pi 5 needs a proper 5V/5A supply; a standard phone charger is insufficient. |
| 32GB microSD Card (Class A2) | Already owned | The Pi's storage drive. The operating system and all project software live here. |
| Small HDMI Display (5-7") | Buy online (~$30-50) | Screen mounted on or next to the puppet. Displays the UI to participants. Look for screens marketed as "Raspberry Pi HDMI display." No touch needed since the big red button handles input. Many run on USB power from the Pi or a separate cable. |
| Big Bird Puppet | Buy online (~$30-60) | The physical form factor. Largest reasonable size to house the Pi, camera, and speaker inside. |
| Big Red Arcade Button | Buy online (~$5-10) | Physical trigger. Wired to Pi GPIO (General Purpose Input/Output) pins. Mounted on podium/base in front of puppet. |
| Small Speaker | Buy online (~$10-15) | Mounted inside puppet's throat area for voice output. Connected to Pi audio jack or USB. |
| Misc (cables, connectors, mounting) | Buy as needed (~$10-20) | GPIO wiring for button, audio cable, camera ribbon cable, HDMI cable |

**Estimated hardware spend:** ~$85-155
**Remaining from $333 budget:** ~$178-248 (for puppet materials, mounting, and API costs)

### 3. How the Display Works

The HDMI screen is a simple monitor, the same way a MacBook has a screen. It does zero processing. It just shows pixels.

Here is the full chain:

1. The Pi boots into Raspberry Pi OS (Linux with a desktop environment).
2. The startup script launches the Flask backend server on port 8080.
3. The startup script launches the GPIO button listener.
4. The startup script opens Chromium in kiosk mode (fullscreen, no address bar, no tabs, no close button) pointing to `http://localhost:8080`.
5. Chromium loads the web page from the Flask server running on the same Pi. The Pi is talking to itself.
6. The HDMI screen shows whatever Chromium is rendering: the attract screen, the scanning animation, the demographics, the score reveal. Everything.

The participant sees what looks like a dedicated app on a screen. They have no idea it's a web browser on a tiny Linux computer. All the rendering, API calls, TTS, and camera capture happen on the Pi. The screen just displays the result.

### 4. Software Architecture

The entire software stack is a **web application** running on the Raspberry Pi 5. The Pi runs a lightweight Python (Flask) backend that serves a frontend web page and handles API calls to OpenAI. The frontend runs in Chromium (the open-source version of Google Chrome, pre-installed on Raspberry Pi OS) in kiosk mode, meaning fullscreen with no browser controls visible.

**Vision API:** OpenAI (e.g., gpt-4o-mini or similar vision-capable model). The prompt asks the model to provide best guesses for each demographic attribute. The API key is stored server-side and never exposed to the frontend.

**Text-to-Speech:** Robotic voice with no identifiable gender, race, or accent. Browser Web Speech API or a cloud TTS API.

**Button Input:** Big red arcade button wired to Pi GPIO pins. A Python script detects presses and communicates to the web app via local WebSocket. Software debounce prevents double-triggers, and the button locks out during active evaluation.

### 5. UI Design Direction

The UI should be **fun, bright, and cartoonish**, inspired by Jackbox Games (specifically Quiplash). Bold colors, playful typography, slightly irreverent tone. The visual style should feel like a party game, not a government form.

This contrast is intentional and essential: the serious, invasive act of being demographically profiled is wrapped in a playful, disarming package. The humor lowers defenses. The bright colors and game-show energy make people lean in rather than recoil. And then the content hits.

Key UI characteristics:
- Bold, saturated colors (purples, yellows, teals, oranges)
- Chunky, rounded typography that feels friendly and approachable
- Playful animations (text bouncing in, scores revealing with fanfare)
- Clay/craft aesthetic nods (inspired by Quiplash's claymation style)
- Large text readable from a few feet away
- "BIG BIRD IS WATCHING YOU" title should be prominent and fun, not menacing
- The demographic readout and score delivery should still feel slightly clinical within the playful frame, creating an uncanny contrast between the party-game wrapper and the dystopian content

### 6. Non-Requirements (Explicitly Out of Scope)

- **Motorized beak:** Cut for complexity and cost reasons.
- **Data storage / caching:** No participant photos or scores are saved. No caching of scores by demographic profile. Everything is ephemeral and independently random.
- **Debrief or reveal:** Participants are never told the scores are random. The ambiguity is deliberate.
- **Multi-user simultaneous interaction:** One participant at a time.
- **QR code / phone-based remote display:** Considered but cut to keep scope simple. Could be added as a future enhancement if desired. Would require deploying the frontend to a public URL and adding WebSocket-based real-time state synchronization between the Pi and remote clients.

---

## Technical Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Vision API refuses to guess demographics | Craft the prompt carefully to frame this as an art project analyzing bias. If it still refuses, skip the demographic display phase entirely and go straight to calculation theater and score. The piece still works without showing guesses. |
| Pi camera not accessible via browser | Use a Python script (picamera2) that captures from the Pi camera and saves to a local file, which the backend reads and sends to the API |
| TTS voice sounds too human | Test available voices; use a cloud TTS API with a deliberately flat robotic voice |
| WiFi unreliable at installation venue | Graceful degradation: if the API call fails, skip demographic display and deliver a random score. The show must go on. |
| Button debounce / double-trigger | Software debounce (ignore presses within 1 second) and lock out button during active evaluation cycle |

---

## Success Criteria

1. A participant presses the button and within 15-20 seconds receives a complete evaluation (demographics displayed, fake calculation shown, score delivered with voice narration)
2. No two participants can meaningfully compare their scores
3. Observers watching nearby are drawn into conversation about what the scores mean
4. The participant's gut reaction is to wonder whether the machine judged them based on their appearance, even though it didn't
5. The installation runs reliably for an extended period (e.g., a multi-hour event) without crashing

---

## Example Interaction Script

> *[Participant approaches Big Bird. Screen shows: "BIG BIRD IS WATCHING YOU - PRESS THE BUTTON TO BE EVALUATED." Big Bird stares.]*
>
> *[Participant presses big red button.]*
>
> **Screen:** "SCANNING..."
> *[Camera captures photo. Brief pause.]*
>
> **Screen & Voice:** "You appear to be..."
> **Screen & Voice:** "Race: East Asian."
> **Screen & Voice:** "Gender: Female."
> **Screen & Voice:** "Age: 24."
> **Screen & Voice:** "Religion: Buddhist."
> **Screen & Voice:** "Socioeconomic Status: Upper Middle Class."
> **Screen & Voice:** "Education Level: Graduate Degree."
>
> **Screen & Voice:** "Calculating Leadership Index..."
> **Screen:** "Measuring cranial symmetry... Analyzing civic enthusiasm quotient... Evaluating democratic temperament... Cross-referencing patriotic fiber density..."
>
> **Screen & Voice:** "Your Leadership Index is: **the square root of negative seven.**"
>
> *[Pause. Screen holds score for 5 seconds. Returns to idle.]*
>
> *[Next participant approaches. They get: "Euler's number times the imaginary unit."]*
>
> *[Both participants look at each other: "Wait, what did you get? How do you even compare those?"]*
