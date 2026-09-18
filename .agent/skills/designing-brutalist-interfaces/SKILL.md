---
name: designing-brutalist-interfaces
description: Architects raw, high-impact industrial brutalist and tactical telemetry web interfaces fusing Swiss typography with aerospace terminal aesthetics. Features rigid grids, extreme typographic contrast, technical brackets, and utilitarian accents. Use when building developer tools, engineering dashboards, or bold creative portfolios.
---

# Designing Brutalist & Tactical Interfaces

Advanced engineering directive for architecting web interfaces that synthesize mid-century Swiss Typographic design, industrial equipment blueprints, and tactical terminal interfaces. Enforces rigid modular grids, extreme scale contrast, and purely utilitarian color palettes.

## When to use this skill
- Developer tooling, CLI companions, and infrastructure dashboards
- Tactical telemetry, security operations, and aerospace/hardware interfaces
- Bold creative portfolios or underground editorial sites
- Triggered by keywords: "brutalist", "Swiss typography", "industrial UI", "terminal aesthetic", "tactical telemetry", "raw grid"

## Workflow Checklist
- [ ] 1. **Select Archetype**: Commit to either **Swiss Industrial Print** (Light) OR **Tactical Telemetry** (Dark). Do not mix.
- [ ] 2. **Construct Rigid Grid**: Apply explicit dividing borders (`border-2 border-black` or `border-neutral-800`).
- [ ] 3. **Implement Macro-Typography**: Render structural headers in heavy uppercase with compressed leading (`leading-[0.85]`).
- [ ] 4. **Implement Micro-Typography**: Render telemetry data and labels in uppercase monospace with loose tracking (`tracking-widest`).
- [ ] 5. **Deploy Technical Framing**: Add ASCII brackets, corner ticks, crosshairs, or index coordinates (`[SEC_01]`, `+---+`).
- [ ] 6. **Apply Utilitarian Accent**: Use a single functional accent (International Orange `#FF5500` or Safety Yellow `#FFEE00`).

## The Two Visual Archetypes

### Archetype A: Swiss Industrial Print (Light Mode)
- **Palette**: Heavy ink black (`#000000`) over newsprint bone (`#F4F4F0`).
- **Accent**: International Signal Red (`#E50000`) or Hazard Orange (`#FF5500`).
- **Characteristics**: Monolithic sans-serif typography, asymmetric negative space, visible architectural grid lines.

### Archetype B: Tactical Telemetry Terminal (Dark Mode)
- **Palette**: Void black (`#080808`) with phosphorescent green (`#00FF66`), amber (`#FFB000`), or cool technical white (`#ECECEC`).
- **Characteristics**: 100% monospaced typography, tabular metrics, crosshair coordinate corners, scanline textures.

## Component Code Template: Tactical Telemetry Card
```tsx
<div className="relative border border-neutral-800 bg-neutral-950 p-6 font-mono">
  {/* Corner crosshairs */}
  <span className="absolute -top-1.5 -left-1.5 text-neutral-600 text-xs select-none">+</span>
  <span className="absolute -top-1.5 -right-1.5 text-neutral-600 text-xs select-none">+</span>
  <span className="absolute -bottom-1.5 -left-1.5 text-neutral-600 text-xs select-none">+</span>
  <span className="absolute -bottom-1.5 -right-1.5 text-neutral-600 text-xs select-none">+</span>

  {/* Header telemetry */}
  <div className="flex justify-between items-center border-b border-neutral-800 pb-3 text-xs tracking-widest text-neutral-400 uppercase">
    <span>SYS_NODE // 04</span>
    <span className="text-amber-500 font-bold animate-pulse">[ONLINE]</span>
  </div>

  {/* Hero metric */}
  <div className="my-6">
    <span className="text-xs text-neutral-500 uppercase tracking-widest">Throughput Rate</span>
    <div className="text-4xl font-bold text-neutral-100 tracking-tighter mt-1">
      842.14 <span className="text-sm font-normal text-neutral-500">MB/S</span>
    </div>
  </div>

  {/* System metadata table */}
  <div className="grid grid-cols-2 gap-2 pt-3 border-t border-neutral-900 text-[11px] text-neutral-400">
    <div>LATENCY: 1.4ms</div>
    <div>BUFFER: 99.8%</div>
  </div>
</div>
```

## Resources
- [Telemetry Elements Reference](resources/telemetry-elements.md)
