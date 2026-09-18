# agent.md — LaunchLens

**AI-powered potential customer discovery & pre-launch market intelligence agent**  
Built for: AWSxFirst Commit 2026

---

## 1. Problem Statement

Before launching a product, founders and product teams need to answer a critical question:

> **Who is most likely to need this product, where can we find them, and what evidence shows that they have the problem?**

Today, this research is usually fragmented across Reddit, LinkedIn, public communities, forums, review websites, social platforms, product directories, news articles, and niche online groups. Teams manually search for people discussing relevant problems, copy links into spreadsheets, read posts one by one, and try to decide which prospects are actually worth contacting.

This creates three major problems:

- **Discovery is slow** — potential customers are scattered across many communities and platforms.
- **Signal is noisy** — not everyone discussing a problem is a genuine potential customer.
- **Research becomes outdated quickly** — customer pain points, communities, competitors, and conversations change continuously.

The core failure is the same shape as many pre-launch workflows:

**The evidence that potential customers exist is already publicly available, but nobody is efficiently collecting, qualifying, and turning that evidence into an actionable customer list.**

---

## 2. Proposed Solution

**LaunchLens** is an AI-powered **Potential Customer Finder Agent** designed for any product before launch.

A founder provides a simple product description, target problem, or ideal customer profile. The agent then researches publicly available online signals and builds a structured list of potential customer segments and prospects.

LaunchLens can:

- Understand the product, its problem, target audience, and value proposition from a short description
- Discover online communities where people discuss the relevant problem
- Search for conversations, questions, complaints, feature requests, reviews, and discussions that indicate genuine pain
- Identify **potential customer profiles** based on problem relevance, intent, and contextual evidence
- Score leads using transparent criteria such as **problem fit, intent, relevance, and evidence strength**
- Extract the source conversation and explain **why the person or segment may be a potential customer**
- Cluster discovered prospects into useful customer segments
- Identify common pain points and recurring language customers use to describe the problem
- Generate suggested outreach angles based on the person's publicly expressed problem — without pretending that every discovered person is ready to buy
- Produce a pre-launch market intelligence report showing **where potential customers are, what they care about, and what signals support the opportunity**
- Allow the founder to change the product description or ICP and rerun the discovery process

The key workflow is:

**Product Idea → Problem Understanding → Web/Community Discovery → Signal Extraction → Lead Qualification → Customer Segmentation → Evidence-backed Insights → Outreach Suggestions**

This turns scattered public conversations into a continuously actionable **customer discovery pipeline**.

---

## 3. Core Agent Workflow

LaunchLens works as a multi-step research agent rather than a simple keyword search.

### Step 1 — Product Input

The founder provides:

```text
Product:
An AI-powered tool that automatically summarizes long technical documents.

Target users:
Software developers, engineering managers, and technical researchers.

Problem:
Developers spend too much time reading large technical documents and extracting important information.
```

The agent converts this into a structured research profile:

```json
{
  "product": "...",
  "problem": "...",
  "target_users": ["developers", "engineering managers", "technical researchers"],
  "pain_points": ["time spent reading", "information overload", "manual summarization"],
  "keywords": ["technical documentation", "developer productivity", "documentation overload"],
  "buying_signals": ["looking for tools", "asking for recommendations", "complaining about workflow"]
}
```

### Step 2 — Potential Customer Discovery

The agent searches public sources for people and communities where the problem is being discussed.

Possible sources include:

- Reddit
- Public forums
- Public Discord/community pages where accessible
- Product-review websites
- Public social posts
- Hacker News
- GitHub issues/discussions
- Public blogs and comments
- Product communities
- Industry-specific forums
- Public Q&A websites
- News and industry publications

The system should prioritize **publicly accessible information** and respect platform terms, rate limits, robots policies, and applicable privacy laws.

### Step 3 — Signal Extraction

Instead of treating every keyword match as a lead, the agent looks for meaningful signals:

| Signal | Example |
|---|---|
| Pain signal | "I spend hours reading documentation every week." |
| Intent signal | "Is there a tool that can automatically summarize this?" |
| Recommendation signal | "What tools do you use for this?" |
| Frustration signal | "Our current workflow is painfully slow." |
| Switching signal | "Looking for an alternative to our current tool." |
| Feature request | "I wish this product could automatically..." |
| Community signal | Repeated discussions around the same problem |

### Step 4 — Lead Qualification

Each potential customer receives an explainable score based on signals.

Example:

```text
Problem Fit       → 0.90
Intent             → 0.80
Target Persona     → 0.95
Evidence Strength  → 0.85
Overall Score      → 0.88
```

The score is not intended to claim that someone will purchase the product. It represents **how strongly the available public evidence matches the product's target problem and customer profile**.

### Step 5 — Customer Segmentation

The agent groups discovered prospects into segments such as:

```text
Segment A — Independent Developers
Main pain: documentation overload
Primary signal: asking for productivity tools

Segment B — Engineering Managers
Main pain: team knowledge sharing
Primary signal: discussing documentation and onboarding problems

Segment C — Technical Researchers
Main pain: processing large technical papers
Primary signal: looking for research summarization workflows
```

### Step 6 — Actionable Output

The founder receives:

- Potential customer list
- Customer segments
- Pain points
- Intent signals
- Evidence snippets
- Source links
- Relevance score
- Suggested outreach angle
- Community recommendations
- Market-language keywords
- Common objections or unmet needs

---

## 4. Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| Frontend | React + Tailwind CSS | Product input, lead dashboard, customer segments, evidence cards |
| Agent Orchestration | n8n | Coordinates research, APIs, filtering, enrichment, scoring, and report generation |
| AI Agent | OpenClaw + LLM API | Plans research, interprets evidence, qualifies prospects, summarizes findings |
| Search / Discovery | Search APIs / public APIs | Finds relevant conversations, communities, reviews, and public discussions |
| Data Extraction | JavaScript / Python | Normalizes discovered information into a common schema |
| Lead Scoring | TypeScript / Python rules | Transparent scoring based on fit, intent, relevance, and evidence |
| Backend | Node.js / FastAPI | API layer and research-job management |
| Data Store | PostgreSQL | Stores research runs, prospects, evidence, segments, and scores |
| Cache / Queue | Redis | Caching repeated searches and managing background jobs |
| Charts | Recharts | Segment distribution, signal strength, and discovery analytics |
| Hosting | AWS | Deploy frontend, backend, n8n, and OpenClaw |
| Automation | n8n | Multi-step workflows and scheduled research |
| Reporting | LLM-generated Markdown/JSON | Generates customer-discovery reports |

### Why n8n?

n8n acts as the workflow and integration layer:

```text
User Product Brief
       ↓
Research Profile Generator
       ↓
Search / Data Sources
       ↓
Normalize Results
       ↓
Remove Duplicates
       ↓
AI Signal Extraction
       ↓
Lead Scoring
       ↓
Segmentation
       ↓
Evidence Validation
       ↓
PostgreSQL
       ↓
Dashboard + Report
```

### Why OpenClaw?

OpenClaw acts as the autonomous research and reasoning layer.

Instead of simply sending one prompt to an LLM, the agent can:

1. Understand the product
2. Decide what information it needs
3. Generate search strategies
4. Investigate multiple sources
5. Compare discovered signals
6. Identify relevant customer segments
7. Re-evaluate weak or conflicting evidence
8. Produce a structured customer-discovery report

n8n handles **workflow orchestration and integrations**, while OpenClaw handles **agentic research and reasoning**.

---

## 5. Data Model

A potential customer record can follow this structure:

```json
{
  "id": "lead_001",
  "source": "reddit",
  "source_url": "...",
  "author": "public_username",
  "customer_segment": "Independent Developer",
  "problem_detected": "Documentation overload",
  "pain_signal": "Strong",
  "intent_signal": "Medium",
  "problem_fit": 0.91,
  "evidence_strength": 0.87,
  "overall_score": 0.88,
  "evidence": [
    "Public discussion indicating difficulty processing long documentation."
  ],
  "suggested_outreach_angle": "Ask about their current documentation workflow and whether summarization would reduce research time."
}
```

The system should store only information that is necessary for the intended workflow and should avoid collecting sensitive or unnecessary personal information.

---

## 6. Lead Scoring Engine

The initial prototype can use a transparent rules-based scoring model.

```text
problem_fit       = similarity between product problem and detected problem
intent_score      = strength of buying / solution-seeking signal
persona_fit       = match with target customer profile
evidence_strength = quality and specificity of supporting public evidence

lead_score =
    (0.35 * problem_fit)
  + (0.25 * intent_score)
  + (0.20 * persona_fit)
  + (0.20 * evidence_strength)
```

Example interpretation:

```text
0.80 – 1.00 → Strong potential match
0.60 – 0.79 → Relevant potential match
0.40 – 0.59 → Weak / requires validation
< 0.40       → Low relevance
```

These thresholds are prototype defaults and should be validated against real customer-discovery outcomes before being treated as a reliable predictive system.

### Important Principle

The score should answer:

> **"How strongly does the available evidence match this product's target problem?"**

It should **not** claim:

> "This person will buy."

The system is a customer-discovery assistant, not a guaranteed sales predictor.

---

## 7. AI Agent Output

The AI reasoning layer should return structured information.

Example:

```json
{
  "customer_segment": "Engineering Manager",
  "problem": "Difficulty keeping engineering documentation accessible",
  "pain_level": "high",
  "intent": "medium",
  "problem_fit": 0.89,
  "evidence_strength": 0.84,
  "reason": "The public discussion describes a recurring documentation problem that closely matches the product's stated use case.",
  "outreach_angle": "Ask how the team currently handles large technical documentation and what part of the workflow consumes the most time.",
  "recommended_next_step": "Validate the pain through a short discovery conversation."
}
```

The agent should clearly distinguish:

- **Observed evidence**
- **AI interpretation**
- **Inference**
- **Recommended next step**

This makes the system explainable and reduces unsupported conclusions.

---

## 8. n8n Workflow

A prototype workflow can be implemented as:

```text
[Webhook / Product Input]
          ↓
[Create Product Research Profile]
          ↓
[Generate Search Queries]
          ↓
[Search Multiple Public Sources]
          ↓
[Merge Results]
          ↓
[Deduplicate]
          ↓
[Extract Relevant Signals]
          ↓
[LLM Qualification]
          ↓
[Lead Scoring]
          ↓
[Customer Segmentation]
          ↓
[Evidence Validation]
          ↓
[Store in PostgreSQL]
          ↓
[Generate Report]
          ↓
[React Dashboard]
```

### Optional automated workflow

The founder can choose:

```text
Run once
Daily
Weekly
```

For recurring research, the workflow can search for **new conversations and newly emerging pain signals** rather than repeatedly returning the same results.

---

## 9. Dashboard

The frontend should provide four major views.

### A. Research Overview

```text
Product: AI Documentation Summarizer

Sources analyzed: 127
Relevant conversations: 42
Potential customer signals: 31
Customer segments: 5

Top detected problem:
Documentation overload

Top intent signal:
People actively asking for automation tools
```

### B. Potential Customer Explorer

Each lead card contains:

```text
Customer Segment
Problem
Signal Strength
Intent
Problem Fit
Evidence
Source
Suggested Next Step
```

The founder can filter by:

- Customer segment
- Source
- Intent
- Problem fit
- Score
- Pain point
- Date discovered

### C. Customer Segment View

Show:

```text
Segment
Number of signals
Most common pain
Most common intent
Relevant communities
Representative evidence
```

### D. Market Language View

This is especially useful before launch.

Show the actual vocabulary customers use:

```text
"documentation overload"
"too much context switching"
"manual research"
"takes hours to summarize"
"looking for an automated solution"
```

This can help founders improve:

- Landing-page copy
- Product positioning
- SEO keywords
- Feature priorities
- Outreach messaging

---

## 10. Datasets / Data Sources

### For the hackathon demo

Do not depend on a large proprietary customer database.

Use a controlled set of publicly accessible or synthetic examples:

- Public Reddit discussions
- Public Hacker News discussions
- GitHub issues/discussions
- Public product reviews
- Public forums
- Public blogs
- Synthetic conversations for demonstrating edge cases

A demo dataset can contain:

```text
100–300 public/synthetic conversation records
20–50 relevant signals
10–20 customer segments
```

### Production data sources

Depending on API availability and platform terms:

| Source | Potential Use |
|---|---|
| Reddit API | Public problem discussions and community discovery |
| GitHub API | Issues, discussions, feature requests |
| Hacker News / Algolia API | Startup and technology discussions |
| Product review platforms | Pain points and product complaints |
| Search APIs | Broad web discovery |
| Industry forums | Domain-specific customer problems |
| Public community pages | Customer segment discovery |

**Do not bypass authentication, access controls, paywalls, or platform restrictions.**

---

## 11. Deployment Architecture

```text
                         ┌──────────────────────┐
                         │      React UI        │
                         │   Tailwind Dashboard │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   FastAPI / Node.js  │
                         │     Backend API      │
                         └──────────┬───────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
             ┌───────────────┐             ┌───────────────┐
             │      n8n      │             │  PostgreSQL   │
             │ Orchestration │             │   Database    │
             └───────┬───────┘             └───────────────┘
                     │
                     ▼
             ┌───────────────┐
             │    OpenClaw   │
             │ Research Agent│
             └───────┬───────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   Search APIs   Public APIs   Web Sources
```

### AWS deployment

A production-oriented architecture can use:

- **EC2** — n8n + OpenClaw
- **RDS PostgreSQL** — persistent application data
- **ElastiCache Redis** — caching / queue support
- **S3** — reports and exported research results
- **CloudFront** — frontend delivery
- **Application Load Balancer** — API routing
- **Secrets Manager** — API credentials
- **CloudWatch** — logs and monitoring

For the hackathon, this can be simplified to:

```text
AWS EC2
 ├── n8n
 ├── OpenClaw
 └── Backend

Vercel
 └── React Frontend

Neon / PostgreSQL
 └── Application Data
```

---

## 12. Path to Production

### Phase 1 — Prototype

- Product description input
- Limited public data sources
- n8n workflow
- OpenClaw research agent
- Rules-based lead scoring
- React dashboard
- Synthetic/demo data where needed

### Phase 2 — Validation

- Add more data sources
- Validate relevance scoring against human-reviewed leads
- Improve duplicate detection
- Add customer-segment clustering
- Add evidence quality checks
- Track which research signals lead to meaningful customer conversations

### Phase 3 — Production

- Secure backend architecture
- OAuth/API integrations where appropriate
- Background research jobs
- Rate limiting
- Source-specific compliance controls
- Stronger relevance models
- Human review workflow
- Audit logs
- Workspace/team support
- CRM integrations
- Scheduled market monitoring

### Phase 4 — Continuous Customer Intelligence

The long-term product becomes more than a one-time lead finder:

```text
Product
   ↓
Continuous Market Research
   ↓
New Customer Problems
   ↓
New Potential Customers
   ↓
Emerging Segments
   ↓
Competitive Signals
   ↓
Product / Marketing Feedback
```

---

## 13. Demo Script Reference

### Demo Scenario

Imagine a founder is preparing to launch:

> **"An AI tool that summarizes technical documentation for developers."**

### Demo Flow

1. Enter the product description and target customer profile.
2. Launch the **Find Potential Customers** workflow.
3. n8n starts the research pipeline.
4. OpenClaw generates multiple research strategies.
5. Public conversations are collected from several sources.
6. Duplicate and irrelevant results are removed.
7. AI extracts pain and intent signals.
8. Each result receives an explainable relevance score.
9. Results are grouped into customer segments.
10. Dashboard displays the strongest evidence-backed opportunities.
11. Select one potential customer signal.
12. Show the original public discussion.
13. Show why LaunchLens classified it as relevant.
14. Show a suggested discovery/outreach angle.
15. Open the **Market Language** view.
16. Show the phrases customers repeatedly use.
17. Generate a final **Pre-Launch Customer Discovery Report**.

### Final Demo Message

Instead of saying:

> "We found 50 leads."

The product should demonstrate:

> **"We found where the problem is being discussed, identified the customer segments experiencing it, showed the evidence behind each signal, and turned that research into an actionable pre-launch customer discovery pipeline."**

---

## 14. Privacy, Ethics & Responsible Discovery

LaunchLens should be designed around **public information and customer research**, not surveillance.

### Principles

- Use publicly accessible information only.
- Respect platform terms, API policies, robots directives, and rate limits.
- Do not bypass authentication or access controls.
- Avoid collecting sensitive personal information.
- Minimize stored personal information.
- Store source URLs and evidence needed to explain a lead.
- Clearly distinguish observed facts from AI-generated inference.
- Do not claim that a person is definitely a buyer.
- Give users the ability to remove research results from their workspace.
- Use human review before automated outreach.
- Avoid spam or mass unsolicited messaging.

The product should optimize for **evidence-backed customer discovery**, not indiscriminate scraping.

---

## 15. Known Limitations

- Public conversations do not represent the entire market.
- A person discussing a problem may not be a potential buyer.
- Public usernames and discussions can provide incomplete context.
- Platform APIs and access policies vary.
- Search results can contain duplicates, noise, or outdated information.
- LLMs can incorrectly interpret ambiguous conversations.
- Relevance scores are heuristic unless validated against real outcomes.
- Customer discovery requires human validation and conversations.
- Automated outreach should not be treated as a substitute for genuine customer research.

---

## 16. Future Features

### Product Intelligence

- Competitor discovery
- Feature-gap detection
- Emerging problem detection
- Market trend monitoring
- Product positioning suggestions

### Customer Intelligence

- ICP discovery
- Customer segment clustering
- Pain-point ranking
- Buying-intent detection
- Community discovery
- Customer-language extraction

### Workflow Integrations

- CRM export
- Slack notifications
- Email reports
- Notion research reports
- Google Sheets export
- HubSpot / Salesforce integrations

### Agentic Research

The future version can continuously answer:

```text
What new customer problems appeared this week?

Which customer segments are becoming more active?

Which communities are discussing our problem?

What features are people repeatedly requesting?

Which customer signals are new?

What evidence changed since the previous research run?
```

---

## 17. One-Line Product Definition

**LaunchLens is an AI-powered pre-launch customer discovery agent that finds, qualifies, and explains potential customer signals from public online conversations so founders can validate who has the problem before they launch.**

---

## 18. Positioning

### Traditional Approach

```text
Founder
  ↓
Google searches
  ↓
Open 20 tabs
  ↓
Read posts manually
  ↓
Copy interesting links
  ↓
Create spreadsheet
  ↓
Guess who is relevant
  ↓
Write outreach manually
```

### LaunchLens

```text
Founder
  ↓
Describe Product + ICP
  ↓
LaunchLens
  ↓
Autonomous Research
  ↓
Signal Extraction
  ↓
Evidence Validation
  ↓
Lead Qualification
  ↓
Customer Segmentation
  ↓
Actionable Customer Discovery Report
```

### Core Value Proposition

> **Before you launch the product, LaunchLens helps you discover where your customers already are, what problems they are talking about, and which public signals are worth validating.**
