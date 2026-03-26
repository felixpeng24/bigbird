# Big Bird is Watching You

An interactive art installation where a Big Bird puppet evaluates participants' "Leadership Index" using fake pseudoscientific analysis and delivers a mathematically absurd, incomparable score.

The piece critiques algorithmic bias and the human impulse to be measured by systems that appear authoritative but are fundamentally arbitrary. The name references Orwell's *1984* — surveillance and authoritarian judgment subverted by a children's character with no race, gender, ethnicity, or age.

## How It Works

1. **Idle** — Screen displays "BIG BIRD IS WATCHING YOU." Participant approaches.
2. **Capture** — Participant presses a big red arcade button. A camera in Big Bird's eye captures a photo.
3. **Demographic Analysis** — A vision API guesses race, gender, age, religion, socioeconomic status, and education level. These are displayed on screen and narrated aloud. **Every attribute has a weight of zero in the scoring formula.**
4. **Calculation Theater** — Pseudoscientific jargon scrolls on screen ("Measuring cranial symmetry...", "Quantifying participatory wavelength...") for 5–10 seconds.
5. **Score Delivery** — A mathematically absurd value is delivered: negative pi, the square root of negative seven, aleph-null, e^(iπ)+1, etc. Scores are independently random and structurally incomparable — you cannot rank pi against infinity.
6. **Reset** — Returns to idle after 5 seconds.

## Why It Works

Participants experience a machine that looks at them, appears to think very hard, and delivers a judgment. In the gap between appearance and reality, people reveal their own assumptions — wondering whether their race affected the score, whether someone who "looked different" would score better. They project the biases they carry onto a system that carries none.

## Hardware

- **Raspberry Pi 5 (8GB)** — Main computer running the web server, camera, audio, and GPIO button input
- **Pi Camera Module 3** — Mounted inside Big Bird's eye socket
- **5–7" HDMI Display** — Mounted on or next to the puppet
- **Big Red Arcade Button** — Wired to Pi GPIO, mounted on a podium
- **Small Speaker** — Inside the puppet for robotic voice narration
- **Big Bird Puppet** — Houses all components

## Software

- **Backend:** Python (Flask) running on the Pi, serving the frontend and handling API calls
- **Frontend:** Web app running in Chromium kiosk mode (fullscreen, no browser UI)
- **Vision API:** OpenAI (gpt-4o-mini or similar) for demographic guesses
- **TTS:** Robotic voice with no identifiable gender, race, or accent
- **Button Input:** GPIO → Python script → WebSocket → web app

## Course Context

Created for **"The Game of Democracy: Art, Engineering, Chance, Choice, and Civic Life"** — a course using Taryn Simon's *Kleroterion* (2024) as an organizing metaphor. The Kleroterion was an ancient Athenian sortition device that randomly selected citizens for public office. Big Bird extends this logic: if every system that claims to evaluate human potential is contaminated by bias, then perhaps the most honest output is one that means nothing at all.

## Design Direction

Fun, bright, and cartoonish — inspired by Jackbox Games. Bold saturated colors, chunky rounded typography, playful animations. The contrast is intentional: the serious act of being demographically profiled is wrapped in a disarming party-game package.
