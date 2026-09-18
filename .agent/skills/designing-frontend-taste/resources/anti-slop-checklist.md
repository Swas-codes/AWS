# Anti-Slop Pre-Flight Audit Checklist

Run through this checklist before outputting frontend code to guarantee agency-tier polish.

## Layout & Composition
- [ ] No generic 3-column identical card rows. Use variable widths (e.g., `8 col + 4 col` or staggered grid).
- [ ] Mobile collapse verified: all asymmetric grids fall back to clean vertical stacks (`grid-cols-1`) on `< 768px`.
- [ ] No full-viewport lockups with `h-screen`. Use `min-h-[100dvh]` to prevent mobile browser URL bar jitter.
- [ ] Meaningful whitespace: sections breathe with distinct hierarchy, not uniform repetitive padding.

## Typography
- [ ] No browser defaults or generic Inter-only styling. Characterful pairings are applied.
- [ ] Display headlines have tight letter-spacing (`-0.02em` to `-0.04em`) and compact line-heights (`1.1` to `1.2`).
- [ ] Paragraph text is constrained to readable widths (`max-w-xl` to `max-w-2xl` / ~65 characters per line).
- [ ] Numbers and metrics use tabular figures (`tabular-nums`) or monospace fonts.
- [ ] No orphaned single words on headline breaks (`text-wrap: balance`).

## Color & Surface Polish
- [ ] Background is not dead flat `#000000` or `#ffffff`. Uses rich off-black or warm substrate.
- [ ] Single primary accent color used with purpose; zero neon gradient slop.
- [ ] Borders use subtle opacity (`border-border/40` or `rgba(255,255,255,0.08)`).
- [ ] Drop shadows are tinted and diffuse, never harsh black boxes.

## Copywriting & Tone
- [ ] No generic AI buzzwords ("Unleash", "Elevate", "Next-Gen", "Seamless", "Supercharge").
- [ ] Realistic, authentic product content used instead of "Lorem Ipsum" or "John Doe".
- [ ] Concise, active voice copy.
