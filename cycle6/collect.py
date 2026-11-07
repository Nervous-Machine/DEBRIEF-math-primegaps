#!/usr/bin/env python3
"""Collect cycle 6 (independent rerun of openai/PrimeGaps186) results from the logs copied out of the VM into
results_cycle6.json. Deterministic: rerun any time the logs change. Pre-registration: ../prereg_cycle6.yaml."""
import json, os, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda n: open(os.path.join(HERE, n), encoding="utf-8", errors="replace").read() if os.path.exists(os.path.join(HERE, n)) else ""
grab = lambda pat, s, d=None: (re.search(pat, s, re.M) or [None, d])[1] if re.search(pat, s, re.M) else d

out = {"cycle": 6, "dated": "2026-11-07", "registered": "prereg_cycle6.yaml (sha256 in prereg_cycle6.sha256; C8/C9 added by amendment A1 after C6, before they ran)",
       "source_commit": rd("source_commit.txt").strip(), "environment": rd("environment.txt").strip().splitlines(),
       "tools": {"landrun_commit": rd("landrun_commit.txt").strip(), "nanoda_commit": rd("nanoda_commit.txt").strip()}}

c4 = rd("C4.log")
out["C4"] = {"check": "lake exe cache get && lake build PrimeGaps186", "lean": grab(r"^Lean \(version ([^)]*)\)", c4), "lake": grab(r"^Lake version (\S+)", c4),
             "build_exit": int(grab(r"build_exit=(\d+)", c4, "-1")), "warning_lines": int(grab(r"warning_lines=(\d+)", c4, "-1")), "error_lines": int(grab(r"error_lines=(\d+)", c4, "-1")),
             "wall": grab(r"Elapsed \(wall clock\) time \([^)]*\): (\S+)", c4), "peak_rss_kb": int(grab(r"Maximum resident set size \(kbytes\): (\d+)", c4, "0"))}
out["C4"]["pass"] = out["C4"]["build_exit"] == 0 and out["C4"]["warning_lines"] == 0 and out["C4"]["error_lines"] == 0

c5, c5c, ax = rd("C5.log"), rd("C5.comparator.log"), rd("C5.axioms.txt")
axsets = [sorted(a.strip() for a in m.group(1).replace("\n", " ").split(",")) for m in re.finditer(r"depends on axioms: \[([^\]]*)\]", ax)]
SIX = sorted(["propext", "Classical.choice", "Quot.sound", "PrimeGap186.kloosterman3_bound", "PrimeGap186.kloosterman2_correlation_bound", "PrimeGap186.physical_integral_bounds"])
out["C5"] = {"check": "lake exe comparator comparator/main.json under systemd-run, then #print axioms", "comparator_exit": int(grab(r"comparator_exit=(\d+)", c5, "-1")),
             "comparator_ok": "Your solution is okay!" in c5c, "nanoda_accepts": "nanoda kernel accepts the solution" in c5c, "lean_kernel_accepts": "Lean default kernel accepts the solution" in c5c,
             "sandbox": "systemd-run --property=RestrictAddressFamilies=~AF_UNIX --user, landrun " + grab(r"landrun version (\S+)", c5, "?"),
             "lean4export": grab(r'"exporter":\{"name":"lean4export","version":"([^"]+)"', c5), "wall": grab(r"Service runtime: (.*)", c5c), "peak_mem": grab(r"Memory peak: (\S+)", c5c),
             "theorems_checked": 3, "axioms_per_theorem": axsets, "axioms_exactly_six": len(axsets) == 3 and all(a == SIX for a in axsets)}
out["C5"]["pass"] = out["C5"]["comparator_exit"] == 0 and out["C5"]["comparator_ok"] and out["C5"]["nanoda_accepts"] and out["C5"]["lean_kernel_accepts"] and out["C5"]["axioms_exactly_six"]

c6 = json.loads(rd("C6.json") or "{}")
out["C6"] = {"check": "stock python-flint 0.9.0 wheel: certificate regression check_flint_signed_fft()", **{k: c6.get(k) for k in ("python", "python_flint", "regression", "first_mismatch_index")},
             "bundled_flint": "3.6.0 (release 30600)", "pass": c6.get("regression") == "fail", "note": "pass here means the prediction held: the stock build fails the regression"}

c8b, c8 = rd("C8b.log"), json.loads(rd("C8.json") or "{}")
out["C8"] = {"check": "FLINT v3.6.0 + cherry-pick 7ad753d (PR 2790), python-flint 0.9.0 built from source against it; same regression",
             "flint_commit": grab(r"flint_commit=(\S+) Fix fft", c8b), "cherry_pick_exit": int(grab(r"cherry_pick_exit=(\d+)", c8b, "-1")), "flint_reports": grab(r"python-flint 0.9.0 FLINT (\S+)", c8b),
             "regression": c8.get("regression"), "pass": c8.get("regression") == "pass",
             "first_attempt_note": "a first attempt fell back to FLINT main (3.7.0-dev) because git had no committer identity for the cherry-pick; python-flint's version gate rejected 3.7.0-dev; that attempt is C8.log and is superseded"}

c9 = rd("C9.log")
rec = json.loads(rd("prime_gap_186_fresh.json") or "{}")
out["C9"] = {"check": "python3 -B prime_gap_186_certificate.py --workers 4 --output fresh.json on the C8 build (the script accepts only 1 or 4 workers; the prereg said 20)",
             "certificate_sha256": grab(r"^(\S+)  prime_gap_186_certificate.py", c9), "exit": int(grab(r"certificate_exit=(\d+)", c9, "-1")) if c9 else None,
             "receipt_passed": rec.get("passed"), "elapsed_seconds": rec.get("elapsed_seconds"), "wall": grab(r"Elapsed \(wall clock\) time \([^)]*\): (\S+)", c9), "peak_rss_kb": int(grab(r"Maximum resident set size \(kbytes\): (\d+)", c9, "0")) or None,
             "status": "running" if not os.path.exists(os.path.join(HERE, "C9.done")) else "done"}
out["C9"]["pass"] = out["C9"]["status"] == "done" and out["C9"]["exit"] == 0 and out["C9"]["receipt_passed"] is True
if rec:
    from fractions import Fraction as Fr
    fm, rq = Fr(str(rec.get("final_margin_lower", "0"))), Fr(str(rec.get("required_margin", "0")))
    out["C9"]["final_margin_lower"] = float(fm); out["C9"]["required_margin"] = float(rq); out["C9"]["margin_exceeds_required"] = fm > rq
    out["C9"]["margin_exceeds_1_over_50000"] = fm > Fr(1, 50000)  # the numerics paper states a normalized margin greater than 1/50000
    out["C9"]["component_count"] = rec.get("component_count")
    out["C9"]["receipt_sha256"] = hashlib.sha256(open(os.path.join(HERE, "prime_gap_186_fresh.json"), "rb").read()).hexdigest()
out["predictions_held"] = {k: out[k]["pass"] for k in ("C4", "C5", "C6", "C8")} | ({"C9": out["C9"]["pass"]} if out["C9"]["status"] == "done" else {})
json.dump(out, open(os.path.join(HERE, "results_cycle6.json"), "w"), indent=1)
print(json.dumps({k: (v if not isinstance(v, dict) else v.get("pass", v.get("status"))) for k, v in out.items() if k in ("C4", "C5", "C6", "C8", "C9", "predictions_held")}))
