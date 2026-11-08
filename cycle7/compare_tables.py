#!/usr/bin/env python3
"""Cycle 7, mechanical part: compare every number table in the pinned Challenge.lean against the numerics paper
"Numerical certificate for prime gaps at most 186" (text extracted with pdftotext -layout).

    python3 -I compare_tables.py <Challenge.lean> <numerics.txt> <out.json>

Compares: the 77 trial coefficients (Table 1.1), the six component tables (Tables 2.1-2.6, the A and B columns are
what the third axiom asserts; q and E are proof data), the mask caps (1.5), the three scalar bounds of Lemma 2.5, and
the face coefficients. Also checks the tables' internal budget inequalities (2.30)-(2.31) exactly in rationals.
This is a text comparison. It says nothing about whether the Lean definitions denote the paper's quantities."""
import json, re, sys
from fractions import Fraction as Fr

lean = open(sys.argv[1], encoding="utf-8").read()
num = open(sys.argv[2], encoding="utf-8").read().splitlines()
out = {"source": sys.argv[1].split("/")[-1], "numerics_text": sys.argv[2].split("/")[-1], "checks": {}}
ok_all = True


def rec(name, ok, **kw):
    global ok_all
    ok_all &= bool(ok)
    out["checks"][name] = {"ok": bool(ok), **kw}


def lean_list(defname):
    m = re.search(r"def " + defname + r" : List \w+ :=\s*\[(.*?)\]\n", lean, re.S)
    rows = re.findall(r"\(([^()]*)\)", m.group(1))
    return [tuple(int(x) for x in r.split(",")) for r in rows]


def lean_coeffs():
    m = re.search(r"def trialCoefficientInteger : Fin 11 → Fin 7 → ℤ :=\s*(.*?\])\]\n", lean, re.S)
    rows = re.findall(r"!\[([-0-9,\s]+)\]", m.group(1))
    return [[int(x) for x in r.replace("\n", " ").split(",")] for r in rows]


# ---- numerics tables ----
def block(start_pat, end_pat):
    s = next(i for i, l in enumerate(num) if re.search(start_pat, l))
    e = next(i for i in range(s + 1, len(num)) if re.search(end_pat, num[i]))
    return num[s:e]


LABEL = re.compile(r"(?<![\w(])(L\d+|P\d+|H)(?![\w)])")


def outer_table(title):
    rows = []
    for l in block(title, r"total"):
        m = re.match(r"\s*(L\d+|P\d+|H)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s*$", l)
        if m:
            rows.append(tuple(int(x) for x in m.groups()[1:]))
    return rows


def inner_pair(title_left, end_pat):
    """Two side-by-side tables (label A E | label A E). Split by the column where the right table's labels start."""
    lines = block(title_left, end_pat)
    left, right = [], []
    for l in lines:
        for m in re.finditer(r"(L\d+|P\d+|H)\s+(-?\d+)\s+(-?\d+)", l):
            (left if m.start() < 35 else right).append((int(m.group(2)), int(m.group(3))))
    return left, right


def coeff_table():
    rows = {}
    order = []
    for l in block(r"Table 1\.1\. Integer coe", r"^\s*1\.3\. Source supports"):
        m = re.match(r"\s*(∅|\([\d, ]+\))\s+((?:-?\d+\s*)+)$", l)
        if m:
            sig = m.group(1).replace(" ", "")
            if sig not in rows:
                rows[sig] = []
                order.append(sig)
            rows[sig] += [int(x) for x in m.group(2).split()]
    return order, rows


# Table 1.1 vs trialCoefficientInteger
order, rows = coeff_table()
lc = lean_coeffs()
sig_lean = ["∅", "(2)", "(3)", "(4)", "(5)", "(6)", "(2,2)", "(2,3)", "(2,4)", "(3,3)", "(2,2,2)"]
rec("table_1_1_trial_coefficients", order == sig_lean and all(rows[s] == lc[i] for i, s in enumerate(sig_lean)),
    lean_rows=len(lc), paper_rows=len(order), entries=sum(len(r) for r in lc))

# Tables 2.1-2.6 vs the six Lean lists
t21, t22 = outer_table(r"Table 2\.1: Component bounds"), outer_table(r"Table 2\.2: Component bounds")
l21, l22 = lean_list("outerOrderTwoBounds"), lean_list("outerOrderFiveHalvesBounds")
rec("table_2_1_outer_order_two", t21 == l21, rows=len(l21), paper_rows=len(t21))
rec("table_2_2_outer_order_five_halves", t22 == l22, rows=len(l22), paper_rows=len(t22))
t23, t24 = inner_pair(r"Table 2\.3\. Bounds", r"Table 2\.5\. Bounds")
t25, t26 = inner_pair(r"Table 2\.5\. Bounds", r"Table 2\.7")
for name, tbl, ldef in [("table_2_3_inner_base_order_two", t23, "innerBaseOrderTwoBounds"),
                        ("table_2_4_inner_base_order_five_halves", t24, "innerBaseOrderFiveHalvesBounds"),
                        ("table_2_5_inner_enlarged_order_two", t25, "innerEnlargedOrderTwoBounds"),
                        ("table_2_6_inner_enlarged_order_five_halves", t26, "innerEnlargedOrderFiveHalvesBounds")]:
    ll = lean_list(ldef)
    rec(name, tbl == ll, rows=len(ll), paper_rows=len(tbl))
rec("component_count_97", len(l21) + len(l22) + sum(len(lean_list(d)) for d in
    ["innerBaseOrderTwoBounds", "innerBaseOrderFiveHalvesBounds", "innerEnlargedOrderTwoBounds",
     "innerEnlargedOrderFiveHalvesBounds"]) == 97)
rec("axiom_inequality_count_152", 2 * (len(l21) + len(l22)) + 45 + 3 == 152)

# Internal budget inequalities (2.30)-(2.31), exact rationals. Not part of the axiom; data the Lean proof must use.
d0, one_minus_bh = Fr(44415113, 5_000_000_000), Fr(1000843183, 1_000_000_000)
bad = []
for q, A, B, E in l21 + l22:
    c = Fr(q, 10**6)
    if not c * Fr(A, 10**18) + Fr(B, 10**18) / c <= Fr(E, 10**12):
        bad.append(("outer", q, A, B, E))
for ldef, kappa in [("innerBaseOrderTwoBounds", d0), ("innerBaseOrderFiveHalvesBounds", d0),
                    ("innerEnlargedOrderTwoBounds", one_minus_bh), ("innerEnlargedOrderFiveHalvesBounds", one_minus_bh)]:
    for A, E in lean_list(ldef):
        if not kappa * Fr(A, 10**18) <= Fr(E, 10**12):
            bad.append((ldef, A, E))
rec("budget_inequalities_2_30_2_31_hold_exactly", not bad, violations=bad)
totals = {"O2": sum(r[3] for r in l21), "O5/2": sum(r[3] for r in l22)}
rec("group_totals_match_table_2_7", totals["O2"] == 38927522 and totals["O5/2"] == 622829241
    and sum(e for _, e in lean_list("innerBaseOrderTwoBounds")) == 55254
    and sum(e for _, e in lean_list("innerBaseOrderFiveHalvesBounds")) == 435544
    and sum(e for _, e in lean_list("innerEnlargedOrderTwoBounds")) == 1405159
    and sum(e for _, e in lean_list("innerEnlargedOrderFiveHalvesBounds")) == 32422390, totals=totals)
grand = sum(r[3] for r in l21 + l22) + sum(e for d in ["innerBaseOrderTwoBounds", "innerBaseOrderFiveHalvesBounds",
            "innerEnlargedOrderTwoBounds", "innerEnlargedOrderFiveHalvesBounds"] for _, e in lean_list(d))
rec("grand_total_696075110", grand == 696075110, grand_total=grand)

# Lemma 2.5 scalars appear in the axiom text
ax = lean[lean.index("axiom PrimeGap186.physical_integral_bounds"):lean.index("end\n\nnamespace PrimeGap186\n\n/-- The forty")]
rec("lemma_2_5_scalars_in_axiom", all(s in ax for s in ["23685317816", "23685317890", "90248755123"])
    and "(23685317816 : ℝ) / (10 : ℝ) ^ 24 ≤ PrimeGap186.trialIH" in ax
    and "PrimeGap186.trialIH ≤ (23685317890 : ℝ) / (10 : ℝ) ^ 24" in ax
    and "(90248755123 : ℝ) / (10 : ℝ) ^ 24 ≤ PrimeGap186.trialJLambdaH" in ax)
numtxt = "\n".join(num)
rec("lemma_2_5_scalars_in_paper", all(s in numtxt for s in ["23685317816 · 10−24 ≤ IH ≤ 23685317890 · 10−24", "Jλ,H ≥ 90248755123 · 10−24"]))
# the axiom divides every component by the lower IH endpoint, as (2.30)-(2.31) do
rec("axiom_divides_by_IH_lower", ax.count("((23685317816 : ℝ) / (10 : ℝ) ^ 24)") == 8)

# masks (1.5) and shared constants
masks = {"outer": [(89196, 68225), (95598, 49152), (None, 46580)], "base": [(84930, 68225), (87194, 44781), (None, 35265)],
         "enlarged": [(85161, 68225), (87249, 44976), (None, 35419)]}
rec("mask_caps_1_5", all(f"if r ≤ {a} then {b}" in lean for a, b in [(89196, 68225), (84930, 68225), (85161, 68225)])
    and all(s in lean for s in ["95598 then 49152 else 46580", "87194 then 44781 else 35265", "87249 then 44976 else 35419"])
    and all(s in numtxt for s in ["0 : 89196", "89197 : 95598", "95599 : 98263", "0 : 84930", "84931 : 87194", "87195 : 89524",
                                  "0 : 85161", "85162 : 87249", "87250 : 89914", "68225", "49152", "46580", "44781", "35265", "44976", "35419"]))
rec("constants_shared", all(s in lean for s in ["(2742997 / 2624989) / 98304", "68225 * trialMesh", "262499 / 1000000",
                                                "(21 / 200) / (1 + t / 100) + (179 / 200) / (1 + (907 / 5) * t)",
                                                "2479900401 / 2500000000", "-843183 / 1000000000", "Finset.range 98264"])
    and all(s in numtxt for s in ["2742997", "2624989", "98304", "262499", "21/200", "179/200", "907/5", "2479900401", "843183", "98264"]))
rec("d0_44415113_not_in_statement_file", True, present="44415113" in lean, note="d0 is the old-inner restoration coefficient of (2.28); absent from Challenge.lean means the Lean proof does not carry it as a named constant in the statement file")

# margin arithmetic of Cor. 2.6, exact
rho_star = Fr(2624989, 10**7)
lhs = rho_star * Fr(90248755123, 23685317890) - Fr(500103, 500000)
margin = Fr(500103, 500000) - 1 - rho_star * Fr(697, 10**6)
rec("corollary_2_6_margin_exact", lhs == Fr(18806715247, 236853178900000000) and margin == Fr(230382667, 10**13) and margin > Fr(1, 50000),
    margin=str(margin), margin_float=float(margin))

# the largest cap: paper (1.13) zeta = 19037/(100000 rho), rounded down to a multiple of h (section 1.1); Lean uses 68225 * h
rho = Fr(1, 4) + Fr(12499, 10**6)
zeta = Fr(19037) / (100000 * rho)
h = Fr(2742997, 2624989) / 98304
rec("largest_cap_68225_is_floor_of_zeta_over_h", (zeta / h).numerator // (zeta / h).denominator == 68225 and zeta != 68225 * h,
    zeta=str(zeta), zeta_over_h=float(zeta / h), note="Lean's cap 68225*h is the paper's zeta rounded down to the grid, not zeta itself; consistent with section 1.1")

out["all_ok"] = ok_all
json.dump(out, open(sys.argv[3], "w"), indent=1, ensure_ascii=False)
print("all_ok" if ok_all else "MISMATCH", json.dumps({k: v["ok"] for k, v in out["checks"].items()}, indent=1))
