# -*- coding: utf-8 -*-
from gen_main import *

# ============================ 07 합판 2mm: 울타리·사다리·모종삽·신발 ============================
def s_axis(i):                       # 사다리 앞다리 발판 i번째 중심의 다리 축 방향 위치 (아래끝 기준)
    return (12 + 9.5 * i - 0.45) / math.cos(TILT)

def p_ladder_front():
    Lf, w, lw, tw, tl = LEG_L, 27.0, 4.6, 3.4, 3.0
    top_notch = Lf - (s_axis(8) + 1.31)
    bot_notch = s_axis(0) - 1.31
    yt = tl
    ya, yb = yt, yt + Lf
    cL = lw / 2
    cR = w - lw / 2
    pts = [(0, ya), (cL - tw / 2, ya), (cL - tw / 2, 0), (cL + tw / 2, 0), (cL + tw / 2, ya), (lw, ya), (lw, ya + top_notch),
           (w - lw, ya + top_notch), (w - lw, ya), (cR - tw / 2, ya), (cR - tw / 2, 0), (cR + tw / 2, 0), (cR + tw / 2, ya), (w, ya),
           (w, yb), (cR + tw / 2, yb), (cR + tw / 2, yb + tl), (cR - tw / 2, yb + tl), (cR - tw / 2, yb), (w - lw, yb),
           (w - lw, yb - bot_notch), (lw, yb - bot_notch), (lw, yb), (cL + tw / 2, yb), (cL + tw / 2, yb + tl),
           (cL - tw / 2, yb + tl), (cL - tw / 2, yb), (0, yb)]
    cut = [poly(pts)]
    for i in range(8):
        lo, hi = s_axis(i) + 1.31, s_axis(i + 1) - 1.31
        cut.append(rect(lw, yb - hi, w - 2 * lw, hi - lo))
    return part("LD1", "사다리 앞 다리판(발판 창 8개)", w, Lf + 2 * tl, 1, cut, [], [],
                note="2mm 합판 · 위가 윗끝", labels=[(1, 4, "위 탭 → 윗발판 슬롯 / 아래 탭 → 바닥 슬롯")])

def p_rungcaps():
    return part("LD2", "사다리 발판 덧댐(앞면에 접착)", 24, 2.6, 9, [rect(0, 0, 24, 2.6)], [], [],
                note="앞 다리판 발판 위치에 9개 접착 (밑에서 12, 21.5, …, 88 높이)")

def p_ladder_back():
    Lf, lw, tw, tl = LEG_L, 3.8, 3.4, 3.0
    w = 2 * (BACK_X + lw / 2)
    ya, yb = tl, tl + Lf
    s_b = (38 - 0.45) / math.cos(TILT)
    yc0, yc1 = yb - s_b - 1.5, yb - s_b + 1.5
    cL, cR = lw / 2, w - lw / 2
    pts = [(0, ya), (cL - tw / 2, ya), (cL - tw / 2, 0), (cL + tw / 2, 0), (cL + tw / 2, ya), (lw, ya), (lw, yc0), (w - lw, yc0),
           (w - lw, ya), (cR - tw / 2, ya), (cR - tw / 2, 0), (cR + tw / 2, 0), (cR + tw / 2, ya), (w, ya), (w, yb),
           (cR + tw / 2, yb), (cR + tw / 2, yb + tl), (cR - tw / 2, yb + tl), (cR - tw / 2, yb), (w - lw, yb), (w - lw, yc1),
           (lw, yc1), (lw, yb), (cL + tw / 2, yb), (cL + tw / 2, yb + tl), (cL - tw / 2, yb + tl), (cL - tw / 2, yb), (0, yb)]
    return part("LD3", "사다리 뒤 다리판(가로대 1)", w, Lf + 2 * tl, 1, [poly(pts)], [], [], note="2mm 합판")

def p_ladder_step():
    w, d = 24.0, 14.0
    cut = [rect(0, 0, w, d)]
    for sx in (-1, 1):
        ux = 12 + sx * 10.95
        cut.append(rect(ux - 2.0, 7 - 2.2, 4.0, 4.4))
    # 아이 실루엣 발 슬롯 (사다리 로컬 좌표로 환산)
    gx, gz = 25 + 5.7, 12 + 1.0
    xl, zl = global_to_ladder(gx, gz)
    cut.append(rrect(12 + xl, 7 + zl, 5.1, 2.1, math.degrees(math.atan2(math.sin(-0.32), math.cos(-0.32)))))
    return part("LD4", "사다리 윗발판(슬롯 3개)", w, d, 1, cut, [], [],
                note="2mm 합판 · 평면도, 위쪽=뒤", labels=[(1, 17, "양끝 슬롯=앞·뒤 다리판 윗탭 / 기울어진 슬롯=아이 발 탭")])

def p_fence():
    rails = part("FR", "울타리 가로대", 59.6, 4.2, 2, [rect(0, 0, 59.6, 4.2)],
                 [poly([(xc + 51.8 - 3.3, 0), (xc + 51.8 - 3.3, 4.2)], close=False) for xc in PICKET_X] +
                 [poly([(xc + 51.8 + 3.3, 0), (xc + 51.8 + 3.3, 4.2)], close=False) for xc in PICKET_X],
                 [], note="말뚝 뒤쪽에 접착, 높이 y=12.4~16.6 / 25.4~29.6")
    pw = 6.6
    pts = [(3.3, 0), (6.6, 4.5), (6.6, 29.4), (5.1, 29.4), (5.1, 32.9), (1.5, 32.9), (1.5, 29.4), (0, 29.4), (0, 4.5)]
    pick = part("FP", "울타리 말뚝", pw, 32.9, 6, [poly(pts)], [], [], note="2mm 합판 · 바닥 슬롯 6개에 꽂음")
    return [rails, pick]

def p_trowel():
    pts = [(-1.2, 0), (1.2, 0), (1.2, 7.83), (0.65, 7.83), (0.65, 8.7), (3.48, 8.7), (1.2, 14.88), (1.2, 21.13), (-1.2, 21.13),
           (-1.2, 14.88), (-3.48, 8.7), (-0.65, 8.7), (-0.65, 7.83), (-1.2, 7.83)]
    return part("TR", "모종삽(×1.45)", 6.96, 21.13, 1, [poly([(x + 3.48, y) for x, y in pts])], [], [],
                note="2mm 합판 · 아래 탭 → 바닥 슬롯")

def p_shoes():
    a, b = 5.1, 4.1
    pts = []
    for k in range(0, 37):
        th = math.radians(5 * k)
        x, y = a * math.cos(th), b * math.sin(th)
        t = 5 * k
        if 115 <= t <= 155:                 # 뒤꿈치 입구
            y -= 1.3 * math.sin((t - 115) / 40.0 * math.pi)
        pts.append((a + x, b - y))
    pts.append((a - a, b))
    # 발 앞코가 오른쪽
    return part("SZ", "아이 신발(옆모습)", 2 * a, b, 4, [poly(pts)], [], [], note="2mm 합판 2장 겹침 = 신발 한 짝 (한 켤레 = 4장)")

# ============================ 08~10 아크릴 ============================
def p_opal_moon():
    cx, cy = R1, R1
    w, h = R1 + crescent_geom(R1, R2, DD)[0], 2 * R1
    eng = []
    for (x, y, r) in [(-21, 2, 3.2), (-15, -13, 2.8), (-14, 14, 3.0), (-5, -20, 2.2), (-4, 21, 2.4), (-18, -5, 2.0)]:
        eng.append(circle(cx + x, cy - y, r))
    return part("MF", "달 앞판(유백 아크릴)", w, h, 1, [crescent(cx, cy, R1, R2, DD)], [], eng, note="3mm 유백 아크릴 · 크레이터 6개 각인")

def p_jar_discs():
    d = 11.2
    plain = part("JD", "병 몸통 디스크(투명)", d, d, 8, [circle(d / 2, d / 2, d / 2)], [], [], note="3mm 투명 아크릴 Ø11.2 (병 1개 = 5장)")
    cr = crescent(d / 2 - 1.5, d / 2, 3.128, 2.616, 1.4375)
    eng = part("JDE", "병 가운데 디스크(초승달 각인)", d, d, 2, [circle(d / 2, d / 2, d / 2)], [], [cr], note="병 1개당 가운데(3번째) 한 장")
    return [plain, eng]

def p_lantern_back():
    w = 11.6
    ox = (11.6 - 10.5) / 2
    pts = [(w / 2, 0), (w, 5.2), (w - ox, 5.2), (w - ox, 16.7), (ox, 16.7), (ox, 5.2), (0, 5.2)]
    return part("LB", "랜턴 뒷층(유백 아크릴)", w, 16.7, 1, [poly(pts)], [], [], note="3mm 유백 아크릴, 창 없음")

CHILD_PTS = [
    (60.4, 90.8), (62.2, 90.2), (63.4, 91.6), (64.4, 94.2), (67.4, 97), (70.2, 100), (72, 101.2),
    (72.2, 99.2), (72, 97.2), (73, 95.2), (75.6, 93.6), (79, 93), (82, 94.2), (83.8, 97), (84.8, 101.8),
    (83, 103.6), (81.6, 104.6), (83, 108.8), (85, 113), (87, 115.2), (87.6, 117.2), (86.2, 117.6),
    (84.6, 115.2), (83, 112), (84, 116), (86.6, 122), (88.4, 122.8), (85.2, 126.4), (82.6, 126.6),
    (83.4, 132), (84.8, 135.4), (86.6, 138), (86.2, 139.2), (77.2, 139.2), (76.8, 134.2), (78.2, 129.2),
    (79, 126.8), (71.8, 127.2), (69, 125.8), (70, 122.6), (71.2, 116.4), (72, 110.2), (72.4, 106.2),
    (71.2, 104.6), (68, 101.6), (64.4, 97.2), (61.8, 95.2), (60, 92.4)]

def p_child():
    pts = []
    for p in CHILD_PTS:
        pts.append(p)
        if p == (86.2, 139.2):               # 바닥 변: 발 탭 삽입 (폭 5, 길이 3)
            pts += [(84.2, 139.2), (84.2, 142.2), (79.2, 142.2), (79.2, 139.2)]
    minx = min(p[0] for p in pts); miny = min(p[1] for p in pts)
    maxx = max(p[0] for p in pts); maxy = max(p[1] for p in pts)
    return part("CH", "아이 실루엣(검정 아크릴)", maxx - minx, maxy - miny, 1,
                [poly([(x - minx, y - miny) for x, y in pts])], [], [],
                note="2mm 검정 아크릴 · 정면 앞에서 본 모습 · 아래 탭 → 윗발판 슬롯")

HANG = [(22, 198, -10, True), (35, 210, -20, True), (39, 178, 4, True),
        (-14, 232, 14, False), (37, 218, 22, False), (-36, 202, 24, False), (44, 162, 16, False)]

def p_charms():
    res = []
    stars = [h for h in HANG if h[3]]
    moons = [h for h in HANG if not h[3]]
    res.append(part("HS", "매달 별", 8.4, 8.4, len(stars), [star(4.2, 4.2, 4, 4.2, 1.3)], [], [],
                    note="2mm 유백 아크릴(또는 금색 종이). 실은 뒷면 윗 뾰족 끝에 접착"))
    cres = crescent(3.264, 3.264, 3.264, 2.73, 1.5, -14.3)
    res.append(part("HM", "매달 달", 6.6, 6.6, len(moons), [cres, circle(2.2, 2.2, 0.4)], [], [],
                    note="2mm 유백 아크릴 · 실 구멍 Ø0.8"))
    return res

def sprout(s):
    R1_, R2_, d_ = 2.856 * s, 2.389 * s, 1.3125 * s
    outer, inner = crescent_pts(R1_, R2_, d_, n=48)
    ca, sa = math.cos(0.25), math.sin(0.25)
    cx, cy = 1.0 * s, 13.8 * s
    def T(p): return (cx + p[0] * ca - p[1] * sa, cy + p[0] * sa + p[1] * ca)
    o = [T(p) for p in outer]
    ii = [T(p) for p in inner]
    ybot = 8.2 * s - 3.0
    idx = [i for i, p in enumerate(o) if -0.8 <= p[0] <= 0.8 and p[1] < cy - 0.5]
    if idx:
        i0, i1 = idx[0], idx[-1]
        o = o[:i0] + [(-0.8, o[i0][1]), (-0.8, ybot), (0.8, ybot), (0.8, o[i1][1])] + o[i1 + 1:]
    pts = o + ii
    minx = min(p[0] for p in pts); maxy = max(p[1] for p in pts)
    maxx = max(p[0] for p in pts); miny = min(p[1] for p in pts)
    return [(p[0] - minx, maxy - p[1]) for p in pts], maxx - minx, maxy - miny

def p_sprouts():
    res = []
    for name, s in (("SP1", 1.0), ("SP2", 0.85)):
        pts, w, h = sprout(s)
        res.append(part(name, "달 새싹 %s (화분 %s)" % (name[-1], name[-1]), w, h, 1, [poly(pts)], [], [],
                        note="2mm 유백 아크릴 · 아래 줄기(탭)를 화분 가운데층 홈에 꽂음"))
    return res
