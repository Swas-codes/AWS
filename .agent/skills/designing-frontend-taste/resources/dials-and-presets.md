# Dials and Presets Reference

Global configuration values driving variance, animation, and density.

## Dial Presets by Archetype

| Use Case | DESIGN_VARIANCE (1-10) | MOTION_INTENSITY (1-10) | VISUAL_DENSITY (1-10) | Typography Family |
| :--- | :---: | :---: | :---: | :--- |
| **SaaS Landing (Mainstream)** | 7 | 6 | 4 | Sans Grotesk + Geist Mono |
| **Agency / Creative Studio** | 9 | 8 | 3 | Editorial Serif + Geometric Sans |
| **Premium Consumer Product** | 7 | 6 | 3 | High-character Sans + Soft Accents |
| **Designer Portfolio** | 8 | 7 | 3 | Kinetic Display + Clean Mono |
| **Developer Portfolio** | 6 | 5 | 4 | Clean Technical Sans + Dense Code Blocks |
| **Editorial / Long-form Blog** | 6 | 4 | 3 | Serif Display + High-legibility Body |
| **Technical Telemetry / Cockpit** | 4 | 3 | 7 | Fixed Monospace + Modular Grid |

## Dial Rules & Behavior

### DESIGN_VARIANCE
- **1–3 (Symmetrical)**: Fixed grid columns, strict alignment, centered layouts.
- **4–7 (Dynamic)**: Off-center hero, alternating card sizes, deliberate negative space.
- **8–10 (Artistic)**: Overlapping z-index cards, diagonal bleed elements, extreme scale contrast.

### MOTION_INTENSITY
- **1–3 (Subtle)**: Opacity transitions only, zero layout shifts.
- **4–6 (Interactive)**: Hover scale (`1.02`), spring-eased accordions, scroll-reveals.
- **7–10 (Cinematic)**: Kinetic typography, GSAP scrubbed paths, dynamic cursor/parallax effects.

### VISUAL_DENSITY
- **1–3 (Airy/Gallery)**: Massive section padding (`py-24` to `py-36`), large white space, minimal elements per viewport.
- **4–6 (Balanced)**: Standard web SaaS layout (`py-16` to `py-20`), generous line-heights (`1.6`).
- **7–10 (Compact)**: Condensed table cells, compact card paddings (`p-3` to `p-4`), small font scales (`12px` to `14px`).
