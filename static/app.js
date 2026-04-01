/* Big Bird frontend — full evaluation loop with TTS */

(function () {
    "use strict";

    // -----------------------------------------------------------------------
    // SocketIO connection
    // -----------------------------------------------------------------------
    var socket = io();

    // -----------------------------------------------------------------------
    // Phase state
    // -----------------------------------------------------------------------
    var currentPhase = "IDLE";
    var PHASES = ["IDLE", "CAPTURING", "ANALYZING", "CALCULATING", "REVEALING", "RESETTING"];

    // -----------------------------------------------------------------------
    // TTS wrapper
    // -----------------------------------------------------------------------
    var ttsQueue = [];
    var ttsSpeaking = false;

    function speak(text, callback) {
        if (!window.speechSynthesis) {
            console.warn("[TTS] speechSynthesis not available");
            if (callback) callback();
            return;
        }
        var utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.85;
        utterance.pitch = 0.7;
        utterance.volume = 1.0;
        utterance.onend = function () {
            console.log("[TTS] finished: " + text.substring(0, 40));
            if (callback) callback();
        };
        utterance.onerror = function () {
            console.warn("[TTS] error on: " + text.substring(0, 40));
            if (callback) callback();
        };
        console.log("[TTS] speaking: " + text.substring(0, 40));
        window.speechSynthesis.speak(utterance);
    }

    function cancelTTS() {
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
        }
    }

    // -----------------------------------------------------------------------
    // Calculation theater jargon
    // -----------------------------------------------------------------------
    var JARGON_LINES = [
        "Measuring cranial symmetry index...",
        "Computing Bayesian leadership posterior...",
        "Analyzing micro-expression confidence matrix...",
        "Calibrating phrenological neural mesh...",
        "Extracting socioeconomic gradient vectors...",
        "Running Monte Carlo competence simulation...",
        "Applying Fourier transform to ambition waveform...",
        "Normalizing charisma eigenvalues...",
        "Parsing hierarchical dominance topology...",
        "Interpolating executive function wavelets...",
        "Querying distributed authority consensus...",
        "Resolving quantum decisiveness superposition...",
        "Bootstrapping meritocratic confidence intervals...",
        "Compiling synergistic potential tensors...",
        "Deconvolving organizational aura spectrum...",
        "Fitting Gaussian to vision-alignment manifold...",
        "Hashing deterministic free-will coefficients...",
        "Optimizing bureaucratic inertia gradients...",
        "Sampling from posterior distribution of gravitas...",
        "Triangulating strategic hand-wave amplitude...",
    ];

    // -----------------------------------------------------------------------
    // Demographic labels
    // -----------------------------------------------------------------------
    var DEMOGRAPHIC_ORDER = ["race", "gender", "age", "socioeconomic_status", "education"];
    var DEMOGRAPHIC_LABELS = {
        race: "RACE",
        gender: "GENDER",
        age: "AGE",
        socioeconomic_status: "SOCIOECONOMIC STATUS",
        education: "EDUCATION LEVEL",
    };

    // -----------------------------------------------------------------------
    // Phase transition
    // -----------------------------------------------------------------------
    function setPhase(phase) {
        if (PHASES.indexOf(phase) === -1) {
            console.warn("[PHASE] Unknown phase: " + phase);
            return;
        }
        var oldPhase = currentPhase;
        currentPhase = phase;
        console.log("[PHASE] " + oldPhase + " -> " + phase);

        // Hide all phase divs, show the active one
        PHASES.forEach(function (p) {
            var el = document.getElementById("phase-" + p);
            if (el) {
                if (p === phase) {
                    el.classList.add("active");
                } else {
                    el.classList.remove("active");
                }
            }
        });

        // Update debug status
        var debugPhase = document.getElementById("debug-phase");
        if (debugPhase) {
            debugPhase.textContent = phase;
        }
    }

    // -----------------------------------------------------------------------
    // Demographic reveal
    // -----------------------------------------------------------------------
    function revealDemographics(demographics) {
        var container = document.getElementById("demographic-list");
        var refusalEl = document.getElementById("refusal-message");
        container.innerHTML = "";

        if (demographics.refused) {
            // Show refusal message
            refusalEl.classList.remove("hidden");
            speak("Subject defies classification.");
            return;
        }

        refusalEl.classList.add("hidden");
        speak("Subject analysis complete. Displaying results.");

        // Reveal each demographic one by one
        var delay = 1800; // ms between each attribute
        DEMOGRAPHIC_ORDER.forEach(function (key, index) {
            setTimeout(function () {
                var value = demographics[key] || "UNKNOWN";
                var label = DEMOGRAPHIC_LABELS[key] || key.toUpperCase();

                var row = document.createElement("div");
                row.className = "demographic-row";
                row.innerHTML = '<span class="demo-label">' + label + ':</span> <span class="demo-value">' + value + '</span>';
                container.appendChild(row);

                // TTS for each attribute
                var spokenLabel = label.toLowerCase().replace(/_/g, " ");
                speak(spokenLabel + ": " + value);
            }, delay * (index + 1));
        });
    }

    // -----------------------------------------------------------------------
    // Calculation theater
    // -----------------------------------------------------------------------
    function runCalculationTheater() {
        var container = document.getElementById("jargon-container");
        var progressBar = document.getElementById("calculation-progress");
        container.innerHTML = "";
        if (progressBar) progressBar.style.width = "0%";

        // Shuffle jargon and pick 6-8 lines
        var shuffled = JARGON_LINES.slice().sort(function () { return Math.random() - 0.5; });
        var lines = shuffled.slice(0, 7);
        var totalDuration = 7000; // 7 seconds total
        var interval = totalDuration / lines.length;

        // Speak the first line
        speak("Computing your Leadership Index. Please stand by.");

        lines.forEach(function (line, index) {
            setTimeout(function () {
                var el = document.createElement("div");
                el.className = "jargon-line";
                el.textContent = "> " + line;
                container.appendChild(el);

                // Auto-scroll
                container.scrollTop = container.scrollHeight;

                // Update progress
                var pct = Math.min(100, ((index + 1) / lines.length) * 100);
                if (progressBar) progressBar.style.width = pct + "%";
            }, interval * index);
        });
    }

    // -----------------------------------------------------------------------
    // Score reveal
    // -----------------------------------------------------------------------
    function revealScore(score) {
        var display = document.getElementById("score-display");
        display.textContent = score;
        display.className = "score-text";

        // Trigger entrance animation
        setTimeout(function () {
            display.classList.add("score-visible");
        }, 50);

        speak("Your Leadership Index has been calculated.");
    }

    // -----------------------------------------------------------------------
    // SocketIO event listeners
    // -----------------------------------------------------------------------
    socket.on("phase_change", function (data) {
        if (!data || !data.phase) return;

        var phase = data.phase;
        var phaseData = data.data || {};

        setPhase(phase);

        // Phase-specific behavior
        switch (phase) {
            case "CAPTURING":
                cancelTTS();
                speak("Hold still. Capturing subject for evaluation.");
                break;

            case "ANALYZING":
                if (phaseData.demographics) {
                    revealDemographics(phaseData.demographics);
                }
                break;

            case "CALCULATING":
                runCalculationTheater();
                break;

            case "REVEALING":
                if (phaseData.score) {
                    revealScore(phaseData.score);
                }
                break;

            case "RESETTING":
                speak("Evaluation complete. Returning to surveillance mode.");
                break;

            case "IDLE":
                cancelTTS();
                // Clear stale content
                var demoList = document.getElementById("demographic-list");
                if (demoList) demoList.innerHTML = "";
                var refusal = document.getElementById("refusal-message");
                if (refusal) refusal.classList.add("hidden");
                var jargon = document.getElementById("jargon-container");
                if (jargon) jargon.innerHTML = "";
                var scoreEl = document.getElementById("score-display");
                if (scoreEl) {
                    scoreEl.textContent = "";
                    scoreEl.className = "score-text";
                }
                var progressBar = document.getElementById("calculation-progress");
                if (progressBar) progressBar.style.width = "0%";
                break;
        }
    });

    socket.on("connect", function () {
        console.log("[SOCKET] connected");
        var debugSocket = document.getElementById("debug-socket");
        if (debugSocket) {
            debugSocket.textContent = "connected";
        }
    });

    socket.on("disconnect", function () {
        console.log("[SOCKET] disconnected");
        var debugSocket = document.getElementById("debug-socket");
        if (debugSocket) {
            debugSocket.textContent = "disconnected";
        }
    });

    // -----------------------------------------------------------------------
    // Spacebar handler — emits button_press to server
    // -----------------------------------------------------------------------
    document.addEventListener("keydown", function (e) {
        if (e.code === "Space" && !e.repeat) {
            e.preventDefault();
            console.log("[INPUT] spacebar pressed — emitting button_press");
            socket.emit("button_press");
        }
    });

    // -----------------------------------------------------------------------
    // Initialize
    // -----------------------------------------------------------------------
    setPhase("IDLE");
})();
