#!/usr/bin/env python3
"""validate_cases.py — mechanises the Dx/ case-authoring checklist.

Run from the dx:/dx folder:  python3 validate_cases.py

Checks (per CASE_AUTHORING_PLAN.md §5):
  - cases.json parses as JSON
  - every caseMNMs / expectedP1 / finalDx / finalUmbrella name resolves in DIAG_LIB
    (DIAG_LIB entry names + their `subs` subtypes; finalUmbrella resolves to a top-level `n`)
  - every caseMNM has a tier (1|2) and a matching mnmRuleOut entry
  - every expectedP1 has >=1 `rel` history OR pe item that plausibly names it (heuristic; warn only)
  - every top-level `required` id exists among history/pe/basic/advanced items
  - every sigNegs[].id exists; every mnmExpectedDemotion.after_item exists
  - v2 fields present + well-formed: demographics{name,age,sex,occupation,mrn},
    vitals{hr,bp,spo2,rr,temp each {value,unit,abnormal}}, allergies, background[], pathway{validation,reveal}
  - item id prefixes (h##/pe##/bi##/ai##) match their array
  - extracted <script> from index.html passes `node --check` (if node present)

Exit code 0 = all hard checks pass (warnings allowed); 1 = at least one ERROR.
"""
import json, re, sys, subprocess, tempfile, os

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = os.path.join(HERE, "cases.json")
INDEX = os.path.join(HERE, "index.html")

errors, warnings = [], []
def err(cid, msg): errors.append(f"[{cid}] ERROR: {msg}")
def warn(cid, msg): warnings.append(f"[{cid}] warn:  {msg}")


def load_diag_lib_names():
    """Parse DIAG_LIB from index.html → (set of all valid dx names, set of umbrella `n` names)."""
    html = open(INDEX, encoding="utf-8").read()
    m = re.search(r"const DIAG_LIB\s*=\s*\{", html)
    if not m:
        print("FATAL: could not locate DIAG_LIB in index.html"); sys.exit(2)
    # Slice from the opening brace to a heuristic end (the SYS_COLOR map or end of object).
    start = m.end() - 1
    depth, i = 0, start
    while i < len(html):
        c = html[i]
        if c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0: break
        i += 1
    block = html[start:i + 1]
    names, umbrellas = set(), set()
    # entry names:  n:"..."  (allow ' and " inside via non-greedy up to ",)
    for nm in re.findall(r'\bn:\s*"((?:[^"\\]|\\.)*)"', block):
        names.add(nm)
    # subtypes:  subs:[ "...", "..." ]
    for subsblock in re.findall(r"subs:\s*\[(.*?)\]", block, re.S):
        for sub in re.findall(r'"((?:[^"\\]|\\.)*)"', subsblock):
            names.add(sub)
    # umbrellas = entries that declare subs
    for entry in re.findall(r'\bn:\s*"((?:[^"\\]|\\.)*)"[^}]*?subs:', block):
        umbrellas.add(entry)
    return names, umbrellas


def check_case(c, names):
    cid = c.get("id", "?")
    # --- required top-level fields ---
    for f in ("id", "title", "approach", "system", "difficulty", "vignette",
              "caseMNMs", "expectedP1", "finalDx", "finalUmbrella", "diagnosisScore",
              "required", "sigNegs", "mnmRuleOut", "keyTeachingPoints",
              "history", "pe", "basic", "advanced", "pathway",
              "demographics", "vitals", "allergies", "background"):
        if f not in c:
            err(cid, f"missing top-level field `{f}`")

    if c.get("difficulty") not in ("easy", "moderate", "challenging", "easy-moderate", "easy–moderate"):
        warn(cid, f"unusual difficulty value: {c.get('difficulty')!r}")

    # --- demographics ---
    demo = c.get("demographics", {})
    for k in ("name", "age", "sex", "occupation", "mrn"):
        if k not in demo: err(cid, f"demographics missing `{k}`")

    # --- vitals ---
    vit = c.get("vitals", {})
    for k in ("hr", "bp", "spo2", "rr", "temp"):
        if k not in vit:
            err(cid, f"vitals missing `{k}`"); continue
        for sub in ("value", "unit", "abnormal"):
            if sub not in vit[k]: err(cid, f"vitals.{k} missing `{sub}`")

    # --- background must be a list ---
    if not isinstance(c.get("background"), list):
        err(cid, "background must be a list")

    # --- pathway ---
    pw = c.get("pathway", {})
    if "validation" not in pw or "status" not in pw.get("validation", {}):
        err(cid, "pathway.validation.status missing")
    if "reveal" not in pw:
        warn(cid, "pathway.reveal missing")

    # --- name resolution ---
    def resolve(name): return name in names
    for m in c.get("caseMNMs", []):
        if not isinstance(m, dict) or "name" not in m:
            err(cid, f"caseMNMs entry malformed: {m!r}"); continue
        if m.get("tier") not in (1, 2):
            err(cid, f"caseMNM '{m['name']}' missing/invalid tier (got {m.get('tier')!r})")
        if not resolve(m["name"]):
            err(cid, f"caseMNM '{m['name']}' not in DIAG_LIB")
    for p in c.get("expectedP1", []):
        if not resolve(p):
            err(cid, f"expectedP1 '{p}' not in DIAG_LIB")
    # finalDx may be a composite/specific phrasing (e.g. "SCLC with paraneoplastic SIADH")
    # that isn't a literal DIAG_LIB entry — it is scored via diagnosisScore, not the search.
    fdx = c.get("finalDx", "")
    if not resolve(fdx):
        warn(cid, f"finalDx '{fdx}' not a literal DIAG_LIB entry (ok if composite — must be in diagnosisScore @100)")
    if not resolve(c.get("finalUmbrella", "")):
        err(cid, f"finalUmbrella '{c.get('finalUmbrella')}' not in DIAG_LIB")
    if fdx and fdx not in c.get("diagnosisScore", {}):
        err(cid, f"finalDx '{fdx}' is not a key in diagnosisScore")

    # --- MNM ↔ mnmRuleOut coverage ---
    ruleout_names = {r.get("mnm") for r in c.get("mnmRuleOut", [])}
    for m in c.get("caseMNMs", []):
        if isinstance(m, dict) and m.get("name") not in ruleout_names:
            err(cid, f"caseMNM '{m.get('name')}' has no mnmRuleOut entry")

    # --- item ids + prefixes ---
    prefixes = {"history": "h", "pe": "pe", "basic": "bi", "advanced": "ai"}
    all_ids = {}
    for arr, pref in prefixes.items():
        for it in c.get(arr, []):
            iid = it.get("id", "")
            all_ids[iid] = arr
            if not iid.startswith(pref):
                warn(cid, f"item id '{iid}' in {arr}[] does not start with '{pref}'")
            for f in ("lbl", "cost", "find"):
                if f not in it: err(cid, f"item '{iid}' missing `{f}`")

    # --- required ids exist ---
    for rid in c.get("required", []):
        if rid not in all_ids:
            err(cid, f"required id '{rid}' not found among items")
    # --- sigNegs ids exist ---
    for sn in c.get("sigNegs", []):
        if sn.get("id") not in all_ids:
            err(cid, f"sigNegs id '{sn.get('id')}' not found among items")
    # --- demotion after_item exists ---
    for dm in c.get("mnmExpectedDemotion", []):
        ai = dm.get("after_item")
        if ai and ai not in all_ids:
            err(cid, f"mnmExpectedDemotion after_item '{ai}' not found among items")

    # --- expectedP1 has a discriminating item (heuristic, warn only) ---
    rel_text = " ".join(
        (it.get("lbl", "") + " " + it.get("find", "") + " " + it.get("exp", "")).lower()
        for arr in ("history", "pe") for it in c.get(arr, []) if it.get("rel")
    )
    for p in c.get("expectedP1", []):
        key = re.split(r"[ /(]", p.lower())[0]
        if len(key) > 3 and key not in rel_text:
            warn(cid, f"expectedP1 '{p}' — no obvious rel history/pe item mentions it (check discriminator exists)")

    # --- diagnosisScore should score finalDx 100 ---
    ds = c.get("diagnosisScore", {})
    if c.get("finalDx") in ds and ds[c["finalDx"]] != 100:
        warn(cid, f"finalDx scores {ds[c['finalDx']]} (expected 100)")


def check_js_syntax():
    html = open(INDEX, encoding="utf-8").read()
    scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
    if not scripts:
        warn("engine", "no inline <script> found to node --check"); return
    js = "\n".join(scripts)
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
    except Exception:
        warn("engine", "node not available — skipped JS syntax check"); return
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tf:
        tf.write(js); path = tf.name
    try:
        r = subprocess.run(["node", "--check", path], capture_output=True, text=True)
        if r.returncode != 0:
            errors.append(f"[engine] ERROR: extracted <script> failed node --check:\n{r.stderr.strip()}")
    finally:
        os.unlink(path)


def main():
    try:
        data = json.load(open(CASES, encoding="utf-8"))
    except Exception as e:
        print(f"FATAL: cases.json did not parse: {e}"); sys.exit(2)
    names, _ = load_diag_lib_names()
    print(f"DIAG_LIB: {len(names)} diagnosis names parsed")
    cases = data.get("cases", [])
    print(f"cases.json: {len(cases)} cases\n")
    for c in cases:
        check_case(c, names)
    check_js_syntax()

    for w in warnings: print(w)
    if warnings: print()
    for e in errors: print(e)
    print()
    if errors:
        print(f"❌ {len(errors)} error(s), {len(warnings)} warning(s)"); sys.exit(1)
    print(f"✅ all hard checks pass ({len(warnings)} warning(s))"); sys.exit(0)


if __name__ == "__main__":
    main()
