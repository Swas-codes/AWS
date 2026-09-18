---
name: creating-skills
description: Creates high-quality Antigravity skills following standardized directory layouts, YAML frontmatter specifications, and progressive disclosure principles. Use when the user asks to build, generate, scaffold, or customize an Antigravity skill or agent workflow.
---

# Antigravity Skill Creator

Guides the creation of robust, predictable, and maintainable skills within `.agents/skills/` (workspace) or `~/.gemini/config/skills/` (global).

## When to use this skill
- User asks: "build me a skill for [task]"
- Scaffolding new agent automation behaviors or tool workflows
- Standardizing repetitive prompt patterns and checklists into reusable skills

## Workflow Checklist
Copy and update this checklist as you design and scaffold the skill:
- [ ] 1. Define skill intent & triggers (determine gerund name and trigger keywords)
- [ ] 2. Choose skill scope (workspace `.agents/skills/` vs global `~/.gemini/config/skills/`)
- [ ] 3. Create directory structure (`<skill-name>/SKILL.md`, `scripts/`, `examples/`, `resources/`)
- [ ] 4. Draft YAML frontmatter (`name` in gerund form <= 64 chars, 3rd-person `description` <= 1024 chars)
- [ ] 5. Write concise instructions adhering to the "Claude Way" (under 500 lines, progressive disclosure)
- [ ] 6. Validate skill layout and test invocation

## Core Standards

### Folder Structure
```
.agents/skills/<skill-name>/
├── SKILL.md                 # Required: Main instructions with YAML frontmatter
├── scripts/                 # Optional: Executable helper scripts
├── examples/                # Optional: Reference input/output implementations
└── resources/               # Optional: Schemas, templates, or assets
```

### YAML Frontmatter
```yaml
---
name: managing-databases
description: Manages schema migrations, backups, and query optimization for PostgreSQL databases. Use when the user asks to run database migrations, inspect tables, or optimize SQL performance.
---
```
- **name**: Lowercase gerund form (`verb-ing-object`), letters, numbers, and hyphens only.
- **description**: Third-person perspective with explicit triggering phrases.

### Degrees of Freedom
- **Bullet Points** (High freedom): Heuristics, code style principles, architecture guidelines.
- **Code Blocks** (Medium freedom): Config templates, boilerplate code snippets.
- **Bash Commands** (Low freedom): Exact terminal commands for deterministic operations.

## Output Format
When generating a skill, output:
1. Target directory path
2. `SKILL.md` contents inside a markdown code block
3. Any supporting scripts or template files
