# Dr Derek Feedback — Plan & Progress

**Source:** Meeting with Dr Derek Soon (Neurology) + his elective medical student, reviewing the Clinical Reasoning App (Dx/ / Doctordle).
**Owners:** Atticus (build), Dr Natasha Luke (academic), Dr Derek Soon (clinical accuracy).
**Created:** 2026-07-09 · Branch: `m3-order-catalog`

This document tracks the response to Dr Derek's feedback. Status keys: ✅ done · 🔨 in progress · 📋 planned · 🧭 decision locked (not yet built) · 💬 discussion.

---

## Locked decisions (from Atticus, 2026-07-09)
1. **Merge investigations** → *merged-but-sectioned*: present one "Investigations" step, but keep Basic → Advanced grouped internally so the escalation teaching + scoring survive. (Track 3 — decided, build later.)
2. **AI integration** → *plan only, do not build yet*. See Track 4 for the full plan. (Track 4 — plan below.)
3. **Anatomical reorganisation** → *neurology only first*, then generalise. (Track 2 — decided, build later.)
4. **Sequencing now** → implement **Track 0** and **Track 1**. Tracks 2–4 are documented/decided but deferred.

---

## Strengths to preserve (do not regress)
- The **"Recommendation vs Yours"** and **"Full Analysis"** debrief panels were singled out by the elective students as the most useful learning tools. Every change below must keep these intact; where possible, lean into them (e.g. carry Track 2's anatomical reasoning into the debrief).
- The **M1/2 (guided) vs M3 (independent)** learning progression stays.
- Do not disturb the scoring maths (Approach / Process / Diagnosis weights, `biRel`/`aiPen`).

---

## Track 0 — Clinical accuracy with Dr Derek  🔨
**Priority: highest** ("this is information accuracy" — takes priority over features).

- 💬 **Book the recurring Friday review** at NUS (Dr Derek + Atticus). Human action — not code.
- ✅ **Per-case review sheet generator** (`case_review_sheet.py`): emits print-friendly Markdown into `review_sheets/` — every history/exam/investigation item with its finding + teaching note, MNMs, sig-negs, rule-outs, teaching points, criteria, and a clinician sign-off block with ☐ accurate / ☐ needs-change checkboxes per item. Run `python3 case_review_sheet.py [case_006]`. Surfaces the `pathway.validation` status too.
- 📋 **Review order:** neuro cases first (007 Parkinson's, 008 GBS, 009 GCA, 010 Graves, 011 MS), then the two GS cases (005 cholecystitis, 006 pancreatitis, both recently revised).
- Structural gate before each review remains `validate_cases.py`.

## Track 1 — Quick UX wins  ✅ (verified desktop + mobile, 2026-07-09)
Directly answers the student's friction. Low risk, no scoring changes.

1. ✅ **Scroll follows the latest action** — `doItem` sets `G._followTail`; after the workstation renders, the newest finding is scrolled into view (`block:'center'`) instead of snapping to the top. *(index.html doItem, renderWorkstation.)*
2. ✅ **Always-visible stage stepper** — `wsStepper()` renders `History ▸ Examination ▸ Investigations ▸ Diagnosis` in a dedicated `.ws-stepbar` between the fixed banner and the body (cannot be occluded by the differential drawer); active step ringed + animated; a `showStageToast()` "Now: <stage>" toast fires on every stage change. Investigations shown as one step (previews the Track 3 merge). *(index.html wsStepper/renderWorkstation/showStageToast, style.css .ws-stepbar/.ws-step/.stage-toast.)*
3. ✅ **Remove a diagnosis in the re-rank window** — a `✕` per row (`rRemove`) deletes from `G.diff`, keeps `phase1Names` honest, and re-renders. *(index.html buildRItems/rRemove.)*
4. ✅ **Search "did you mean" + broader synonyms** — no-exact-match now shows the closest candidates (`itemMatchScore`) rather than an empty list; SYN_GROUPS extended with lay↔medical vocabulary. Verified: "loose stool"→bowel-habit item, "throwing up"→vomiting item. *(index.html matchItem/itemMatchScore/renderPalBody/SYN_GROUPS.)*

**Verification:** driven in the Launch preview (desktop 1280 + mobile 375). Stepper states + toast + rank-remove + search all confirmed; zero console errors. `validate_cases.py` green; `style.css?v=20260709a`.

## Track 2 — Anatomical differential reasoning (M1/2, NEURO FIRST)  🧭
Reorganise the M1/2 differential list around the neuro scaffold: **Where** (localise) → **What** (pathology) → **When** (acute/subacute/chronic).
- **Data:** add `region`/localisation + `tempo` tags to neuro `DIAG_LIB` entries (cortex, basal ganglia, cerebellum, brainstem, cord, root, plexus, peripheral nerve, NMJ, muscle…).
- **UI:** in M1/2, `openDrawer()` groups by localisation first, pathology/tempo as sub-facets.
- Pilot in neurology, then generalise the "where→what→when" frame to other systems. **Decided: neuro only first.**

## Track 3 — Merge investigations (merged-but-sectioned)  🧭
Present a single "Investigations" step; keep Basic → Advanced grouping internally.
- Touches: stage hierarchy, `getStageItems`, scoring split (`biRel`/`aiPen`), the new stepper, debrief timeline.
- Keep the "escalate appropriately — don't jump to CT/ERCP" teaching and its scoring. **Decided: build after Track 0/1.**

## Track 4 — AI integration (PLAN ONLY — do not build yet)  📋
See full plan in the next section.

---

## AI Integration — Plan (for AICET / Dr Natasha discussion)

**Reframe the ask.** The shared article lists *consumer ChatGPT plugins*. That is not the right model for an embedded medical teaching app (no key security, no control over output, no data governance). What fits is a **small, controlled Claude API integration** behind our own backend — pick **one** pilot feature, not "add a plugin."

### Candidate features
- **(A) Socratic tutor / hint button** *(recommended pilot)* — at each stage the model gives a probing hint ("what dangerous cause should you exclude before imaging?") **without revealing the answer**. Best fit for clinical reasoning; lowest trust burden.
- **(B) Free-text differential grader** — the model judges the student's typed diagnosis + justification against the case rubric. Bonus: softens the "search too strict" problem. Higher trust burden (grading must be defensible).
- **(C) End-of-case debrief coach** — conversational Q&A about the completed case, grounded in the case's teaching content.

### Why a backend is required
The app is static (GitHub Pages) and **cannot hold an API key**. AI needs the serverless step from the existing 3-phase backend roadmap:
- **Frontend (static)** → **serverless proxy** (Cloudflare Worker / Netlify Function / Supabase Edge Function) holding `ANTHROPIC_API_KEY` → **Anthropic API**.
- Model: **Claude Haiku** for hints (cheap, fast); escalate only if quality needs it.
- Controls: rate-limiting per session; **no PII** (cases are synthetic); PDPA-clean; prompt template version-controlled and **clinician-reviewed**; output labelled "study aid, not authoritative."

### Data flow (feature A, the pilot)
1. Send: de-identified case context + current stage + the student's current differential list.
2. Model returns: one Socratic hint, capped tokens, guard-railed by a system prompt that forbids naming the final diagnosis.
3. Log the prompt/response for later review; show behind a feature flag on **one neuro case** first.

### Guardrails & governance
- System prompt constrains strictly to hints; **never** reveals the final Dx.
- Every prompt template reviewed by a clinician (Dr Derek/Dr Natasha) before it ships.
- Model output can be wrong — always labelled as a learning aid.
- Key management + cost ownership decided with AICET / Dr Natasha.

### Rough cost
Haiku-class model, short hint prompts → pennies per student session. Negligible for a pilot; model a per-student cap.

### Rollout
Prototype (flag, one case) → student pilot → evaluate → expand features/cases. Ties into backend **Phase 1 (BaaS)** — the same serverless layer that later carries accounts/leaderboard.

---

## Progress log
- **2026-07-09** — Plan created from Dr Derek's feedback; decisions locked (merged-but-sectioned investigations; AI plan-only; neuro-first anatomical reorg; do Track 0+1 now). Prior same-day work: revised GS pancreatitis (case_006) + corrected biliary-colic teaching (case_005), committed `8e31468`.
- **2026-07-09** — **Track 1 shipped + browser-verified** (scroll-follow, always-visible stage stepper + toast, remove-in-rank-modal, search "did you mean" + lay-synonym lexicon). **Track 0** review-sheet generator (`case_review_sheet.py`) added. Tracks 2–4 remain deferred per sequencing.

## Open items / needs input
- Confirm Friday slot with Dr Derek at NUS.
- After Track 0/1 land: schedule Track 2 (neuro anatomical reorg) design session with Dr Derek.
- AICET / Dr Natasha: AI pilot feature confirmation (recommend A), key + cost ownership.
