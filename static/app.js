/* Big Bird frontend — SocketIO client, phase state machine, spacebar handler */

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

    /**
     * Transition the UI to the given phase.
     * Hides all phase divs, shows the matching one, updates debug status.
     */
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
    // SocketIO event listeners
    // -----------------------------------------------------------------------
    socket.on("phase_change", function (data) {
        if (data && data.phase) {
            setPhase(data.phase);
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
    // Initialize on load
    // -----------------------------------------------------------------------
    setPhase("IDLE");
})();
