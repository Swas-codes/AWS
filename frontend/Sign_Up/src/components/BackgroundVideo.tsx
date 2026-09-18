import { useEffect, useRef } from 'react';

const VIDEO_SRC =
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260514_135830_bb6491d1-9b66-4aec-9722-13b4dfe3fb46.mp4';

/**
 * BackgroundVideo — autoplay/loop video with smooth mouse-parallax.
 *
 * The video shifts and scales subtly based on cursor position,
 * creating a cinematic depth effect. All transforms are GPU-accelerated
 * (only CSS `transform` changes — no layout, no paint, no video seeking).
 *
 * A lerp loop smooths the motion so it feels fluid, not jittery.
 */
export default function BackgroundVideo() {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    /* Slow the video down for a cinematic feel */
    video.playbackRate = 0.4;

    /* ── Config ── */
    const MAX_SHIFT = 20;   // max px the video moves
    const SCALE = 1.08;     // slight zoom so edges don't show when shifting
    const LERP = 0.06;      // smoothing factor (lower = smoother/slower)

    /* ── State ── */
    let targetX = 0;        // -1 … +1
    let targetY = 0;
    let currentX = 0;
    let currentY = 0;
    let rafId = 0;

    const onMouseMove = (e: MouseEvent) => {
      // Map mouse position to -1…+1 range (center = 0)
      targetX = (e.clientX / window.innerWidth) * 2 - 1;
      targetY = (e.clientY / window.innerHeight) * 2 - 1;
    };

    const tick = () => {
      // Lerp toward target
      currentX += (targetX - currentX) * LERP;
      currentY += (targetY - currentY) * LERP;

      // Apply transform: translate opposite to mouse + constant scale
      const tx = -currentX * MAX_SHIFT;
      const ty = -currentY * MAX_SHIFT;
      video.style.transform =
        `translate3d(${tx}px, ${ty}px, 0) scale(${SCALE})`;

      rafId = requestAnimationFrame(tick);
    };

    window.addEventListener('mousemove', onMouseMove, { passive: true });
    rafId = requestAnimationFrame(tick);

    return () => {
      window.removeEventListener('mousemove', onMouseMove);
      cancelAnimationFrame(rafId);
    };
  }, []);

  return (
    <video
      ref={videoRef}
      className="bg-video"
      autoPlay
      muted
      loop
      playsInline
    >
      <source src={VIDEO_SRC} type="video/mp4" />
    </video>
  );
}
