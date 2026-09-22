const canvas = document.getElementById("galaxy-canvas");
const ctx = canvas.getContext("2d");

const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
).matches;


/* ---------- CANVAS ---------- */

let width = window.innerWidth;
let height = window.innerHeight;

function resizeCanvas() {
    width = window.innerWidth;
    height = window.innerHeight;

    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    canvas.width = width * dpr;
    canvas.height = height * dpr;

    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

resizeCanvas();

window.addEventListener("resize", resizeCanvas);


/* ---------- PARTICLES ---------- */

const particles = [];

function createParticles() {
    particles.length = 0;

    const area = width * height;
    const count = Math.floor(area / 7000);

    const particleCount = Math.max(
        70,
        Math.min(count, 200)
    );

    for (let i = 0; i < particleCount; i++) {

        const depth = Math.random();

        const particle = {
            x: Math.random() * width,
            y: Math.random() * height,

            homeX: 0,
            homeY: 0,

            velocityX: 0,
            velocityY: 0,

            driftX: (Math.random() - 0.5) * 0.08,
            driftY: (Math.random() - 0.5) * 0.08,

            radius: 0.5 + depth * 1.2,

            opacity: 0.20 + depth * 0.50,

            depth: depth
        };

        particle.homeX = particle.x;
        particle.homeY = particle.y;

        particles.push(particle);
    }
}

createParticles();


/* ---------- CURSOR PHYSICS ---------- */

const physics = {
    interactionRadius: 260,
    mouseStrength: 0.13,
    springStrength: 0.006,
    damping: 0.88
};

const mouse = {
    x: 0,
    y: 0,
    active: false
};

window.addEventListener("mousemove", (event) => {
    mouse.x = event.clientX;
    mouse.y = event.clientY;
    mouse.active = true;
});

window.addEventListener("mouseleave", () => {
    mouse.active = false;
});


/* ---------- CONNECTIONS ---------- */

const connections = {
    maxDistance: 135,
    maxOpacity: 0.16
};


/* ---------- PULSES ---------- */

const pulses = {
    active: [],
    maxActive: 4,
    spawnChance: 0.005,
    speed: 0.8
};

function spawnPulse() {

    if (particles.length < 2) {
        return;
    }

    const firstIndex =
        Math.floor(Math.random() * particles.length);

    const secondIndex =
        Math.floor(Math.random() * particles.length);

    if (firstIndex === secondIndex) {
        return;
    }

    const first = particles[firstIndex];
    const second = particles[secondIndex];

    const dx = second.x - first.x;
    const dy = second.y - first.y;

    const distance = Math.sqrt(
        dx * dx + dy * dy
    );

    if (
        distance === 0 ||
        distance > connections.maxDistance
    ) {
        return;
    }

    pulses.active.push({
        x1: first.x,
        y1: first.y,

        x2: second.x,
        y2: second.y,

        progress: 0,

        speed:
            pulses.speed *
            (0.75 + Math.random() * 0.5)
    });
}


/* ---------- UPDATE PARTICLES ---------- */

function updateParticles() {

    for (const particle of particles) {

        /*
         * Natural drift is applied directly
         * to position so momentum does not
         * continuously accumulate.
         */

        if (!prefersReducedMotion) {
            particle.x += particle.driftX;
            particle.y += particle.driftY;
        }


        /* Spring force */

        const springX =
            (particle.homeX - particle.x) *
            physics.springStrength;

        const springY =
            (particle.homeY - particle.y) *
            physics.springStrength;

        particle.velocityX += springX;
        particle.velocityY += springY;


        /* Cursor force */

        if (
            mouse.active &&
            !prefersReducedMotion
        ) {

            const dx =
                mouse.x - particle.x;

            const dy =
                mouse.y - particle.y;

            const distance =
                Math.sqrt(
                    dx * dx +
                    dy * dy
                );

            if (
                distance > 0 &&
                distance < physics.interactionRadius
            ) {

                const normalizedX =
                    dx / distance;

                const normalizedY =
                    dy / distance;

                const falloff =
                    1 -
                    distance /
                    physics.interactionRadius;

                const force =
                    physics.mouseStrength *
                    falloff *
                    (0.5 + particle.depth);

                particle.velocityX +=
                    normalizedX * force;

                particle.velocityY +=
                    normalizedY * force;
            }
        }


        /* Damping */

        particle.velocityX *=
            physics.damping;

        particle.velocityY *=
            physics.damping;


        /* Apply velocity */

        particle.x +=
            particle.velocityX;

        particle.y +=
            particle.velocityY;


        /* Screen wrapping */

        if (particle.x < -20) {
            particle.x = width + 20;
            particle.homeX = particle.x;
        }

        if (particle.x > width + 20) {
            particle.x = -20;
            particle.homeX = particle.x;
        }

        if (particle.y < -20) {
            particle.y = height + 20;
            particle.homeY = particle.y;
        }

        if (particle.y > height + 20) {
            particle.y = -20;
            particle.homeY = particle.y;
        }
    }
}


/* ---------- DRAW PARTICLES ---------- */

function drawParticles() {

    for (const particle of particles) {

        const opacity =
            particle.opacity;

        ctx.beginPath();

        ctx.arc(
            particle.x,
            particle.y,
            particle.radius,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            `rgba(190, 198, 220, ${opacity})`;

        ctx.fill();
    }
}


/* ---------- DRAW CONNECTIONS ---------- */

function drawConnections() {

    for (
        let i = 0;
        i < particles.length;
        i++
    ) {

        const first =
            particles[i];

        for (
            let j = i + 1;
            j < particles.length;
            j++
        ) {

            const second =
                particles[j];

            const dx =
                second.x - first.x;

            const dy =
                second.y - first.y;

            const distance =
                Math.sqrt(
                    dx * dx +
                    dy * dy
                );

            if (
                distance >
                connections.maxDistance
            ) {
                continue;
            }

            const opacity =
                (1 -
                    distance /
                    connections.maxDistance) *
                connections.maxOpacity;

            ctx.beginPath();

            ctx.moveTo(
                first.x,
                first.y
            );

            ctx.lineTo(
                second.x,
                second.y
            );

            ctx.strokeStyle =
                `rgba(150, 160, 190, ${opacity})`;

            ctx.lineWidth = 0.6;

            ctx.stroke();
        }
    }
}


/* ---------- UPDATE PULSES ---------- */

function updatePulses() {

    if (prefersReducedMotion) {
        pulses.active.length = 0;
        return;
    }

    if (
        pulses.active.length <
        pulses.maxActive &&
        Math.random() <
        pulses.spawnChance
    ) {
        spawnPulse();
    }

    for (
        let i = pulses.active.length - 1;
        i >= 0;
        i--
    ) {

        const pulse =
            pulses.active[i];

        pulse.progress +=
            pulse.speed / 100;

        if (pulse.progress >= 1) {
            pulses.active.splice(i, 1);
        }
    }
}


/* ---------- DRAW PULSES ---------- */

function drawPulses() {

    for (const pulse of pulses.active) {

        const x =
            pulse.x1 +
            (pulse.x2 - pulse.x1) *
            pulse.progress;

        const y =
            pulse.y1 +
            (pulse.y2 - pulse.y1) *
            pulse.progress;

        ctx.beginPath();

        ctx.arc(
            x,
            y,
            1.5,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            "rgba(180, 190, 220, 0.75)";

        ctx.fill();
    }
}


/* ---------- ANIMATION LOOP ---------- */

function animate() {

    ctx.clearRect(
        0,
        0,
        width,
        height
    );

    updateParticles();

    updatePulses();

    drawConnections();

    drawParticles();

    drawPulses();

    requestAnimationFrame(animate);
}


animate();