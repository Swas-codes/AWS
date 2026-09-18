---
name: styling-luxury-interfaces
description: Engineers agency-tier, high-end visual designs with haptic depth, cinematic spatial rhythm, soft ambient lighting, and fluid spring motion physics. Blocks cheap AI defaults in favor of Apple-level and Linear-level polish. Use when the user requests luxury, high-end, expensive, calm, or Awwwards-tier web interfaces.
---

# Styling Luxury Interfaces (Agency-Tier)

An elite frontend architecture skill for crafting high-end, luxury digital experiences ($150k+ agency tier). Prioritizes haptic depth, tactile micro-interactions, airy whitespace, and fluid spring motion physics.

## When to use this skill
- Building luxury, high-end consumer brands and flagship SaaS products
- Designing bespoke agency websites, design portfolios, and premium landing experiences
- Polishing interfaces to feel expensive, calm, and tactile
- Triggered by keywords: "luxury UI", "expensive design", "Apple-like", "Linear-tier", "Awwwards", "soft lighting", "high-end frontend"

## Workflow Checklist
- [ ] 1. **Select Texture Archetype**: Choose Ethereal Glass, Editorial Luxury, or Soft Structuralism.
- [ ] 2. **Establish Spatial Rhythm**: Apply macro-padding (`py-24` to `py-36`) with generous margins.
- [ ] 3. **Implement Hairline Borders**: Use `border-white/10` (dark) or `border-black/5` (light) with backdrop blur.
- [ ] 4. **Configure Ambient Shadows**: Layer multiple low-opacity shadows with large blur radii (> 32px).
- [ ] 5. **Choreograph Spring Motion**: Set cubic-bezier easing (`cubic-bezier(0.16, 1, 0.3, 1)`) for micro-interactions.
- [ ] 6. **Ensure Mobile Fluidity**: Collapse all asymmetric elements to single columns with full touch padding.

## Texture Archetypes

### 1. Ethereal Glass (Dark Mode / High-Tech)
- **Canvas**: OLED black (`#050505`).
- **Surfaces**: Semi-transparent dark cards (`bg-neutral-900/40`) with `backdrop-blur-2xl` and pure white hairlines (`border-white/10`).
- **Lighting**: Subtle radial background glows (opacity < 15%) centered behind focal points.

### 2. Editorial Luxury (Warm Substrate / Lifestyle)
- **Canvas**: Warm ivory or cream (`#FDFBF7`) with espresso text (`#1C1917`).
- **Typography**: High-contrast variable serif display (`Instrument Serif`, `Newsreader`) with geometric sans accents.
- **Accents**: Muted sage, bronze, or terracotta.

### 3. Soft Structuralism (Light Mode / Airy)
- **Canvas**: Silver-gray or pure off-white (`#F8F9FA`).
- **Surfaces**: Crisp white floating cards elevated by ultra-diffuse ambient shadows:
  `box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.04), 0 0 1px rgba(0, 0, 0, 0.08)`.

## Component Code Template: Floating Glass Card
```tsx
<div className="group relative rounded-3xl border border-white/10 bg-white/[0.03] p-8 backdrop-blur-2xl transition-all duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] hover:-translate-y-1 hover:border-white/20 hover:bg-white/[0.05] hover:shadow-[0_24px_48px_-12px_rgba(0,0,0,0.5)]">
  {/* Ambient sheen on hover */}
  <div className="pointer-events-none absolute -inset-px rounded-3xl opacity-0 transition-opacity duration-500 group-hover:opacity-100 bg-gradient-to-b from-white/10 to-transparent" />

  <span className="text-xs font-mono uppercase tracking-widest text-neutral-400">Exclusive Cohort</span>
  <h3 className="mt-4 text-3xl font-display font-medium text-neutral-100 tracking-tight">Concierge Discovery</h3>
  <p className="mt-3 text-neutral-400 leading-relaxed text-sm">
    Architected for high-velocity teams seeking uncompromising aesthetic precision.
  </p>
</div>
```

## Motion Guidelines
- **Spring Easing**: Always use natural decelerations:
  `transition-all duration-500 ease-[cubic-bezier(0.16,1,0.3,1)]`
- **Interactive Scale**: Keep hover scales subtle (`hover:scale-[1.015]`), never clownish or abrupt.
