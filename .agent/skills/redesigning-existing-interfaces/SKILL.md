---
name: redesigning-existing-interfaces
description: Audits and elevates existing websites and applications to premium agency quality without breaking functionality. Identifies and fixes generic AI design defaults, poor typography, flat color palettes, and awkward spacing while preserving the existing tech stack. Use when the user asks to redesign, audit, elevate, or polish an existing UI.
---

# Redesigning Existing Interfaces

An audit-first frontend engineering skill for systematically diagnosing and elevating legacy or AI-generated interfaces into premium, agency-quality products without rewriting codebases from scratch.

## When to use this skill
- Elevating existing websites, landing pages, or web apps that look generic or unpolished
- Refactoring AI-generated boilerplate to feel custom, thoughtful, and high-taste
- Preserving business logic, API connections, and core architecture while overhauling UI
- Triggered by keywords: "redesign", "audit UI", "polish existing app", "fix UI slop", "make this look professional", "elevate design"

## Workflow: Scan → Diagnose → Fix
Do not rewrite from scratch. Follow this strict sequence:
- [ ] 1. **Scan**: Inspect existing styling engine (Tailwind, CSS Modules, vanilla CSS) and component hierarchy.
- [ ] 2. **Diagnose**: Run the Redesign Audit across typography, colors, layout, and states.
- [ ] 3. **Fix Typography**: Tighten headlines, constrain paragraph widths (`max-w-xl`), apply `text-wrap: balance`.
- [ ] 4. **Fix Surfaces**: Eliminate dead black/pure gray; introduce consistent warm/cool tinting and diffuse shadows.
- [ ] 5. **Fix Layout**: Break symmetrical repetition with asymmetric focal points and intentional spacing.
- [ ] 6. **Validate Functionality**: Ensure responsive mobile layouts, form usability, and all interactive states remain intact.

## The Redesign Audit Protocol

### 1. Typography Upgrades
- **Problem**: Default Inter or browser fonts with generic weighting.
  - **Fix**: Elevate to high-character typography (`Geist`, `Cabinet Grotesk`, `Outfit`, or an editorial serif for headings).
- **Problem**: Headlines lack presence or look like large body copy.
  - **Fix**: Increase scale contrast, apply tight tracking (`tracking-tight` / `-0.025em`), and reduce line-height (`1.15`).
- **Problem**: Paragraphs stretch edge-to-edge across wide viewports.
  - **Fix**: Constrain line lengths to ~65 characters (`max-w-xl` to `max-w-2xl`) with line-height of `1.6`.
- **Problem**: Single orphan words sitting alone on the final line of headings.
  - **Fix**: Add `text-wrap: balance` or `text-wrap: pretty`.

### 2. Color & Surface Upgrades
- **Problem**: Dead pitch black (`#000000`) or sterile gray backgrounds.
  - **Fix**: Replace with rich charcoal or tinted darks (`#0a0a0c`, `#0e1117`) or warm bone substrates (`#fbfbfa`).
- **Problem**: Oversaturated, competing neon accent colors.
  - **Fix**: Restrict to one primary accent with saturation below 80%.
- **Problem**: Harsh, muddy black drop shadows (`shadow-md`).
  - **Fix**: Tint shadows to match substrate hue and lower opacity to under 0.05.

### 3. Layout & Structure Upgrades
- **Problem**: Repetitive, identical 3-column card rows.
  - **Fix**: Introduce asymmetrical bento grids (`col-span-8` anchor with `col-span-4` telemetry).
- **Problem**: Uniform, cramped padding throughout all sections.
  - **Fix**: Expand section macro-padding (`py-20` to `py-28`) to give content room to breathe.

### 4. Interactive Polish
- **Problem**: Abrupt hover state snaps or standard linear easing.
  - **Fix**: Use natural easing curves (`transition-all duration-300 ease-out` or spring physics).
- **Problem**: Missing focus-visible and active states.
  - **Fix**: Add distinct `focus-visible:ring-2 focus-visible:ring-primary/40` and `active:scale-[0.98]`.
