---
name: designing-frontend-taste
description: Designs distinctive, high-taste frontends with intentional typography, layout variance, and motion choreography. Eliminates generic AI web defaults and templates. Use when building landing pages, portfolios, marketing sites, or modern web interfaces.
---

# Designing Frontend Taste (Anti-Slop Framework)

A specialized design engineering skill that eliminates generic, templated AI web aesthetics. Gated by brief inference and the three core design dials: **VARIANCE**, **MOTION**, and **DENSITY**.

## When to use this skill
- Building landing pages (SaaS, consumer, agency, events)
- Designing creative portfolios (developers, designers, studios)
- Upgrading generic AI frontend boilerplate to agency-grade quality
- Triggered by requests mentioning "taste", "Awwwards", "anti-slop", "premium frontend", "editorial layout", or "bespoke UI"

## Workflow Checklist
Copy and track this checklist during frontend generation:
- [ ] 1. **Brief Inference**: Output the one-line Design Read before writing code.
- [ ] 2. **Dial Calibration**: Set `DESIGN_VARIANCE`, `MOTION_INTENSITY`, and `VISUAL_DENSITY`.
- [ ] 3. **Layout Selection**: Apply asymmetrical bento, broken grid, or editorial split (no generic 3-card rows).
- [ ] 4. **Typographic Pair**: Select bespoke display + high-legibility body fonts with tight headline tracking.
- [ ] 5. **Surface & Palette**: Set background tone (off-black or warm bone), max 1 accent color, tinted shadows.
- [ ] 6. **Pre-Flight Validation**: Run the anti-slop audit before final output.

## 1. Brief Inference & The Design Read
Before generating code or styling, read the room and declare in one line:
> **"Reading this as: [page kind] for [audience], with a [vibe] language, leaning toward [design system/aesthetic]."**

### Absolute Negative Defaults (Banned Patterns)
- ❌ No AI-purple/cyan gradients or generic mesh backgrounds
- ❌ No centered hero with identical 3-column feature cards
- ❌ No default Inter + slate-900 combinations
- ❌ No infinite-loop floating badges or aimless micro-animations
- ❌ No generic marketing jargon ("Next-Gen", "Seamless", "Elevate")

## 2. The Three Dials
Every layout, motion, and density decision is governed by three calibrated dials (1–10):
- **`DESIGN_VARIANCE`** (Default: 8): `1` = rigid symmetry, `10` = artistic experimental asymmetry.
- **`MOTION_INTENSITY`** (Default: 6): `1` = static editorial, `10` = cinematic physics/scroll-driven.
- **`VISUAL_DENSITY`** (Default: 4): `1` = art gallery airy, `10` = dense telemetry cockpit.

See [Dials and Presets Reference](resources/dials-and-presets.md) for full use-case calibration mappings.

## 3. Structural Layout Architecture
Select one asymmetric layout archetype rather than symmetrical columns:

### Asymmetrical Bento Grid
```tsx
<div className="grid grid-cols-1 md:grid-cols-12 gap-6">
  {/* Dominant anchor card */}
  <div className="md:col-span-8 p-8 rounded-2xl bg-card border border-border/40">
    <h3 className="text-3xl font-display font-semibold tracking-tight">Primary Value Proposition</h3>
    <p className="mt-4 text-muted-foreground max-w-xl">Rich visual or interactive preview goes here.</p>
  </div>
  {/* Secondary metric card */}
  <div className="md:col-span-4 p-8 rounded-2xl bg-muted/30 border border-border/40 flex flex-col justify-between">
    <span className="text-xs font-mono uppercase tracking-widest text-muted-foreground">Realtime Telemetry</span>
    <span className="text-5xl font-mono font-bold tracking-tighter mt-6">99.98%</span>
  </div>
</div>
```

### Editorial Split
Massive display typography on the left (`md:w-1/2`), staggered interactive cards or horizontal preview pills on the right (`md:w-1/2`). Mobile always collapses to full width (`w-full`).

## 4. Typography & Color Science
- **Display Type**: Choose high-character display faces (`Geist`, `Cabinet Grotesk`, `Clash Display`, `Instrument Serif`, `Syne`).
- **Tracking Rules**: Apply tight tracking on large display headers (`tracking-tight` or `letter-spacing: -0.03em`). Generous tracking on uppercase badges/mono metadata (`tracking-widest` or `0.08em`).
- **Background Physics**: Avoid `#000000` or `#ffffff`. Use tinted darks (`#0a0a0c`, `#0f1115`) or warm bones (`#fbfbfa`, `#f7f6f3`).
- **Shadow Tinting**: Never use pure black drop shadows. Always tint shadows with background hue at low opacity (< 0.06).

## 5. Pre-Flight Validation
Execute the [Anti-Slop Audit Checklist](resources/anti-slop-checklist.md) prior to delivering code:
1. Did you output the one-line Design Read?
2. Are headlines set with character-rich fonts and tight tracking?
3. Is layout free of generic three-column feature cards?
4. Are buttons using clear hierarchy (1 primary solid action, secondary outline/ghost)?
5. Does the layout gracefully collapse on mobile screens (`< 768px`)?

## Resources
- [Dials and Presets Table](resources/dials-and-presets.md)
- [Anti-Slop Audit Checklist](resources/anti-slop-checklist.md)
