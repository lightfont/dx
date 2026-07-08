#!/usr/bin/env python3
"""Generate print-friendly clinical-review sheets from cases.json.

Track 0 (Dr Derek accuracy reviews): emits one Markdown sheet per case into
review_sheets/, laying out every history/examination/investigation item with its
finding and teaching note, plus MNMs, significant negatives, rule-outs, teaching
points and criteria — with a sign-off block for the clinician to mark up.

Usage:
    python3 case_review_sheet.py                # all cases
    python3 case_review_sheet.py case_006       # one case (id or index)
"""
import json, os, sys, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "review_sheets")

STAGES = [("history", "History"), ("pe", "Examination"),
          ("basic", "Basic investigations"), ("advanced", "Advanced investigations")]


def esc(s):
    return str(s or "").replace("\n", " ").strip()


def sheet(c):
    L = []
    w = L.append
    val = (c.get("pathway", {}).get("validation", {}) or {})
    status = val.get("status", "draft")
    w(f"# Case review — {c.get('title','?')}  ·  `{c.get('id','')}`")
    w("")
    w(f"- **Patient:** {esc(c.get('patient'))}")
    w(f"- **System / discipline:** {esc(c.get('system'))}"
      + (f" · {esc(c.get('discipline'))}" if c.get("discipline") else ""))
    w(f"- **Difficulty:** {esc(c.get('difficulty'))}")
    w(f"- **Final diagnosis:** {esc(c.get('finalDx'))}"
      + (f"  (umbrella: {esc(c.get('finalUmbrella'))})" if c.get("finalUmbrella") and c.get("finalUmbrella") != c.get("finalDx") else ""))
    w(f"- **Validation status:** `{status}`"
      + (f" — {esc(val.get('validatedBy'))}" if val.get("validatedBy") else " — not yet clinician-signed-off"))
    if val.get("notes"):
        w(f"- **Validation notes:** {esc(val.get('notes'))}")
    w("")

    v = c.get("vitals", {}) or {}
    vit = " · ".join(f"{k.upper()} {vv.get('value')}{vv.get('unit','')}"
                     for k, vv in v.items() if isinstance(vv, dict) and vv.get("value"))
    if vit:
        w(f"**Vitals:** {vit}  \n**Allergies:** {esc(c.get('allergies'))}")
    if c.get("background"):
        w("**Background:** " + "; ".join(esc(b) for b in c["background"]))
    w("")
    w("## Vignette")
    w("> " + esc(c.get("vignette")))
    w("")

    mnms = c.get("caseMNMs", [])
    if mnms:
        w("## Must-not-miss differentials")
        for m in mnms:
            nm = m.get("name") if isinstance(m, dict) else m
            tier = f" (Tier {m.get('tier')})" if isinstance(m, dict) and m.get("tier") else ""
            w(f"- {esc(nm)}{tier}")
        w("")
    if c.get("expectedP1"):
        w("## Common differentials expected (Phase 1)")
        w(", ".join(esc(x) for x in c["expectedP1"]))
        w("")

    for key, label in STAGES:
        items = c.get(key, [])
        if not items:
            continue
        w(f"## {label}")
        w("")
        for it in items:
            flags = []
            if it.get("required"): flags.append("REQUIRED")
            if it.get("rel"): flags.append("relevant")
            else: flags.append("not-relevant")
            if it.get("sigNeg"): flags.append("sig-neg")
            if it.get("penalize"): flags.append("penalised")
            w(f"### {esc(it.get('lbl'))}  ·  `{it.get('id','')}`  ·  cost: {esc(it.get('cost'))}  ·  {', '.join(flags)}")
            w(f"- **Finding:** {esc(it.get('find'))}")
            if it.get("exp"):
                w(f"- **Teaching note:** {esc(it.get('exp'))}")
            if it.get("lookingFor"):
                w(f"- **Looking for:** {esc(it.get('lookingFor'))}")
            w("")
            w("  _Clinician: ☐ accurate  ☐ needs change → _______________________________________________")
            w("")

    if c.get("sigNegs"):
        w("## Significant negatives (scored)")
        for s in c["sigNegs"]:
            w(f"- ({s.get('pts','?')} pts) {esc(s.get('label'))}")
        w("")

    if c.get("mnmRuleOut"):
        w("## Must-not-miss rule-out reasoning")
        for m in c["mnmRuleOut"]:
            w(f"**{esc(m.get('mnm'))}** — {esc(m.get('statusLbl') or m.get('status'))}")
            for f in m.get("findings", []):
                w(f"  - _{esc(f.get('type'))}_: {esc(f.get('text'))}")
            w("")

    if c.get("keyTeachingPoints"):
        w("## Key teaching points")
        for i, t in enumerate(c["keyTeachingPoints"], 1):
            w(f"{i}. {esc(t)}")
            w("   _Clinician: ☐ accurate  ☐ needs change_")
        w("")

    for fld, title in [("approachText", "Approach"), ("approachInsight", "Approach insight"),
                       ("expertNarrative", "Expert narrative"),
                       ("sensitivityNote", "Sensitivity note"), ("specificityNote", "Specificity note")]:
        if c.get(fld):
            w(f"## {title}")
            w(esc(c[fld]))
            w("")

    w("---")
    w("## Clinician sign-off")
    w("- Reviewer: __________________________   Date: ____________")
    w("- Overall: ☐ Approved   ☐ Approved with changes   ☐ Needs re-work")
    w("- Summary of required changes:")
    w("")
    w("  _________________________________________________________________")
    w("")
    return "\n".join(L)


def main():
    data = json.load(open(os.path.join(ROOT, "cases.json")))
    cases = data.get("cases", data if isinstance(data, list) else [])
    sel = sys.argv[1] if len(sys.argv) > 1 else None
    if sel is not None:
        if sel.isdigit():
            cases = [cases[int(sel)]]
        else:
            cases = [c for c in cases if c.get("id") == sel]
        if not cases:
            print(f"No case matched '{sel}'"); return
    os.makedirs(OUT, exist_ok=True)
    stamp = datetime.date.today().isoformat()
    for c in cases:
        fn = os.path.join(OUT, f"{c.get('id','case')}_{stamp}.md")
        open(fn, "w").write(sheet(c))
        print(f"wrote {os.path.relpath(fn, ROOT)}")


if __name__ == "__main__":
    main()
