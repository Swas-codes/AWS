# Telemetry Elements Reference

Visual motifs and ASCII framing patterns for industrial and telemetry interfaces.

## ASCII Framing Devices

### Corner Ticks & Anchors
```
+---------------------------------------+
| [SYS_INITIALIZE]                      |
|                                       |
|                                       |
+---------------------------------------+
```

### Coordinate Markers & Badges
- Section tags: `[SEC_01 // INGRESS]`, `// ARCH_LOG_v2`
- Timestamp tags: `[UTC: 2026.09.18_10:24:00]`
- Status pills: `[STATUS: NOMINAL]`, `[HALTED]`, `[DISPATCH_READY]`

## Typography Classes (Tailwind)
- **Macro Header**: `font-sans font-black uppercase tracking-tighter leading-none text-5xl md:text-8xl`
- **Telemetry Label**: `font-mono text-xs uppercase tracking-widest text-neutral-500`
- **Data Metric**: `font-mono font-bold text-3xl md:text-5xl tracking-tight text-neutral-100`
- **Sub-Metric**: `font-mono text-xs text-neutral-400`
