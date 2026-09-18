---
name: launchlens-discovery
description: Autonomous pre-launch customer discovery, forum prospect mining, intent scoring, and market validation for early-stage startups.
---

# LaunchLens Customer Discovery Skill for OpenClaw

This skill empowers OpenClaw agents to autonomously discover early adopters, extract acute customer pain points, verify evidence, synthesize audience segments, and deliver structured discovery reports to the LaunchLens platform.

## Agent Workflow

1. **Intake Product Specification**:
   - Product Name
   - Core Description
   - Target Customer Personas
   - Acute Problem / Pain Point

2. **Cross-Channel Prospect Mining**:
   - **Reddit**: Search subreddits `r/startups`, `r/SaaS`, `r/entrepreneur`, `r/technology`, niche developer communities.
   - **Hacker News**: Search Ask HN threads and comments mentioning workarounds, manual scripts, or tooling frustration.
   - **GitHub**: Search open issues, feature requests, and discussions on related open-source repositories.
   - **Twitter / X & Discord**: Scan public posts for users seeking alternatives or expressing intent to buy.

3. **Deterministic Signal Extraction**:
   For each discovered lead, extract the four core scoring signals:
   - `problem_fit` (0.0 to 1.0): How closely does the prospect's pain match the product's solution?
   - `intent_level` (0.0 to 1.0): Are they passively venting, or actively evaluating tools and willing to pay?
   - `persona_fit` (0.0 to 1.0): Does the author match the target customer demographic?
   - `evidence_strength` (0.0 to 1.0): Is there a direct, verified quote expressing this requirement?

4. **Audience Segmentation**:
   - Group discovered leads into 2-3 actionable customer segments with priority ratings (`high`, `medium`, `low`).
   - Extract raw **market language** (the exact phrases real prospects use to describe their pain).

5. **Delivery to LaunchLens**:
   Post the payload via HTTP POST to:
   `POST http://localhost:8001/api/research/callback`
   Headers:
   - `Authorization: Bearer <N8N_CALLBACK_SECRET>`
   - `Content-Type: application/json`
