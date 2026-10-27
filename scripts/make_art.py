# Generates the site illustrations. Usage: python scripts/make_art.py assets
import math, random, sys, os

OUT = sys.argv[1]
BG = "#111418"; PANEL = "#171b21"; LINE = "#2a3038"; LINE2 = "#3a424d"
MUTED = "#8b929c"; TEXT = "#e7e4dd"; RED = "#e5584e"; RED_D = "#b3261e"
DASH = ' stroke-dasharray="6 6"'
MONO = "JetBrains Mono, Consolas, 'Courier New', monospace"
SERIF = "Gambetta, Georgia, serif"

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")

# ---------- icons (centered at 0,0, ~22px box, stroke-only) ----------
ICONS = {
 "hospital": '<path d="M-3 -9h6v6h6v6h-6v6h-6v-6h-6v-6h6z"/>',
 "university": '<path d="M-11 -3 0 -9 11 -3 0 3z"/><path d="M-6 0v6c3 3 9 3 12 0V0"/><path d="M11 -3v8"/>',
 "cityhall": '<path d="M-11 -4 0 -10 11 -4z"/><path d="M-8 -1v8M-3 -1v8M3 -1v8M8 -1v8M-11 9h22"/>',
 "crisis": '<path d="M-10 -8h20v13h-9l-6 5v-5h-5z"/><path d="M0 2c-4-3-5-5-3-7 1-1 3-1 3 1 0-2 2-2 3-1 2 2 1 4-3 7z"/>',
 "eoc": '<path d="M-10 9 0 -9 10 9z"/><path d="M0 -2v5M0 6v.5"/>',
 "power": '<path d="M2 -10-6 2h5l-2 9 8-12h-5z"/>',
 "startup": '<path d="M-9 8V2M-3 8V-2M3 8V-5M9 8V-9"/>',
 "board": '<rect x="-8" y="-4" width="16" height="8" rx="4"/><circle cx="-5" cy="-8" r="1.4"/><circle cx="0" cy="-8" r="1.4"/><circle cx="5" cy="-8" r="1.4"/><circle cx="-5" cy="8" r="1.4"/><circle cx="0" cy="8" r="1.4"/><circle cx="5" cy="8" r="1.4"/>',
 "shield": '<path d="M0 -10 9 -6v5c0 6-4 9-9 11-5-2-9-5-9-11v-5z"/>',
 "water": '<path d="M0 -10C-4 -3-7 1-7 4a7 7 0 0 0 14 0c0-3-3-7-7-14z"/>',
 "community": '<circle cx="-5" cy="-4" r="3"/><circle cx="5" cy="-4" r="3"/><path d="M-11 8c0-5 3-7 6-7s6 2 6 7M-1 8c0-5 3-7 6-7s6 2 6 7"/>',
 "eye": '<path d="M-11 0C-7 -7 7 -7 11 0 7 7 -7 7 -11 0z"/><circle r="3"/>',
 "gauge": '<path d="M-10 5a10 10 0 0 1 20 0"/><path d="M0 5 6 -3"/><path d="M-10 8h20"/>',
 "dissent": '<path d="M-8 -3h16M-8 3h16M5 -10-5 10"/>',
 "doc": '<path d="M-7 -10h10l5 5v15h-15z"/><path d="M-3 -3h7M-3 1h7M-3 5h5"/>',
}

def node(x, y, icon, label, state="ok", r=24, label_dy=44, fs=13):
    stroke = RED if state in ("fail", "hit") else "#6b7380"
    fill = "#2a1513" if state == "fail" else PANEL
    ic = RED if state in ("fail", "hit") else "#c9c6bf"
    s = []
    if state == "fail":
        for k, op in ((2.4, .10), (1.8, .18), (1.35, .3)):
            s.append(f'<circle cx="{x}" cy="{y}" r="{r*k:.1f}" fill="none" stroke="{RED}" stroke-opacity="{op}" stroke-width="1.5"/>')
    s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
    s.append(f'<g transform="translate({x} {y}) scale({r/24:.2f})" fill="none" stroke="{ic}" stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round">{ICONS[icon]}</g>')
    if label:
        col = RED if state in ("fail", "hit") else MUTED
        s.append(f'<text x="{x}" y="{y+label_dy}" text-anchor="middle" font-family="{MONO}" font-size="{fs}" letter-spacing="1.5" fill="{col}" stroke="{BG}" stroke-width="6" stroke-linejoin="round" paint-order="stroke">{esc(label.upper())}</text>')
    return "\n".join(s)

def contour_blob(cx, cy, r, seed, n=90):
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.28) for _ in range(4)]
    amp = [rnd.uniform(.05, .14), rnd.uniform(.03, .09), rnd.uniform(.02, .06), rnd.uniform(.01, .04)]
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        k = 1 + sum(a * math.sin((j + 2) * t + p) for j, (a, p) in enumerate(zip(amp, ph)))
        pts.append((cx + r * k * math.cos(t) * 1.35, cy + r * k * math.sin(t)))
    d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts) + "Z"
    return d

def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
            f'<defs><radialGradient id="vg" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#1a1f26"/><stop offset="1" stop-color="{BG}"/></radialGradient>'
            f'<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity=".025"/></pattern></defs>\n'
            f'<rect width="{w}" height="{h}" fill="url(#vg)"/><rect width="{w}" height="{h}" fill="url(#grid)"/>\n{body}\n</svg>\n')

def edge(a, b, red=False, dash=False, curve=0):
    (x1, y1), (x2, y2) = a, b
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    cx, cy = mx - dy / L * curve, my + dx / L * curve
    col = RED if red else LINE2
    w = 2 if red else 1.3
    da = ' stroke-dasharray="6 6"' if dash else ""
    op = "1" if red else ".9"
    return f'<path d="M{x1} {y1} Q{cx:.1f} {cy:.1f} {x2} {y2}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{w}"{da}/>'

# ================= HERO: community systems map (2100x900, keep core in middle 1600) =================
def hero():
    W, H = 2100, 900
    b = []
    # contours
    for (cx, cy, rmax, seed) in [(420, 230, 260, 1), (1650, 680, 300, 2), (1180, 160, 170, 3), (300, 760, 200, 4), (1900, 220, 220, 5)]:
        for i in range(1, 10):
            b.append(f'<path d="{contour_blob(cx, cy, rmax * i / 9, seed)}" fill="none" stroke="{LINE}" stroke-width="1"/>')
    # river
    b.append(f'<path d="M-20 560 C 300 520, 520 640, 820 600 S 1300 470, 1560 520 S 1900 640, 2120 600" fill="none" stroke="#18242c" stroke-width="34" stroke-linecap="round"/>')
    b.append(f'<path d="M-20 560 C 300 520, 520 640, 820 600 S 1300 470, 1560 520 S 1900 640, 2120 600" fill="none" stroke="#24343f" stroke-width="1.2"/>')
    # roads
    for d in ["M180 0 L 640 900", "M0 330 L 2100 380", "M1450 0 L 1250 900", "M900 0 L 960 900", "M0 820 L 2100 760"]:
        b.append(f'<path d="{d}" stroke="#20252c" stroke-width="5" fill="none"/>')
    N = {
        "power": (1010, 450), "hospital": (700, 300), "crisis": (640, 560), "cityhall": (1010, 230),
        "eoc": (1290, 330), "university": (1340, 640), "water": (850, 720), "startup": (1560, 240),
        "board": (1650, 470), "base": (450, 420), "community": (1150, 790),
    }
    normal = [("hospital", "cityhall"), ("cityhall", "eoc"), ("eoc", "startup"), ("startup", "board"), ("board", "university"),
              ("university", "community"), ("community", "water"), ("water", "crisis"), ("crisis", "base"), ("base", "hospital"),
              ("eoc", "board"), ("cityhall", "startup"), ("hospital", "crisis")]
    red = [("power", "hospital"), ("power", "crisis"), ("power", "cityhall"), ("power", "university"), ("power", "water"), ("power", "eoc")]
    for a, c in normal: b.append(edge(N[a], N[c], curve=18))
    for a, c in red: b.append(edge(N[a], N[c], red=True, dash=True, curve=-14))
    states = {"power": "fail", "hospital": "hit", "crisis": "hit", "cityhall": "hit", "water": "hit", "university": "hit", "eoc": "hit"}
    labels = {"power": "Substation 4", "hospital": "Regional hospital", "crisis": "988 crisis line", "cityhall": "City hall",
              "eoc": "Emergency ops", "university": "University", "water": "Water plant", "startup": "Startup",
              "board": "Boardroom", "base": "Installation", "community": "Shelter network"}
    icons = {"power": "power", "hospital": "hospital", "crisis": "crisis", "cityhall": "cityhall", "eoc": "eoc", "university": "university",
             "water": "water", "startup": "startup", "board": "board", "base": "shield", "community": "community"}
    for k, (x, y) in N.items():
        b.append(node(x, y, icons[k], labels[k], states.get(k, "ok"), r=44 if k == "power" else 34, label_dy=72 if k == "power" else 62, fs=20))
    # callout
    x, y = 1010, 450
    b.append(f'<path d="M{x+52} {y-34} L 1160 150 H 1560" fill="none" stroke="{RED}" stroke-width="1.2"/>')
    b.append(f'<text x="1170" y="134" font-family="{MONO}" font-size="22" letter-spacing="2" fill="{RED}">SINGLE POINT OF FAILURE</text>')
    b.append(f'<text x="1170" y="184" font-family="{MONO}" font-size="18" letter-spacing="1.5" fill="{MUTED}">6 CRITICAL FUNCTIONS · 5 SECTORS · T+00:42</text>')
    # legend bottom-left (inside safe zone)
    b.append(f'<g font-family="{MONO}" font-size="18" letter-spacing="1.5" fill="{MUTED}">'
             f'<line x1="300" y1="80" x2="350" y2="80" stroke="{LINE2}" stroke-width="1.6"/><text x="366" y="86">DEPENDENCY</text>'
             f'<line x1="300" y1="120" x2="350" y2="120" stroke="{RED}" stroke-width="2.4" stroke-dasharray="6 6"/><text x="366" y="126" fill="{RED}">CASCADE PATH</text></g>')
    return svg(W, H, "\n".join(b))

# ================= TTX: branching scenario timeline (1200x900) =================
def card(x, y, w, tag, title, sub, hot=False):
    h = 108
    stroke = RED if hot else "#3a424d"
    fill = "#24171a" if hot else PANEL
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>'
            f'<text x="{x+18}" y="{y+30}" font-family="{MONO}" font-size="14" letter-spacing="1.5" fill="{RED if hot else MUTED}">{esc(tag)}</text>'
            f'<text x="{x+18}" y="{y+64}" font-family="{SERIF}" font-size="26" fill="{TEXT}">{esc(title)}</text>'
            f'<text x="{x+18}" y="{y+90}" font-family="{MONO}" font-size="15" fill="{MUTED}">{esc(sub)}</text></g>')

def ttx():
    W, H = 1200, 900
    b = []
    b.append(f'<text x="70" y="90" font-family="{MONO}" font-size="18" letter-spacing="3" fill="{RED}">TABLETOP · REGIONAL HEATWAVE · RUN 07 OF 12</text>')
    b.append(f'<circle cx="926" cy="84" r="6" fill="{RED}"/><circle cx="926" cy="84" r="12" fill="none" stroke="{RED}" stroke-opacity=".35"/><text x="1130" y="90" text-anchor="end" font-family="{MONO}" font-size="18" letter-spacing="3" fill="{RED}">LIVE FEED ON</text>')
    b.append(f'<text x="70" y="140" font-family="{SERIF}" font-size="44" fill="{TEXT}">Branching scenario, live feed</text>')
    # timeline
    ty = 820
    b.append(f'<line x1="70" y1="{ty}" x2="1130" y2="{ty}" stroke="{LINE2}" stroke-width="1.3"/>')
    for i, t in enumerate(["T+0", "T+1h", "T+3h", "T+6h", "T+12h"]):
        x = 90 + i * 255
        b.append(f'<line x1="{x}" y1="{ty-6}" x2="{x}" y2="{ty+6}" stroke="{MUTED}"/><text x="{x}" y="{ty+30}" text-anchor="middle" font-family="{MONO}" font-size="16" letter-spacing="1.5" fill="{MUTED}">{t}</text>')
    cw = 300
    C = {
        "a": (70, 280, "INJECT 01 · CITY", "Grid at 98% load", "Rolling outages likely"),
        "b": (450, 190, "INJECT 04 · HEALTHCARE", "ED at 140% capacity", "Heat illness surge"),
        "c": (450, 375, "INJECT 05 · CRISIS LINE", "Wait time 18 min", "Call volume ×3"),
        "d": (830, 170, "DECISION · EOC", "Open cooling centers", "Player choice A"),
        "e": (830, 310, "LIVE FEED · NEWS", "Reporter calls the EOC", "Reacts to player moves", True),
        "f": (830, 450, "LIVE FEED · SOCIAL", "#DormBlackout trends", "University, 1,200 students"),
        "g": (450, 560, "INJECT 07 · NONPROFIT", "Volunteers unreachable", "Shelter staffing gap"),
        "h": (830, 610, "DECISION · CEO", "Delay product launch", "Player choice B"),
    }
    def mid_r(k): x, y, *_ = C[k]; return (x + cw, y + 54)
    def mid_l(k): x, y, *_ = C[k]; return (x, y + 54)
    links = [("a", "b", False), ("a", "c", True), ("a", "g", False), ("b", "d", False), ("c", "e", True), ("c", "f", False), ("g", "h", False)]
    for s, t, hot in links:
        (x1, y1), (x2, y2) = mid_r(s), mid_l(t)
        col = RED if hot else LINE2
        b.append(f'<path d="M{x1} {y1} C {x1+50} {y1}, {x2-50} {y2}, {x2} {y2}" fill="none" stroke="{col}" stroke-width="{2 if hot else 1.3}"{DASH if hot else ""}/>')
        b.append(f'<circle cx="{x2}" cy="{y2}" r="3.5" fill="{col}"/>')
    for k, v in C.items():
        x, y, tag, title, sub, *hot = v
        b.append(card(x, y, cw, tag, title, sub, bool(hot)))
    b.append(f'<text x="70" y="770" font-family="{MONO}" font-size="16" letter-spacing="1.5" fill="{MUTED}">MEASURED · 23 DECISIONS LOGGED · PRE/POST CAPTURED</text>')
    return svg(W, H, "\n".join(b))

# ================= COUNCIL: personas around a plan (800x1000) =================
def council():
    W, H = 800, 1000
    b = []
    cx, cy, R = 400, 460, 280
    people = [("Adversary", "shield"), ("Operations", "cityhall"), ("Clinical", "hospital"), ("Emergency", "eoc"),
              ("Community", "community"), ("Board", "board"), ("Compliance", "doc"), ("Detection", "eye"),
              ("Safety", "gauge"), ("Legal & comms", "crisis"), ("Contrarian", "dissent")]
    n = len(people)
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{LINE}" stroke-width="1"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.55:.0f}" fill="none" stroke="{LINE}" stroke-width="1" stroke-dasharray="3 6"/>')
    pos = []
    for i, (name, ic) in enumerate(people):
        a = -math.pi / 2 + 2 * math.pi * i / n
        pos.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    for i, (x, y) in enumerate(pos):
        hot = people[i][0] == "Contrarian"
        b.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{cx}" y2="{cy}" stroke="{RED if hot else LINE2}" stroke-width="{2 if hot else 1.1}"{DASH if hot else ""}/>')
    # center plan
    b.append(f'<circle cx="{cx}" cy="{cy}" r="78" fill="{PANEL}" stroke="#6b7380" stroke-width="1.6"/>')
    b.append(f'<g transform="translate({cx} {cy-10}) scale(2)" fill="none" stroke="#c9c6bf" stroke-width="1.4" stroke-linejoin="round">{ICONS["doc"]}</g>')
    b.append(f'<text x="{cx}" y="{cy+48}" text-anchor="middle" font-family="{MONO}" font-size="16" letter-spacing="2" fill="{MUTED}">THE PLAN</text>')
    for i, (x, y) in enumerate(pos):
        name, ic = people[i]
        hot = name == "Contrarian"
        a = -math.pi / 2 + 2 * math.pi * i / n
        ldy = 62 if math.sin(a) > -0.2 else -48
        b.append(node(round(x, 1), round(y, 1), ic, name, "hit" if hot else "ok", r=34, label_dy=ldy, fs=19))
    b.append(f'<text x="60" y="84" font-family="{MONO}" font-size="20" letter-spacing="3" fill="{RED}">AI SME COUNCIL</text>')
    b.append(f'<rect x="50" y="808" width="700" height="150" rx="8" fill="#24171a" stroke="{RED}" stroke-width="1.3"/>')
    b.append(f'<text x="78" y="846" font-family="{MONO}" font-size="16" letter-spacing="1.5" fill="{RED}">REQUIRED DISSENT · CONTRARIAN</text>')
    b.append(f'<text x="78" y="890" font-family="{SERIF}" font-size="29" fill="{TEXT}">“The shelter plan assumes volunteers</text>')
    b.append(f'<text x="78" y="928" font-family="{SERIF}" font-size="29" fill="{TEXT}">can reach it. In a flood, they can’t.”</text>')
    return svg(W, H, "\n".join(b))

# ================= PROGRAM: outcome spread across repeated runs (800x1000) =================
def program():
    W, H = 800, 1000
    b = []
    b.append(f'<text x="60" y="84" font-family="{MONO}" font-size="20" letter-spacing="3" fill="{RED}">EXERCISE PROGRAM · 12 RUNS</text>')
    b.append(f'<text x="60" y="136" font-family="{SERIF}" font-size="40" fill="{TEXT}">What tends to happen</text>')
    # panel 1: outcome spread
    b.append(f'<rect x="50" y="172" width="700" height="392" rx="8" fill="{PANEL}" stroke="#3a424d" stroke-width="1.3"/>')
    b.append(f'<text x="78" y="208" font-family="{MONO}" font-size="15" letter-spacing="1.5" fill="{MUTED}">OUTCOME SPREAD · HOURS TO STABILIZE</text>')
    x0, x1, hmax = 90, 710, 8
    X = lambda h: x0 + (x1 - x0) * h / hmax
    tx = X(4)
    b.append(f'<line x1="{tx:.0f}" y1="226" x2="{tx:.0f}" y2="512" stroke="{RED}" stroke-opacity=".7" stroke-width="1.3"{DASH}/>')
    b.append(f'<text x="{tx+8:.0f}" y="240" font-family="{MONO}" font-size="13" letter-spacing="1.5" fill="{RED}">TARGET</text>')
    rows = [("City · cooling centers", 1.6, 2.6, False), ("Healthcare · ED diversion", 2.4, 3.5, False),
            ("Crisis line · call wait", 1.8, 7.6, True), ("Board · press response", 0.7, 1.5, False)]
    rnd = random.Random(7)
    for i, (label, lo, hi, gap) in enumerate(rows):
        y = 290 + i * 62
        col = RED if gap else "#c9c6bf"
        b.append(f'<text x="{x0}" y="{y-20}" font-family="{MONO}" font-size="14" letter-spacing="1" fill="{RED if gap else MUTED}">{esc(label.upper())}</text>')
        b.append(f'<text x="{x1}" y="{y-20}" text-anchor="end" font-family="{MONO}" font-size="13" letter-spacing="1.5" fill="{RED if gap else MUTED}">{"REAL GAP" if gap else "ROBUST"}</text>')
        b.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{LINE}" stroke-width="1"/>')
        if gap:  # 9 of 12 runs miss the target
            vals = [rnd.uniform(lo, 3.8) for _ in range(3)] + [rnd.uniform(4.3, hi) for _ in range(9)]
        else:
            vals = [rnd.uniform(lo, hi) for _ in range(12)]
        b.append(f'<line x1="{X(min(vals)):.1f}" y1="{y}" x2="{X(max(vals)):.1f}" y2="{y}" stroke="{col}" stroke-opacity=".5" stroke-width="3"/>')
        for v in vals:
            b.append(f'<circle cx="{X(v):.1f}" cy="{y + rnd.uniform(-7, 7):.1f}" r="6" fill="{col}" fill-opacity=".85" stroke="{PANEL}" stroke-width="1.5"/>')
    for h in range(0, hmax + 1, 2):
        b.append(f'<text x="{X(h):.0f}" y="540" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">{h}h</text>')
    # panel 2: pre -> post
    b.append(f'<rect x="50" y="588" width="700" height="200" rx="8" fill="{PANEL}" stroke="#3a424d" stroke-width="1.3"/>')
    b.append(f'<text x="78" y="624" font-family="{MONO}" font-size="15" letter-spacing="1.5" fill="{MUTED}">PRE → POST · PARTICIPANT READINESS</text>')
    p0, p1 = 300, 710
    P = lambda v: p0 + (p1 - p0) * v / 100
    for i, (label, pre, post) in enumerate([("Activation", 42, 81), ("Handoffs", 35, 72), ("Public comms", 28, 77)]):
        y = 668 + i * 44
        b.append(f'<text x="78" y="{y+5}" font-family="{MONO}" font-size="14" letter-spacing="1" fill="{MUTED}">{label.upper()}</text>')
        b.append(f'<line x1="{p0}" y1="{y}" x2="{p1}" y2="{y}" stroke="{LINE}" stroke-width="1"/>')
        b.append(f'<line x1="{P(pre):.1f}" y1="{y}" x2="{P(post):.1f}" y2="{y}" stroke="#c9c6bf" stroke-opacity=".5" stroke-width="3"/>')
        b.append(f'<circle cx="{P(pre):.1f}" cy="{y}" r="6" fill="{PANEL}" stroke="{MUTED}" stroke-width="2"/>')
        b.append(f'<circle cx="{P(post):.1f}" cy="{y}" r="7" fill="#c9c6bf"/>')
        b.append(f'<text x="{P(post)+14:.1f}" y="{y+5}" font-family="{MONO}" font-size="13" fill="#c9c6bf">+{post-pre}</text>')
    # finding
    b.append(f'<rect x="50" y="812" width="700" height="150" rx="8" fill="#24171a" stroke="{RED}" stroke-width="1.3"/>')
    b.append(f'<text x="78" y="850" font-family="{MONO}" font-size="16" letter-spacing="1.5" fill="{RED}">FINDING 03 · BRIEFED TO LEADERSHIP</text>')
    b.append(f'<text x="78" y="894" font-family="{SERIF}" font-size="29" fill="{TEXT}">Crisis line staffing misses target</text>')
    b.append(f'<text x="78" y="932" font-family="{SERIF}" font-size="29" fill="{TEXT}">in 9 of 12 runs. Not luck: a real gap.</text>')
    return svg(W, H, "\n".join(b))

for name, fn in (("hero.svg", hero), ("ttx.svg", ttx), ("council.svg", council), ("program.svg", program)):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(fn())
print("ok")
