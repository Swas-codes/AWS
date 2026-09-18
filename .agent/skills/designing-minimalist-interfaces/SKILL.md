---
name: designing-minimalist-interfaces
description: Generates clean, editorial-grade minimalist web interfaces analogous to Linear, Notion, or high-end publications. Enforces warm monochrome palettes, bespoke typographic contrast, flat bento grids, and muted pastel accents without gradients or heavy drop shadows. Use when the user requests minimalist, clean, document-style, or editorial UI.
---

# Designing Minimalist Interfaces

An advanced frontend engineering directive for generating highly refined, ultra-minimalist, editorial web interfaces. Enforces a high-contrast warm monochrome palette, bespoke typography, macro-whitespace, bento grids, and flat component architecture with deliberate muted pastel accents.

## When to use this skill
- Building minimalist SaaS apps, productivity tools, and knowledge bases (Linear/Notion aesthetic)
- Designing editorial portfolios, digital essays, or document-style interfaces
- Triggered by keywords: "minimalist", "clean", "editorial", "Linear-style", "Notion-like", "monochrome UI", "warm paper"

## Workflow Checklist
- [ ] 1. **Apply Substrate**: Set canvas to warm bone (`#F7F6F3` / `#FBFBFA`) or off-black (`#111111`).
- [ ] 2. **Establish Type Hierarchy**: Pair Editorial Serif display with Geometric Sans body and Mono metadata.
- [ ] 3. **Grid Construction**: Lay out flat bento grid with thin hairlines (`border-black/5` or `#EAEAEA`).
- [ ] 4. **Shadow Elimination**: Remove heavy drop shadows (`shadow-none` or ultra-diffuse `< 0.04`).
- [ ] 5. **Spot Color Restriction**: Restrict color to desaturated washed-out pastels for tags and status badges.
- [ ] 6. **Cliché Elimination**: Strip generic marketing clichés and emojis from headings and UI copy.

## Absolute Banned Defaults
- ❌ **No Default Sans**: Banned `Inter`, `Roboto`, `Open Sans`. Use `Geist`, `Switzer`, or system `SF Pro`.
- ❌ **No Heavy Drop Shadows**: Banned `shadow-md`, `shadow-lg`. Shadows are flat or ultra-diffuse.
- ❌ **No Bright Backgrounds**: Banned solid saturated blue/green/purple hero sections.
- ❌ **No Neon/3D Gradients**: Zero glossy 3D mesh or neon fades.
- ❌ **No Pill Shape Containers**: Avoid `rounded-full` for cards and content blocks; use crisp radii (`rounded-lg` / `6px` to `8px`).
- ❌ **No Emojis in UI**: Replace emojis with clean inline SVG primitives or subtle badge text.
- ❌ **No AI Clichés**: Banned words: "Elevate", "Seamless", "Unleash", "Game-changer". Use plain, direct language.

## Typographic Hierarchy
- **Editorial Serif (Headings)**: `Instrument Serif`, `Newsreader`, `Playfair Display`. Apply tight tracking (`-0.03em`) and line-height (`1.15`).
- **Clean Sans-Serif (Body & UI)**: `Geist Sans`, `SF Pro Display`, `Switzer`. Generous line-height (`1.6`) in off-black (`#18181B` / `#2F3437`).
- **Monospace (Telemetry & Metadata)**: `Geist Mono`, `SF Mono`, `JetBrains Mono`. Upper-case, loose tracking (`tracking-wider`).

## Component Layout (Flat Bento Grid)
```tsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-px bg-neutral-200/80 p-px rounded-xl overflow-hidden">
  <div className="bg-white p-6 flex flex-col justify-between min-h-[220px]">
    <div className="flex items-center justify-between">
      <span className="text-xs font-mono text-neutral-500 uppercase tracking-wider">Metric 01</span>
      <span className="text-xs px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 font-medium">Active</span>
    </div>
    <div className="mt-8">
      <h4 className="font-serif text-2xl text-neutral-900 tracking-tight">Focused Execution</h4>
      <p className="text-xs text-neutral-600 mt-1 leading-relaxed">Deterministic outputs without superfluous UI noise.</p>
    </div>
  </div>
</div>
```

## Resources
- [Editorial Color Tokens](resources/editorial-palette.json)
