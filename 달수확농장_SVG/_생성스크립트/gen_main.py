# -*- coding: utf-8 -*-
import math, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_lib import *

OUT = r"D:/k-뉴딜 아카데미/side project_booknook/달수확농장_SVG"
os.makedirs(OUT, exist_ok=True)

# ======================= 3D-view.html 기준 수치 =======================
W, H, D = 120, 250, 147          # 3D 외형 (폭, 높이, 깊이)
FRONT_T = 3                      # 앞판 두께
SIDE_D = D - FRONT_T             # 옆판 깊이 = 144 (3D 외형 깊이 147 = 옆판 144 + 앞판 3)
INNER_W = 114                    # 안쪽 폭
Z_BACK, Z_FRONT_IN = -73.5, 70.5  # 뒤판 바깥면 / 앞판 안쪽면 (z)
FLOOR_TOP = 7                    # 바닥판 윗면 y

# 좌표계: x = 오른쪽(정면에서 볼 때), y = 위, z = 앞쪽(관람자 방향). 원점 = 바닥 중앙.
def floor_uv(x, z):              # 바닥판 평면도(뒤=위, 앞=아래) 좌표
    return x + INNER_W / 2.0, z + 70.5

parts_summary = []

# ============================ 02 합판 3mm 외장판 ============================
def p_S1():
    w, h = W, H
    cx, r, top, bot = 60.0, 52.1, 60.5, 243.6
    hole = "M%s %s V%s A%s %s 0 0 1 %s %s V%s Z" % (f(cx - r), f(bot), f(top), f(r), f(r), f(cx + r), f(top), f(bot))
    score = [
        (rect(1.6, 1.6, w - 3.2, h - 3.2), None),
        (rect(3.6, 3.6, w - 7.2, h - 7.2), None),
        (rect(5.4, 5.4, w - 10.8, h - 10.8), "1.4 1"),
    ]
    band = ("M%s %s V%s A%s %s 0 0 1 %s %s V%s H%s V%s A%s %s 0 0 0 %s %s V%s Z" % (
        f(cx - r - 1.3), f(bot), f(top), f(r + 1.3), f(r + 1.3), f(cx + r + 1.3), f(top), f(bot),
        f(cx + r), f(top), f(r), f(r), f(cx - r), f(top), f(bot)))
    eng = [band]
    for k in range(33):                           # 좌우 가장자리 별빛 (표지 텍스처 좌표 ×0.2)
        y = (75 + 34 * k) * 0.2
        eng.append(sparkle(2.2, y, 1.3, 2.2)); eng.append(sparkle(114.8, y, 1.7, 2.5))
    for k in range(14):
        eng.append(sparkle((50 + 36 * k) * 0.2, 247.2, 2.0, 1.2))
    eng.append(sparkle(60.0, 7.2, 2.8, 4.4))
    eng.append(star(9.6, 13.2, 5, 4.4, 1.8)); eng.append(star(103.2, 14.8, 5, 4.0, 1.6))
    eng.append(sparkle(109.6, 10.8, 2.6, 2.6))
    return part("S1", "앞판(아치 구멍)", w, h, 1, [rect(0, 0, w, h), hole], score, eng,
                note="3mm 합판 · 앞면 = 바깥면")

def p_S2():
    L, h = SIDE_D, H
    cut = [side_panel_outline(L, h)]
    # 바깥면(정면에서 왼쪽 면을 밖에서 본 모습: 앞쪽 = 오른쪽). 텍스처 px×0.2
    eng = [crescent(75, 112, 19.2, 16, 8.8)]
    for (x, y, r) in [(28, 36, 3.2), (116, 52, 2.4), (44, 176, 3.6), (108, 204, 3.0), (32, 216, 2.2), (122, 124, 2.0)]:
        eng.append(star(x, y, 5, r, r * 0.42))
    outer = part("S2", "왼쪽 옆판 · 바깥면", L, h, 1, cut, [], eng,
                 note="바깥면: 앞쪽=오른쪽",
                 labels=[(2, 6, "바깥면 각인(검정) · 앞쪽이 오른쪽 · 이 판을 자름")])
    # 안쪽면: 같은 판을 뒤집어(안쪽이 위로, 앞쪽 = 왼쪽) 새김. x = u - 3 (앞판 3mm 만큼 잘림)
    eng2 = [(ellipse(68, 104, 23, 35), "1.2 1.2"), crescent(70, 104, 18, 15, 8.2)]
    for (x, y, r) in [(36, 48, 3.2), (104, 62, 2.8), (38, 152, 3.6), (96, 166, 3.0), (52, 196, 2.4), (112, 110, 2.4)]:
        eng2.append(sparkle(x - 3, y, r, r))
    inner = part("S2안쪽", "왼쪽 옆판 · 안쪽면(같은 판을 뒤집어서)", L, h, 1, [], [], [], eng2,
                 note="새로 자르는 판 아님",
                 ref=[side_panel_outline(L, h)],
                 labels=[(2, 6, "안쪽면 각인(보라) · 위 S2 판을 뒤집어 안쪽이 위로 · 앞쪽이 왼쪽 · 점선 외곽선은 위치 참고용(자르지 않음)")])
    return [outer, inner]

def p_S3():
    L, h = SIDE_D, H
    cut = [side_panel_outline(L, h)]
    eng = []
    # 바깥면(오른쪽 면을 밖에서 본 모습: 앞쪽 = 왼쪽). u = x + 3
    for (x, y, r) in [(36, 44, 3.2), (108, 68, 2.6), (72, 124, 4.0), (32, 184, 2.4), (112, 208, 3.2)]:
        eng.append(star(x - 3, y, 5, r, r * 0.42))
    return part("S3", "오른쪽 옆판(별)", L, h, 1, cut, [], eng,
                note="바깥면: 앞쪽=왼쪽", labels=[(2, 6, "바깥면에서 본 모습(앞쪽이 왼쪽)")])

def p_S4(hang):
    depth, body = SIDE_D, INNER_W
    holes = []
    labs = []
    for i, (hx, hy, hz, is_star) in enumerate(hang):
        px, py = hx + 60, hz + 73.5
        holes.append(circle(px, py, 0.6))
        labs.append((px + 1.2, py + 0.6, "C%d" % (i + 1)))
    return part("S4", "상판(평면도, 뒤=위)", body + 6, depth, 1, [top_panel_outline(depth, body)] + holes, [], [],
                note="천장 실 구멍 7개", labels=labs)

def p_S5():
    return part("S5", "바닥판(평면도, 뒤=위)", INNER_W + 6, SIDE_D, 1, [top_panel_outline(SIDE_D, INNER_W)], [], [])

def p_S6():
    return part("S6", "뒤판", INNER_W, 244, 1, [rect(0, 0, INNER_W, 244)], [], [],
                note="끼움 판: 안쪽 폭 114에 들어가므로 필요하면 -0.3 줄여 가공")

def sky_star_positions():
    out = []
    for i in range(55):
        x = ((i * 37) % 102) - 51
        y = ((i * 53) % 215) - 102
        sc = 1.1 if i % 3 == 0 else 0.7
        out.append((x, y, sc))
    return out

def moon_bar_positions():
    """달 지지대가 S7(속판)을 통과하는 (x,y) 전역좌표 — 달 로컬 (-18, ±10) 을 달의 기울기 0.26rad 로 변환"""
    res = []
    for ly in (10, -10):
        lx = -18
        xr = lx * math.cos(0.26) - ly * math.sin(0.26)
        yr = lx * math.sin(0.26) + ly * math.cos(0.26)
        res.append((-16 + xr, 184 + yr, lx, ly))
    return res

def p_S7():
    w, h = INNER_W, 241
    eng = []
    for (x, y, sc) in sky_star_positions():
        eng.append(sparkle(x + 57, 244.5 - (124 + y), 1.65 * sc / 1.1 * 1.1, 1.65 * sc / 1.1 * 1.1, 0.22))
    cut = [rect(0, 0, w, h)]
    labs = []
    for i, (gx, gy, lx, ly) in enumerate(moon_bar_positions()):
        cut.append(rect(gx + 57 - 3.1, 244.5 - gy - 1.575, 6.2, 3.15))   # y: 판 윗면 y=244.5 기준
        labs.append((gx + 57 + 4, 244.5 - gy + 0.7, "B%d 슬롯 (x=%s, y=%s)" % (i + 1, f(gx), f(gy))))
    return part("S7", "속판(밤하늘)", w, h, 1, cut, [], eng,
                note="전면(앞쪽)을 보는 면에 금빛 별 55개", labels=labs)

# ============================ 03 합판 3mm 달 조명상자 ============================
R1, R2, DD = 27.2, 22.75, 12.5      # 큰 초승달 형태
MOON_DEPTH_PLY = 5                  # 합판 5겹 = 15mm
def moon_origin():
    a, h = crescent_geom(R1, R2, DD)
    return R1, R1                   # 달 중심이 놓일 로컬 위치(바깥원 중심)

def p_moon_layers():
    cx, cy = R1, R1
    w, h = R1 + crescent_geom(R1, R2, DD)[0], 2 * R1
    # L1: 뒤판(막힌 면) + 지지대 구멍 2 + 전선 구멍
    slots = []
    for (gx, gy, lx, ly) in moon_bar_positions():
        slots.append(rrect(cx + lx, cy - ly, 6.2, 3.15, math.degrees(0.26)))   # 달 기울기 반대로 돌려서 전역 수평 슬롯
    wire = circle(cx - 14, cy + 0, 2.5)
    L1 = part("M1", "달 뒤판(L1)", w, h, 1, [crescent(cx, cy, R1, R2, DD)] + slots + [wire], [], [],
              note="LED·전선 구멍 Ø5", labels=[])
    # L2~L5: 바깥 초승달 + 안쪽 빈 공간(벽 3mm)
    Ri1, Ri2 = R1 - 3, R2 + 3
    ring = [crescent(cx, cy, R1, R2, DD), crescent(cx, cy, Ri1, Ri2, DD)]
    Lr = part("M2", "달 링(L2~L5)", w, h, 4, ring, [], [], note="빈 공간에 LED")
    return [L1, Lr]

def p_bars():
    body_w, tab_w, tab_l = 8.0, 6.0, 3.0
    length = 59.2
    total = length + 2 * tab_l
    off = (body_w - tab_w) / 2
    pts = [(off, 0), (off + tab_w, 0), (off + tab_w, tab_l), (body_w, tab_l), (body_w, tab_l + length),
           (off + tab_w, tab_l + length), (off + tab_w, total), (off, total), (off, tab_l + length),
           (0, tab_l + length), (0, tab_l), (off, tab_l)]
    return part("B", "달 지지대", body_w, total, 2, [poly(pts)], [], [], note="길이 65.2 (몸통 59.2 + 양끝 탭 3)")

# ============================ 04 합판 3mm 덩굴 줄기 ============================
VC = (0.0, 189.5)   # 아치 중심 (x, y)
def vine_defs():
    # (이름, 줄기 x, z, 호 반지름 or None, 줄기 위쪽 y, layer 정의)
    return [
        dict(id="VA", x=-48.5, z=40, R=48.5, top=189.5, layer=dict(z=40, x=-51, ymin=25, ymax=185, step=15), idx=0, arch=dict(z=38, r=48.5, count=18, aIdx=0)),
        dict(id="VB", x=-46.0, z=13, R=46.0, top=189.5, layer=dict(z=12, x=-54, ymin=40, ymax=205, step=18), idx=1, arch=dict(z=14, r=46.0, count=14, aIdx=1)),
        dict(id="VC", x=-55.0, z=-18, R=None, top=222, layer=dict(z=-18, x=-55, ymin=55, ymax=215, step=20), idx=2, arch=None),
    ]

STRIP_W = 3.4
TAB_W, TAB_L = 2.4, 3.0
def build_vine_panel(v):
    sw = STRIP_W / 2.0
    xl = v["x"]
    y_floor = FLOOR_TOP
    # 로컬 원점: 판 외곽 좌상단. 판 좌표계 x는 전역 x 그대로(+shift), y는 전역 y를 아래로 뒤집음
    if v["R"]:
        R = v["R"]
        x_min = xl - sw
        x_max = VC[0] + R + sw
        y_top = VC[1] + R + sw          # 전역 y 의 최댓값
    else:
        x_min, x_max, y_top = xl - sw, xl + sw, v["top"]
    y_bot = y_floor - TAB_L
    W_ = x_max - x_min
    H_ = y_top - y_bot
    X = lambda gx: gx - x_min
    Y = lambda gy: y_top - gy
    cut = []
    if v["R"]:
        Ro, Ri = R + sw, R - sw
        cx, cy = X(VC[0]), Y(VC[1])
        xo_left, xi_left = cx - Ro, cx - Ri
        tabx0 = (xo_left + xi_left) / 2 - TAB_W / 2
        tabx1 = tabx0 + TAB_W
        # 바깥 왼쪽 아래 → 위(스프링라인) → 바깥호(시계방향) → 오른쪽 끝 → 안쪽호(반시계) → 안쪽 왼쪽 아래 → 탭 → 닫기
        d = ("M%s %s V%s A%s %s 0 0 1 %s %s H%s A%s %s 0 0 0 %s %s V%s H%s V%s H%s V%s Z" % (
            f(xo_left), f(Y(y_floor)), f(cy), f(Ro), f(Ro), f(cx + Ro), f(cy), f(cx + Ri), f(Ri), f(Ri),
            f(xi_left), f(cy), f(Y(y_floor)), f(tabx1), f(Y(y_bot)), f(tabx0), f(Y(y_floor))))
        cut.append(d)
    else:
        tabx0 = X(xl) - TAB_W / 2
        tabx1 = tabx0 + TAB_W
        d = poly([(X(xl) - sw, 0), (X(xl) + sw, 0), (X(xl) + sw, Y(y_floor)), (tabx1, Y(y_floor)), (tabx1, Y(y_bot)),
                  (tabx0, Y(y_bot)), (tabx0, Y(y_floor)), (X(xl) - sw, Y(y_floor))])
        cut.append(d)
    # 잎·꽃·별 붙일 자리 표시 (선각인)
    score, labs = [], []
    L = v["layer"]
    y = L["ymin"]
    nleaf = nflower = nstar = 0
    cap = VC[1] if v["R"] else 1e9      # 호가 시작되는 높이 위쪽은 호 줄기와 겹쳐서 생략
    while y <= L["ymax"] + 1e-9:
        for dy, kind in ((0, "leaf"), (6, "leaf")):
            if y + dy > cap:
                continue
            sx = X(xl)
            yy = Y(y + dy)
            score.append(poly([(sx - sw, yy), (sx + sw, yy)], close=False))
            nleaf += 1
        if (y + v["idx"] * 7) % 2 == 0:
            if y + 3 <= cap:
                score.append(circle(X(xl), Y(y + 3), 0.9)); nflower += 1
        else:
            if y + 4 <= cap:
                score.append(poly([(X(xl) - 0.9, Y(y + 4)), (X(xl), Y(y + 4) - 0.9), (X(xl) + 0.9, Y(y + 4)), (X(xl), Y(y + 4) + 0.9)])); nstar += 1
        y += L["step"]
    arch_leaf = arch_flower = 0
    if v["arch"]:
        A = v["arch"]
        for i in range(A["count"] + 1):
            ang = math.pi - (i / A["count"]) * math.pi
            ax = VC[0] + math.cos(ang) * A["r"]
            ay = VC[1] + math.sin(ang) * A["r"]
            nx_, ny_ = math.cos(ang), math.sin(ang)
            score.append(poly([(X(ax) - nx_ * sw, Y(ay) + ny_ * sw), (X(ax) + nx_ * sw, Y(ay) - ny_ * sw)], close=False))
            arch_leaf += 1
            if i % 3 == A["aIdx"]:
                score.append(circle(X(ax), Y(ay - 2.2), 0.9)); arch_flower += 1
    meta = dict(leaf=nleaf + arch_leaf, flower=nflower + arch_flower, star=nstar)
    p = part(v["id"], "덩굴 줄기 %s (z=%s)" % (v["id"][-1], f(v["z"])), W_, H_, 1, cut, score, [],
             note="x=%s z=%s" % (f(xl), f(v["z"])),
             labels=[(1, 4, "잎 %d · 꽃 %d · 별 %d (자리표시)" % (meta["leaf"], meta["flower"], meta["star"]))])
    return p, meta

# ============================ 05 합판 3mm 소품 ============================
def p_brackets():
    pts = [(0, 0), (13, 0), (0, 13)]       # 3D 브래킷 직각삼각형 13×13
    return part("BR", "선반 받침 삼각형", 13, 13, 6, [poly(pts)], [], [], note="선반 아래 접착 (좌 x=-46, 우 x=-24 위치)")

def basket_layers():
    out = []
    for k in range(5):
        y = 1.5 + 3 * k
        r = 9.5 + 3.5 * (y / 16.0)
        a, b = 1.18 * r, 0.75 * r
        out.append((k, a, b))
    return out

def p_basket():
    res = []
    for (k, a, b) in basket_layers():
        w, h = 2 * a, 2 * b
        eng_pts = []
        score = []
        labs = []
        if k == 4:                           # 맨 윗층에 꽃 자리 표시
            for i in range(22):
                ang = i * 2.399
                rad = math.sqrt(i / 22.0) * 11
                fx = a + math.cos(ang) * rad * 1.12
                fz = b + math.sin(ang) * rad * 0.72
                score.append(circle(fx, fz, 0.8))
                labs.append((fx + 1, fz + 0.8, str(i + 1)))
        res.append(part("BK%d" % (k + 1), "바구니 %d층(밑→위)" % (k + 1), w, h, 1, [ellipse(a, b, a, b)], score, [], labels=labs))
    return res

def p_can():
    s = 1.45
    # 단위: 3D 로컬(위쪽 +y) → 외곽선 점(위쪽 +y) 후 SVG로 뒤집기
    body_bl, body_br = -6.38, 6.38
    pts_up = [(-6.38, 0), (6.38, 0), (6.30, 4.45), (13.04, 11.24), (14.70, 11.84), (12.58, 14.24), (11.90, 12.54),
              (5.90, 8.14), (5.945, 11.89), (-5.945, 11.89), (-6.1, 11.3)]
    # 손잡이 바깥 호 (중심 (-5.075, 6.2), R=5.2) 위쪽 교점 y=11.3 → 아래쪽 y=1.1 사이를 왼쪽으로 돌아감
    hc, hr = (-5.075, 6.2), 5.2
    arc_pts = []
    a0 = math.degrees(math.acos((-6.1 - hc[0]) / hr))      # 위쪽 교점 각도
    for i in range(0, 19):
        ang = a0 + (360 - 2 * a0) * i / 18.0
        arc_pts.append((hc[0] + hr * math.cos(math.radians(ang)), hc[1] + hr * math.sin(math.radians(ang))))
    outline_up = pts_up[:-1] + arc_pts          # (-6.1, 11.3) 에서 시작해 호를 돌아 (-6.1, 1.1) 로
    outline_up += [(-6.38, 0)]
    maxy = max(p[1] for p in outline_up)
    minx = min(p[0] for p in outline_up)
    maxx = max(p[0] for p in outline_up)
    def tr(p): return (p[0] - minx, maxy - p[1])
    cut = [poly([tr(p) for p in outline_up])]
    # 손잡이 안쪽 창
    ri = 3.8
    a1 = math.degrees(math.acos((-6.1 - hc[0]) / ri))
    win = []
    for i in range(0, 15):
        ang = a1 + (360 - 2 * a1) * i / 14.0
        win.append((hc[0] + ri * math.cos(math.radians(ang)), hc[1] + ri * math.sin(math.radians(ang))))
    cut.append(poly([tr(p) for p in win]))
    return part("CAN", "물뿌리개(옆모습, ×1.45)", maxx - minx, maxy, 4, cut, [], [], note="3mm 4장 겹침=12mm")

def p_pots():
    res = []
    for name, s in (("PT1", 1.0), ("PT2", 0.85)):
        tw, bw, h = 9.2 * s, 6.8 * s, 8.2 * s
        off = (tw - bw) / 2
        plain = poly([(0, 0), (tw, 0), (tw - off, h), (off, h)])
        notch = poly([(0, 0), (tw / 2 - 0.85, 0), (tw / 2 - 0.85, 3), (tw / 2 + 0.85, 3), (tw / 2 + 0.85, 0), (tw, 0), (tw - off, h), (off, h)])
        res.append(part(name + "a", "화분 %s 앞·뒤층" % name[-1], tw, h, 2, [plain], [], [], note="스케일 %s" % s))
        res.append(part(name + "b", "화분 %s 가운데층(새싹 홈)" % name[-1], tw, h, 1, [notch], [], []))
    return res

def p_lantern():
    # 집 모양 랜턴: 지붕 삼각형(11.6폭, 높이 5.2) + 몸통 10.5×11.5, 창 타원 3.84×6.24
    w = 11.6
    ox = (11.6 - 10.5) / 2
    pts = [(w / 2, 0), (w, 5.2), (w - ox, 5.2), (w - ox, 16.7), (ox, 16.7), (ox, 5.2), (0, 5.2)]
    outline = poly(pts)
    win_f = ellipse(w / 2, 16.7 - 5.75, 1.92, 3.12)
    win_m = ellipse(w / 2, 16.7 - 5.75, 2.6, 3.9)
    return [part("LF", "랜턴 앞층(창)", w, 16.7, 1, [outline, win_f], [], [], note="3mm 합판"),
            part("LM", "랜턴 가운데층(큰 창)", w, 16.7, 1, [outline, win_m], [], [], note="3mm 합판")]

def p_corks():
    return part("CK", "병마개", 8.6, 8.6, 2, [circle(4.3, 4.3, 4.3)], [], [], note="3mm 합판 Ø8.6")

# ============================ 06 합판 4mm 바닥·선반 ============================
def ladder_to_global(xl, zl, theta=-0.32, origin=(25, 12)):
    c, s = math.cos(theta), math.sin(theta)
    return origin[0] + xl * c + zl * s, origin[1] - xl * s + zl * c

def global_to_ladder(gx, gz, theta=-0.32, origin=(25, 12)):
    c, s = math.cos(theta), math.sin(theta)
    dx, dz = gx - origin[0], gz - origin[1]
    return dx * c - dz * s, dx * s + dz * c

TILT = 0.13
LEG_L = 104.5
FOOT_ZL = 7.5 + (LEG_L / 2.0) * math.sin(TILT)       # 사다리 다리 아래끝 z (로컬) ≈ 14.28
FRONT_X, BACK_X = 11.2, 10.7
LADDER_DEG = math.degrees(-0.32)  # 평면도에서 사다리 로컬 x축이 전역 x축과 이루는 각

PICKET_X = [-22 + (-24.8 + 9.9 * i) for i in range(6)]
PICKET_Z = 48.0

SHELF_Y = [47.75, 85.75, 123.75]      # 4mm 선반 중심 y (윗면 = 49.75, 87.75, 125.75)
PILLAR_X, PILLAR_Z0, PILLAR_Z1 = -54.0, -48.5, -23.5   # x 중심, z 범위
SHELF_TABS_Z = [(-49 + 3, -49 + 9), (-49 + 17, -49 + 23)]   # 선반 탭의 전역 z 범위

def floor_slots():
    """바닥판 슬롯 목록: (이름, u, v, 폭u, 폭v, 회전각deg)"""
    sl = []
    u, v = floor_uv(PILLAR_X, (PILLAR_Z0 + PILLAR_Z1) / 2)
    sl.append(("기둥", u, v, 4.1, 21.2, 0))
    for i, x in enumerate(PICKET_X):
        u, v = floor_uv(x, PICKET_Z)
        sl.append(("울타리%d" % (i + 1), u, v, 3.7, 2.1, 0))
    # 사다리 발 4개(앞 2, 뒤 2): 슬롯 긴 방향 = 사다리 로컬 x, 짧은 방향 = 사다리 로컬 z
    for name, xl, zl in (("사다리앞L", -FRONT_X, FOOT_ZL), ("사다리앞R", FRONT_X, FOOT_ZL),
                         ("사다리뒤L", -BACK_X, -FOOT_ZL), ("사다리뒤R", BACK_X, -FOOT_ZL)):
        gx, gz = ladder_to_global(xl, zl)
        u, v = floor_uv(gx, gz)
        sl.append((name, u, v, 3.6, 2.6, math.degrees(math.atan2(-math.sin(-0.32), math.cos(-0.32)))))
    for vid, vx, vz in (("덩굴A", -48.5, 40), ("덩굴B", -46.0, 13), ("덩굴C", -55.0, -18)):
        u, v = floor_uv(vx, vz)
        sl.append((vid, u, v, 2.5, 3.15, 0))
    u, v = floor_uv(-8, 55)
    sl.append(("모종삽", u, v, 2.5, 2.1, 0))
    return sl

def p_floor():
    w, h = INNER_W, 141
    cut = [rect(0, 0, w, h)]
    labs = []
    for (name, u, v, a, b, deg) in floor_slots():
        cut.append(rrect(u, v, a, b, deg))
        labs.append((u + 2.5, v - 1.5, name))
    score = []
    for i in range(45):                      # 풀잎(종이) 위치 표시
        gx = ((i * 29) % 102) - 51
        gz = ((i * 41) % 126) - 63
        score.append(circle(gx + 57, gz + 70.5, 0.6))
        if i % 3 == 0:                       # 작은 꽃(종이 Ø3.2) 위치 표시
            score.append(circle(gx + 1.5 + 57, gz + 1.2 + 70.5, 1.6))
    return part("S9", "바닥판(평면도, 뒤=위)", w, h, 1, cut, score, [],
                note="4mm 합판 · 슬롯 + 풀·꽃 위치 표시", labels=labs)

def p_pillar():
    pw, ph = 25.0, 152.0
    tab_w, tab_l = 21.0, 3.5
    ox = (pw - tab_w) / 2
    outline = poly([(0, 0), (pw, 0), (pw, ph), (ox + tab_w, ph), (ox + tab_w, ph + tab_l), (ox, ph + tab_l), (ox, ph), (0, ph)])
    cut = [outline]
    for sy in SHELF_Y:
        ysvg = 159 - sy                       # 기둥 윗끝 y=159 에서 아래로
        for (z0, z1) in SHELF_TABS_Z:
            zc = (z0 + z1) / 2 - PILLAR_Z0
            cut.append(rect(zc - 3.05, ysvg - 2.05, 6.1, 4.1))
    return part("PL", "선반 기둥(왼쪽 벽 옆)", pw, ph + tab_l, 1, cut, [], [],
                note="4mm 합판 · 왼쪽 = 뒤쪽")

def p_shelf():
    tabs, depth, body = 4.0, 26.0, 36.25
    pts = [(tabs, 0), (tabs + body, 0), (tabs + body, depth), (tabs, depth), (tabs, 23), (0, 23), (0, 17), (tabs, 17),
           (tabs, 9), (0, 9), (0, 3), (tabs, 3)]
    return part("SH", "선반", tabs + body, depth, 3, [poly(pts)], [], [], note="4mm 합판 · 왼쪽 끝 탭이 기둥을 관통")
