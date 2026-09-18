import { useEffect, useRef, useState, useCallback } from 'react';

interface Particle {
  id: number;
  x: number;
  y: number;
  size: number;
}

let particleId = 0;

/**
 * RobotFollower — a CSS-drawn robot that smoothly follows the mouse cursor
 * with blinking eyes, glowing core, and a particle trail.
 */
export default function RobotFollower() {
  const containerRef = useRef<HTMLDivElement>(null);
  const posRef = useRef({ x: window.innerWidth / 2, y: window.innerHeight / 2 });
  const targetRef = useRef({ x: window.innerWidth / 2, y: window.innerHeight / 2 });
  const rafRef = useRef<number>(0);
  const lastParticleRef = useRef(0);

  const [blinking, setBlinking] = useState(false);
  const [particles, setParticles] = useState<Particle[]>([]);

  /* ── Smooth follow via requestAnimationFrame ────────────── */
  const animate = useCallback(() => {
    const el = containerRef.current;
    if (!el) return;

    const lerp = 0.08;
    posRef.current.x += (targetRef.current.x - posRef.current.x) * lerp;
    posRef.current.y += (targetRef.current.y - posRef.current.y) * lerp;

    el.style.left = `${posRef.current.x}px`;
    el.style.top  = `${posRef.current.y}px`;

    rafRef.current = requestAnimationFrame(animate);
  }, []);

  useEffect(() => {
    rafRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(rafRef.current);
  }, [animate]);

  /* ── Track mouse position ───────────────────────────────── */
  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      targetRef.current.x = e.clientX;
      targetRef.current.y = e.clientY;

      /* spawn particle every 60ms of movement */
      const now = Date.now();
      if (now - lastParticleRef.current > 60) {
        lastParticleRef.current = now;
        const id = ++particleId;
        const size = 2 + Math.random() * 4;
        setParticles(prev => [...prev.slice(-12), { id, x: e.clientX, y: e.clientY, size }]);

        /* auto-remove after animation ends */
        setTimeout(() => {
          setParticles(prev => prev.filter(p => p.id !== id));
        }, 800);
      }
    };

    window.addEventListener('mousemove', onMove);
    return () => window.removeEventListener('mousemove', onMove);
  }, []);

  /* ── Periodic blink ─────────────────────────────────────── */
  useEffect(() => {
    const scheduleBlink = () => {
      const delay = 2000 + Math.random() * 4000;    // blink every 2–6 s
      return setTimeout(() => {
        setBlinking(true);
        setTimeout(() => setBlinking(false), 180);   // blink duration
        timer = scheduleBlink();
      }, delay);
    };
    let timer = scheduleBlink();
    return () => clearTimeout(timer);
  }, []);

  /* ── Touch support for mobile ───────────────────────────── */
  useEffect(() => {
    const onTouch = (e: TouchEvent) => {
      const t = e.touches[0];
      if (t) {
        targetRef.current.x = t.clientX;
        targetRef.current.y = t.clientY;
      }
    };
    window.addEventListener('touchmove', onTouch, { passive: true });
    return () => window.removeEventListener('touchmove', onTouch);
  }, []);

  return (
    <>
      {/* Particle trail */}
      {particles.map(p => (
        <div
          key={p.id}
          className="particle"
          style={{
            left: p.x,
            top: p.y,
            width: p.size,
            height: p.size,
          }}
        />
      ))}

      {/* Robot */}
      <div ref={containerRef} className="robot-container">
        <div className="robot-body">
          {/* Antenna */}
          <div className="robot-antenna" />

          {/* Head */}
          <div className="robot-head">
            <div className={`robot-eye${blinking ? ' blink' : ''}`} />
            <div className={`robot-eye${blinking ? ' blink' : ''}`} />
          </div>

          {/* Neck */}
          <div className="robot-neck" />

          {/* Torso */}
          <div className="robot-torso">
            <div className="robot-core" />
            {/* Arms */}
            <div className="robot-arms">
              <div className="robot-arm robot-arm--left" />
              <div className="robot-arm robot-arm--right" />
            </div>
          </div>

          {/* Glow underneath */}
          <div className="robot-glow" />
        </div>
      </div>
    </>
  );
}
