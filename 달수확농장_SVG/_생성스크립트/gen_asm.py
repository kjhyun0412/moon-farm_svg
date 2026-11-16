# -*- coding: utf-8 -*-
from gen_parts2 import *

MARGIN = 14
TITLE_H = 18
GAPX = 22

def T(txt, x, y, fs=2.6, fill="#444", anchor="start", extra=""):
    return '<text x="%s" y="%s" font-size="%s" fill="%s" text-anchor="%s"%s>%s</text>' % (f(x), f(y), fs, fill, anchor, extra, txt)

def Pth(d, stroke="#222", fill="none", sw=0.3, extra=""):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (d, fill, stroke, sw, extra)

class View:
    """영역 좌표(mm) → 시트 좌표. fx, fy: 전역 좌표를 뷰 좌표로 바꾸는 함수"""
    def __init__(self, ox, oy, w, h, title, fx, fy):
        self.ox, self.oy, self.w, self.h, self.title, self.fx, self.fy = ox, oy, w, h, title, fx, fy
        self.items = []
    def P(self, gx, gy):
        return self.ox + self.fx(gx, gy), self.oy + self.fy(gx, gy)
    def add(self, s):
        self.items.append(s)

# ---------- 평면도: 가로 = x, 세로 = z (뒤쪽 = 위) ----------
def plan_view(ox, oy):
    v = View(ox, oy, 120, 147, "평면도 (위에서 본 모습, 위=뒤쪽)", lambda x, z: x + 60, lambda x, z: z + 73.5)
    p = lambda x, z: v.P(x, z)
    a = v.add
    x0, y0 = p(-60, -73.5)
    a(Pth(rect(x0, y0, 120, 147), "#c9a24a", "#f4efe0", 0.4))                      # 바깥 외곽
    a(Pth(rect(*p(-57, -70.5), 114, 141), "#999", "#fff", 0.2, ' stroke-dasharray="1 1"'))   # 바닥판 영역
    a(Pth(rect(*p(-60, -73.5), 3, 144), "#16215a", "#16215a", 0.2))                 # S2
    a(Pth(rect(*p(57, -73.5), 3, 144), "#16215a", "#16215a", 0.2))                  # S3
    a(Pth(rect(*p(-60, 70.5), 120, 3), "#16215a", "#16215a", 0.2))                  # S1
    a(Pth(rect(*p(-57, -73.5), 114, 3), "#16215a", "#16215a", 0.2))                 # S6
    a(Pth(rect(*p(-57, -70.2), 114, 3), "#5b6fb4", "#dfe6ff", 0.2))                 # S7 (z -70.2~-67.2)
    # 달 지지대 (평면에서 선)
    for i, (gx, gy, lx, ly) in enumerate(moon_bar_positions()):
        (xa, ya), (xb, yb) = p(gx, -67.2), p(gx, -8)
        a(Pth(poly([(xa, ya), (xb, yb)], False), "#d98c00", "none", 0.8))
        a(T("B%d" % (i + 1), xa + 1, ya + 12 + 6 * i, 2.6, "#b36b00"))
    # 달
    cxm, cym = p(-16, -8 + 7.5)
    a(Pth(ellipse(cxm, cym, 4.5, 8.5), "#d98c00", "#ffe6a3", 0.4)); a(T("달(M)", cxm + 6, cym, 2.4, "#b36b00"))
    # 기둥, 선반
    a(Pth(rect(*p(-56.25, -48.5), 4.5, 25), "#7d4f27", "#d6a064", 0.3)); a(T("PL", *p(-60.5, -50), 2.4))
    for k in range(3):
        a(Pth(rect(*p(-51.75, -49), 36.25, 26), "#7d4f27", "none", 0.2, ' stroke-dasharray="1 1"'))
    a(T("SH×3", *p(-45, -20), 2.4))
    # 덩굴 줄기
    for nm, vx, vz in (("VA", -48.5, 40), ("VB", -46.0, 13), ("VC", -55, -18)):
        a(Pth(rect(*p(vx - 1.7, vz - 1.5), 3.4, 3), "#2e7d32", "#9ccc65", 0.3)); a(T(nm, *p(vx + 2.5, vz + 1), 2.4, "#2e7d32"))
    a(Pth(poly([p(-48.5, 40), p(48.5, 40)], False), "#2e7d32", "none", 0.5, ' stroke-dasharray="2 1"'))
    a(Pth(poly([p(-46, 13), p(46, 13)], False), "#2e7d32", "none", 0.5, ' stroke-dasharray="2 1"'))
    # 울타리
    a(Pth(rect(*p(-51.8, 45), 59.6, 2), "#999", "#eee", 0.2)); a(T("FR/FP", *p(-52, 43), 2.4))
    for xcn in PICKET_X:
        a(Pth(rect(*p(xcn - 3.3, 47), 6.6, 2), "#bbb", "#fff", 0.2))
    # 사다리
    def lad(xl, zl):
        gx, gz = ladder_to_global(xl, zl); return p(gx, gz)
    feet = [lad(-FRONT_X, FOOT_ZL), lad(FRONT_X, FOOT_ZL), lad(BACK_X, -FOOT_ZL), lad(-BACK_X, -FOOT_ZL)]
    a(Pth(poly(feet), "#b98450", "#f3dcc0", 0.4, ' fill-opacity="0.7"'))
    stepc = [lad(-12, -7), lad(12, -7), lad(12, 7), lad(-12, 7)]
    a(Pth(poly(stepc), "#8a5a2b", "#e6c9a3", 0.4)); a(T("LD1·LD3·LD4", *p(18, 34), 2.4, "#8a5a2b"))
    a(Pth(rrect(*p(25 + 5.7, 12 + 1.0), 5, 2, math.degrees(-0.0)), "#111", "#111", 0.2)); a(T("CH", *p(36, 14), 2.4))
    # 바구니, 물뿌리개, 모종삽, 신발
    a(Pth(ellipse(*p(22, 46), 15, 9.5), "#7d4f27", "#d6a064", 0.4)); a(T("BK", *p(18, 47), 2.6))
    a(Pth(circle(*p(-34, 55), 6.2), "#777", "#ccc", 0.3)); a(T("CAN", *p(-38, 56), 2.4))
    a(Pth(circle(*p(-8, 55), 1.4), "#777", "#ccc", 0.3)); a(T("TR", *p(-9, 59), 2.4))
    for (sx, sz, rr) in ((26, 60, -0.2), (33.5, 61, 0.1)):
        a(Pth(rrect(*p(sx, sz), 4.6, 10.4, math.degrees(rr)), "#a0522d", "#e9a07a", 0.3))
    a(T("SZ", *p(24, 69), 2.4))
    # 매달 장식 위치 (천장 구멍)
    for i, (hx, hy, hz, st) in enumerate(HANG):
        a(Pth(circle(*p(hx, hz), 1.0), "#c00", "#fff", 0.3)); a(T("C%d" % (i + 1), p(hx, hz)[0] + 1.5, p(hx, hz)[1] - 1, 2.2, "#c00"))
    # 치수
    a(T("x=-60", ox, oy - 2, 2.2)); a(T("x=+60", ox + 120, oy - 2, 2.2, anchor="end"))
    a(T("z=-73.5 (뒤)", ox - 2, oy + 3, 2.2, anchor="end")); a(T("z=+73.5 (앞)", ox - 2, oy + 147, 2.2, anchor="end"))
    return v

# ---------- 정면도: 가로 = x, 세로 = y (위쪽 = +y) ----------
def front_view(ox, oy):
    v = View(ox, oy, 120, 250, "정면도 (앞에서 본 모습)", lambda x, y: x + 60, lambda x, y: 250 - y)
    p = lambda x, y: v.P(x, y)
    a = v.add
    a(Pth(rect(ox, oy, 120, 250), "#c9a24a", "#101a4a", 0.4))
    a(Pth(rect(*p(-57, 247), 114, 244 - 244 + 0.01), "#fff", "none", 0.1))
    # 아치 구멍
    cx, r = 60.0, 52.1
    a(Pth("M%s %s V%s A%s %s 0 0 1 %s %s V%s Z" % (f(ox + cx - r), f(oy + 243.6), f(oy + 60.5), f(r), f(r), f(ox + cx + r), f(oy + 60.5), f(oy + 243.6)), "#c9a24a", "#2a3466", 0.4))
    # 속판 별 느낌(생략), 달 (기울어진 초승달)
    outer, inner = crescent_pts(R1, R2, DD, 36)
    pts = []
    for (qx, qy) in outer + inner:
        xr = qx * math.cos(0.26) - qy * math.sin(0.26); yr = qx * math.sin(0.26) + qy * math.cos(0.26)
        pts.append(p(-16 + xr, 184 + yr))
    a(Pth(poly(pts), "#d98c00", "#ffe6a3", 0.4)); a(T("달 M·MF", *p(-12, 150), 2.6, "#ffe6a3"))
    for i, (gx, gy, lx, ly) in enumerate(moon_bar_positions()):
        a(Pth(circle(*p(gx, gy), 1.6), "#ff9800", "#ff9800", 0.2)); a(T("B%d" % (i + 1), p(gx, gy)[0] - 6, p(gx, gy)[1] + 1, 2.4, "#ffb74d"))
    # 아이 실루엣
    cp = [p(25 + (px - 76), 111 + (139.2 - py)) for (px, py) in CHILD_PTS]
    a(Pth(poly(cp), "#f4c95d", "#000", 0.3)); a(T("CH", *p(40, 150), 2.6, "#f4c95d"))
    # 선반, 기둥, 병 등
    a(Pth(rect(*p(-56.25, 159), 4.5, 152), "#7d4f27", "#d6a064", 0.3)); a(T("PL", *p(-62, 100), 2.4, "#d6a064"))
    for sy in SHELF_Y:
        top = sy + 2
        a(Pth(rect(*p(-51.75, top), 36.25, 4), "#7d4f27", "#d6a064", 0.3))
    a(T("SH 윗면 y=49.75/87.75/125.75", *p(-55, 20), 2.4, "#d6a064"))
    for (nm, x, y, w_, h_) in (("JAR", -43, 125.75, 11.2, 15), ("LAN", -25.5, 125.75, 10.5, 16.7), ("JAR", -36, 87.75, 11.2, 15),
                               ("PT1", -43, 49.75, 9.2, 8.2), ("PT2", -28.5, 49.75, 7.8, 7.0)):
        a(Pth(rect(*p(x - w_ / 2, y + h_), w_, h_), "#bbb", "#e9e6d8", 0.3)); a(T(nm, *p(x - 4, y + h_ + 2), 2.2, "#ddd"))
    # 덩굴 줄기 세로 + 호
    for nm, vx, R_ in (("VA", -48.5, 48.5), ("VB", -46.0, 46.0), ("VC", -55, None)):
        top = 189.5 if R_ else 222
        a(Pth(poly([p(vx, 7), p(vx, top)], False), "#81c784", "none", 1.0))
        if R_:
            x1, y1 = p(VC[0] - R_, VC[1]); x2, y2 = p(VC[0] + R_, VC[1])
            a(Pth("M%s %s A%s %s 0 0 1 %s %s" % (f(x1), f(y1), f(R_), f(R_), f(x2), f(y2)), "#81c784", "none", 1.0))
        a(T(nm, *p(vx - 3, 12), 2.4, "#81c784"))
    # 울타리, 바구니 등
    a(Pth(rect(*p(-51.8, 29.6), 59.6, 4.2), "#eee", "#eee", 0.2)); a(Pth(rect(*p(-51.8, 16.6), 59.6, 4.2), "#eee", "#eee", 0.2))
    for xc in PICKET_X:
        a(Pth(poly([p(xc - 3.3, 36.4 - 4.5), p(xc, 36.4), p(xc + 3.3, 36.4 - 4.5), p(xc + 3.3, 7), p(xc - 3.3, 7)]), "#bbb", "#f5f5f5", 0.2))
    a(T("FR·FP", *p(-52, 40), 2.4, "#eee"))
    a(Pth(rect(*p(7, 23), 30, 16), "#7d4f27", "#d6a064", 0.3)); a(T("BK", *p(18, 12), 2.4, "#d6a064"))
    a(Pth(rect(*p(-40, 18.9), 12.8, 11.9), "#777", "#ccc", 0.3)); a(T("CAN", *p(-38, 13), 2.4, "#ddd"))
    a(Pth(rect(*p(-9.5, 25), 3, 18), "#777", "#ccc", 0.3)); a(T("TR", *p(-9, 29), 2.4, "#ddd"))
    for sx in (26, 33.5):
        a(Pth(rect(*p(sx - 2.3, 11.1), 4.6, 4.1), "#a0522d", "#e9a07a", 0.3))
    # 사다리 (정면에서 보면 4개 다리 선)
    for nm, xl, zl_foot, zl_top in (("앞L", -FRONT_X, FOOT_ZL, 1.0), ("앞R", FRONT_X, FOOT_ZL, 1.0), ("뒤L", -BACK_X, -FOOT_ZL, -1.0), ("뒤R", BACK_X, -FOOT_ZL, -1.0)):
        gx1, _ = ladder_to_global(xl, zl_foot); gx2, _ = ladder_to_global(xl, zl_top)
        a(Pth(poly([p(gx1, 7), p(gx2, 111)], False), "#b98450", "none", 0.8))
    a(T("LD", *p(36, 70), 2.6, "#b98450"))
    # 천장에서 매다는 실
    for i, (hx, hy, hz, st) in enumerate(HANG):
        a(Pth(poly([p(hx, 247), p(hx, hy)], False), "#e0c870", "none", 0.2))
        a(Pth(circle(*p(hx, hy), 1.8), "#f4c95d", "#f4c95d", 0.2)); a(T("C%d" % (i + 1), p(hx, hy)[0] + 2.2, p(hx, hy)[1] + 1, 2.2, "#f4c95d"))
    return v

# ---------- 좌측면도: 가로 = z + 73.5 (뒤쪽이 왼쪽, 앞쪽이 오른쪽), 세로 = y ----------
def side_view(ox, oy):
    v = View(ox, oy, 147, 250, "좌측면도 (왼쪽 밖에서 본 모습, 앞=오른쪽)", lambda z, y: z + 73.5, lambda z, y: 250 - y)
    p = lambda z, y: v.P(z, y)
    a = v.add
    a(Pth(rect(ox, oy, 147, 250), "#c9a24a", "#101a4a", 0.4))
    a(Pth(rect(*p(70.5, 250), 3, 250), "#16215a", "#16215a", 0.2)); a(T("S1", *p(71, 20), 2.4, "#aab"))
    a(Pth(rect(*p(-73.5, 247), 3, 244), "#16215a", "#2a3466", 0.2)); a(T("S6", *p(-73, 20), 2.4, "#aab"))
    a(Pth(rect(*p(-70.2, 244.5), 3, 241), "#5b6fb4", "#2a3466", 0.2)); a(T("S7", *p(-69, 30), 2.4, "#aab"))
    a(Pth(rect(*p(-70.5, FLOOR_TOP), 141, 4), "#2e5d2a", "#3d6b36", 0.2)); a(T("S9 바닥(4mm)", *p(-30, 4.5), 2.4, "#cfe"))
    a(Pth(rect(*p(-70.5, 3), 141, 3), "#16215a", "#16215a", 0.2))
    # 달 (두께 18: z -8~10)
    a(Pth(rect(*p(-8, 184 + 27), 15, 54), "#7d4f27", "#d6a064", 0.3)); a(Pth(rect(*p(7, 184 + 27), 3, 54), "#d98c00", "#ffe6a3", 0.3))
    a(T("달 M1~M2×4 + MF", *p(-34, 222), 2.6, "#ffe6a3"))
    for i, (gx, gy, lx, ly) in enumerate(moon_bar_positions()):
        a(Pth(rect(*p(-67.2, gy + 1.5), 59.2, 3), "#ff9800", "#ffcc80", 0.2)); a(T("B%d" % (i + 1), *p(-48, gy + 4), 2.4, "#ffb74d"))
    # 아이, 사다리
    a(Pth(rect(*p(12, 160), 2, 49), "#f4c95d", "#000", 0.2)); a(T("CH", *p(15, 150), 2.4, "#f4c95d"))
    # 사다리 앞/뒤 다리판: 정확한 z 는 18.3° 회전된 위치. 측면에서는 앞다리·뒤다리 선만
    for nm, xl, zf, zt in (("앞", FRONT_X, FOOT_ZL, 1.0), ("뒤", BACK_X, -FOOT_ZL, -1.0)):
        gz1 = ladder_to_global(xl, zf)[1]; gz2 = ladder_to_global(xl, zt)[1]
        a(Pth(poly([p(gz1, 7), p(gz2, 111)], False), "#b98450", "none", 1.0))
    a(Pth(rect(*p(2, 112), 20, 2), "#b98450", "#e6c9a3", 0.2)); a(T("LD4", *p(0, 116), 2.4, "#b98450"))
    # 기둥/선반
    a(Pth(rect(*p(-48.5, 159), 25, 152), "#7d4f27", "#d6a064", 0.2)); a(T("PL", *p(-44, 100), 2.4))
    for sy in SHELF_Y:
        a(Pth(rect(*p(-49, sy + 2), 26, 4), "#a56a2c", "#d6a064", 0.3))
    # 울타리/바구니/삽/신발/물뿌리개
    a(Pth(rect(*p(45, 36.4), 4, 29.4), "#bbb", "#f5f5f5", 0.3)); a(T("FP", *p(40, 40), 2.4, "#eee"))
    a(Pth(rect(*p(38, 23), 16, 16), "#7d4f27", "#d6a064", 0.3)); a(T("BK", *p(42, 14), 2.4))
    a(Pth(rect(*p(50, 11.1), 10.4, 4.1), "#a0522d", "#e9a07a", 0.3)); a(T("SZ", *p(56, 21), 2.4))
    # 덩굴 판
    for nm, vz in (("VA", 40), ("VB", 13), ("VC", -18)):
        a(Pth(rect(*p(vz - 1.5, 222 if nm == "VC" else 239.7), 3, 215 if nm == "VC" else 232.7), "#81c784", "#81c784", 0.2)); a(T(nm, *p(vz - 3, 26), 2.4, "#81c784"))
    # 매다는 실
    for i, (hx, hy, hz, st) in enumerate(HANG):
        a(Pth(poly([p(hz, 247), p(hz, hy)], False), "#e0c870", "none", 0.2)); a(Pth(circle(*p(hz, hy), 1.5), "#f4c95d", "#f4c95d", 0.2))
        a(T("C%d" % (i + 1), p(hz, hy)[0] + 2, p(hz, hy)[1] + 1, 2.2, "#f4c95d"))
    a(T("z=-73.5 (뒤)", ox, oy - 2, 2.2)); a(T("z=+73.5 (앞)", ox + 147, oy - 2, 2.2, anchor="end"))
    return v

def build_asm(path):
    pv = plan_view(MARGIN, MARGIN + TITLE_H)
    fv = front_view(MARGIN + 120 + GAPX + 0, MARGIN + TITLE_H)
    sv = side_view(MARGIN + 240 + 2 * GAPX, MARGIN + TITLE_H)
    total_w = MARGIN * 2 + 120 + 120 + 147 + 2 * GAPX
    total_h = MARGIN + TITLE_H + 250 + 70
    body = '<rect x="0" y="0" width="%s" height="%s" fill="#f4efe0"/>' % (f(total_w), f(total_h))
    body += T("달을 수확하는 농장 · 조립 배치도 (1:1, mm)", MARGIN, MARGIN, 5, "#222", extra=' font-weight="bold"')
    body += T("좌표계: x = 오른쪽, y = 위(바닥=0), z = 앞쪽(관람자 쪽). 원점 = 바닥 중앙. 실제 가공용이 아니라 위치 참고용 도면.", MARGIN, MARGIN + 6, 2.8)
    for v in (pv, fv, sv):
        body += T(v.title, v.ox, v.oy - 4, 3.4, "#222", extra=' font-weight="bold"')
        body += "".join(v.items)
    ly = MARGIN + TITLE_H + 250 + 8
    legend = ["S1~S7 외장판 · M 달(M1,M2×4,MF) · B 달 지지대 · PL 선반 기둥 · SH 선반 · S9 바닥 · VA/VB/VC 덩굴 줄기 · FR/FP 울타리 가로대/말뚝",
              "LD1 사다리 앞 다리판 · LD2 발판 덧댐 · LD3 뒤 다리판 · LD4 윗발판 · CH 아이 실루엣 · BK 바구니 · CAN 물뿌리개 · TR 모종삽 · SZ 신발",
              "JAR 병 · LAN 랜턴 · PT1/PT2 화분(+새싹 SP1/SP2) · C1~C7 매다는 별·달(실은 천장 S4 구멍에서 내려옴)",
              "사다리는 평면도에서 18.3°(0.32rad) 돌려서 설치. 달은 정면도에서 14.9°(0.26rad) 반시계 방향으로 기울여 설치."]
    for i, t in enumerate(legend):
        body += T(t, MARGIN, ly + 5 * i, 2.8)
    svg = ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="%smm" height="%smm" viewBox="0 0 %s %s" font-family="sans-serif">\n'
           '<title>조립 배치도</title>\n<desc>3D-view.html 좌표를 평면도·정면도·좌측면도로 정리한 위치 참고용 도면. 가공 파일 아님.</desc>\n%s\n</svg>\n') % (
        f(total_w), f(total_h), f(total_w), f(total_h), body)
    open(path, "w", encoding="utf-8").write(svg)

build_asm(os.path.join(OUT, "00_조립배치도.svg"))
print("asm ok")
