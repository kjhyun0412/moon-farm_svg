# -*- coding: utf-8 -*-
"""달수확농장 레이저 커팅 SVG 생성 라이브러리 (단위 mm, SVG y축은 아래쪽이 +)"""
import math

# ---------- 숫자/경로 도우미 ----------
def f(v):
    s = ("%.3f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s

def poly(pts, close=True):
    d = "M" + " L".join("%s %s" % (f(x), f(y)) for x, y in pts)
    return d + ("Z" if close else "")

def rect(x, y, w, h):
    return poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])

def circle(cx, cy, r):
    return "M%s %s A%s %s 0 1 0 %s %s A%s %s 0 1 0 %s %s Z" % (
        f(cx - r), f(cy), f(r), f(r), f(cx + r), f(cy), f(r), f(r), f(cx - r), f(cy))

def ellipse(cx, cy, rx, ry):
    return "M%s %s A%s %s 0 1 0 %s %s A%s %s 0 1 0 %s %s Z" % (
        f(cx - rx), f(cy), f(rx), f(ry), f(cx + rx), f(cy), f(rx), f(ry), f(cx - rx), f(cy))

def rot_pt(p, c, deg):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))

def rrect(cx, cy, long_, short_, deg=0):
    """중심(cx,cy), 긴 변 long_, 짧은 변 short_ 를 deg(SVG 시계방향 +) 만큼 돌린 사각형"""
    pts = [(cx - long_ / 2, cy - short_ / 2), (cx + long_ / 2, cy - short_ / 2),
           (cx + long_ / 2, cy + short_ / 2), (cx - long_ / 2, cy + short_ / 2)]
    return poly([rot_pt(p, (cx, cy), deg) for p in pts])

def star(cx, cy, n, R, r, start=-90):
    pts = []
    for i in range(2 * n):
        rad = R if i % 2 == 0 else r
        a = math.radians(start + i * 180.0 / n)
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return poly(pts)

def sparkle(cx, cy, rx, ry, k=0.22):
    return poly([(cx, cy - ry), (cx + k * rx, cy - k * ry), (cx + rx, cy), (cx + k * rx, cy + k * ry),
                 (cx, cy + ry), (cx - k * rx, cy + k * ry), (cx - rx, cy), (cx - k * rx, cy - k * ry)])

def crescent_geom(R1, R2, d):
    a = (R1 * R1 - R2 * R2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, R1 * R1 - a * a))
    return a, h

def crescent(cx, cy, R1, R2, d, ang=0.0):
    """초승달. 바깥원 중심 (cx,cy) 반지름 R1, 안쪽원 중심 (cx+d,cy) 반지름 R2, 열린 쪽은 +x.
    ang: SVG 시계방향 +(도)"""
    a, h = crescent_geom(R1, R2, d)
    top = rot_pt((cx + a, cy - h), (cx, cy), ang)
    bot = rot_pt((cx + a, cy + h), (cx, cy), ang)
    out_large = 1 if a > 0 else 0
    in_large = 1 if (a - d) > 0 else 0
    return "M%s %s A%s %s 0 %d 0 %s %s A%s %s 0 %d 1 %s %s Z" % (
        f(top[0]), f(top[1]), f(R1), f(R1), out_large, f(bot[0]), f(bot[1]),
        f(R2), f(R2), in_large, f(top[0]), f(top[1]))

def crescent_pts(R1, R2, d, n=48):
    """수학 좌표(y 위쪽 +)의 초승달 외곽 점들, 바깥호 → 안쪽호 순서"""
    a, h = crescent_geom(R1, R2, d)
    t = math.atan2(h, a)
    outer = [(R1 * math.cos(t + (2 * math.pi - 2 * t) * i / n), R1 * math.sin(t + (2 * math.pi - 2 * t) * i / n))
             for i in range(n + 1)]
    t2 = math.atan2(h, a - d)  # 안쪽원 중심(d,0) 기준 각
    # 아래 끝점(각 -t2)에서 왼쪽을 거쳐 위 끝점(각 t2)으로, 안쪽원 위를 시계방향(각 감소)으로 이동
    inner = [(d + R2 * math.cos(-t2 - (2 * math.pi - 2 * t2) * i / n), R2 * math.sin(-t2 - (2 * math.pi - 2 * t2) * i / n))
             for i in range(n + 1)]
    return outer, inner

# ---------- 판 외곽 (핑거 접합) ----------
NOTCH_W = 10.0          # 핑거 폭
NOTCH_PITCH = 20.0      # 핑거 간격
FINGER_N = 7            # 핑거 개수
THK_TOP = 3.0           # 상판·바닥판 두께
NOTCH_D = THK_TOP + 0.15  # 옆판 홈 깊이 (도면집 v1.1 규칙: 3+0.15)

def finger_starts(length):
    span = (FINGER_N - 1) * NOTCH_PITCH + NOTCH_W
    s0 = (length - span) / 2.0
    return [s0 + i * NOTCH_PITCH for i in range(FINGER_N)]

def side_panel_outline(length, height):
    """옆판: 위·아래 모서리에 홈(노치). 가로=length(깊이), 세로=height"""
    pts = [(0, 0)]
    for s in finger_starts(length):
        pts += [(s, 0), (s, NOTCH_D), (s + NOTCH_W, NOTCH_D), (s + NOTCH_W, 0)]
    pts += [(length, 0), (length, height)]
    for s in reversed(finger_starts(length)):
        pts += [(s + NOTCH_W, height), (s + NOTCH_W, height - NOTCH_D), (s, height - NOTCH_D), (s, height)]
    pts += [(0, height)]
    return poly(pts)

def top_panel_outline(depth, body_w):
    """상판/바닥판(평면도): 좌우 모서리에 탭(길이10, 돌출 3). 전체 폭 = body_w + 6"""
    t = THK_TOP
    pts = [(t, 0), (t + body_w, 0)]
    for s in finger_starts(depth):
        pts += [(t + body_w, s), (t + body_w + t, s), (t + body_w + t, s + NOTCH_W), (t + body_w, s + NOTCH_W)]
    pts += [(t + body_w, depth), (t, depth)]
    for s in reversed(finger_starts(depth)):
        pts += [(t, s + NOTCH_W), (0, s + NOTCH_W), (0, s), (t, s)]
    return poly(pts)

# ---------- 시트 조립 ----------
RED, BLUE, BLACK, PURPLE, GRAY = "#ff0000", "#0000ff", "#000000", "#8000ff", "#888888"

def part(pid, name, w, h, qty=1, cut=None, score=None, eng=None, eng2=None, note="", labels=None, ref=None):
    return dict(id=pid, name=name, w=w, h=h, qty=qty, cut=cut or [], score=score or [], eng=eng or [],
                eng2=eng2 or [], note=note, labels=labels or [], ref=ref or [])

def _inst(p, k, x, y, n):
    gid = p["id"] if n == 1 else "%s_%d" % (p["id"], k + 1)
    out = {"cut": "", "score": "", "eng": "", "eng2": "", "lab": ""}
    tr = ' transform="translate(%s %s)"' % (f(x), f(y))
    if p["cut"]:
        out["cut"] = '<g id="%s"%s>%s</g>' % (gid, tr, "".join('<path d="%s"/>' % d for d in p["cut"]))
    if p["score"]:
        s = ""
        for it in p["score"]:
            d, dash = (it if isinstance(it, tuple) else (it, None))
            s += '<path d="%s"%s/>' % (d, (' stroke-dasharray="%s"' % dash) if dash else "")
        out["score"] = '<g id="%s_선각인"%s>%s</g>' % (gid, tr, s)
    if p["eng"]:
        out["eng"] = '<g id="%s_각인"%s>%s</g>' % (gid, tr, "".join('<path d="%s"/>' % d for d in p["eng"]))
    if p["eng2"]:
        e2 = ""
        for it in p["eng2"]:
            if isinstance(it, tuple):
                e2 += '<path d="%s" fill="none" stroke="#8000ff" stroke-width="0.3" stroke-dasharray="%s"/>' % it
            else:
                e2 += '<path d="%s"/>' % it
        out["eng2"] = '<g id="%s_안쪽각인"%s>%s</g>' % (gid, tr, e2)
    qtxt = "" if p["qty"] == 1 else " (%d/%d)" % (k + 1, p["qty"])
    if k > 0 and (p["qty"] >= 12 or (p["qty"] >= 3 and p["w"] < 12 and p["h"] < 12)):
        out["lab"] = ""
        return out
    lab = '<text x="%s" y="%s" font-size="2.6">%s ×%d%s · %s×%s</text>' % (
        f(x), f(y - 4.6), p["id"], p["qty"], qtxt, f(p["w"]), f(p["h"]))
    lab += '<text x="%s" y="%s" font-size="2.4">%s</text>' % (f(x), f(y - 1.6), p["name"])
    for (lx, ly, txt) in p["labels"]:
        lab += '<text x="%s" y="%s" font-size="2">%s</text>' % (f(x + lx), f(y + ly), txt)
    if p["ref"]:
        lab += '<g transform="translate(%s %s)">%s</g>' % (f(x), f(y), "".join(
            '<path d="%s" fill="none" stroke="#999999" stroke-width="0.2" stroke-dasharray="2 1.5"/>' % d for d in p["ref"]))
    out["lab"] = lab
    return out

def build_sheet(path, title, desc, parts, maxw=600.0, margin=6.0, gap=6.0, notes=None, min_h=0):
    cells = []
    for p in parts:
        for k in range(p["qty"]):
            cells.append((p, k))
    cells.sort(key=lambda c: -c[0]["h"])
    x = y = margin
    row_h = 0.0
    placed = []
    label_h = 8.0
    def est(txt, fs):
        return sum((fs * 1.0 if ord(c) > 127 else fs * 0.58) for c in txt)
    for p, k in cells:
        quiet = k > 0 and (p["qty"] >= 12 or (p["qty"] >= 3 and p["w"] < 12 and p["h"] < 12))
        lh = 1.5 if quiet else label_h
        w = p["w"] if quiet else max(p["w"], min(est(p["name"], 2.4), 75), min(est("%s ×%d (%d/%d) · %s×%s" % (p["id"], p["qty"], k + 1, p["qty"], f(p["w"]), f(p["h"])), 2.6), 75))
        h = p["h"]
        if x + w > maxw - margin and x > margin:
            x = margin
            y += row_h + gap
            row_h = 0.0
        placed.append((p, k, x, y + lh))
        x += w + (gap if not quiet else 2.5)
        row_h = max(row_h, h + lh)
    total_h = max(y + row_h, 0)
    used_w = max(px + p["w"] for p, k, px, py in placed) + margin
    sheet_w = min(maxw, max(used_w, 150.0))
    # 노트 줄바꿈 (한글 3mm / 영문 1.7mm 가정)
    note_lines = []
    for ln in (notes or []):
        cur, wcur = "", 0.0
        for ch in ln:
            cw = 3.0 if ord(ch) > 127 else 1.75
            if wcur + cw > sheet_w - 2 * margin and cur:
                note_lines.append(cur); cur, wcur = "", 0.0
            cur += ch; wcur += cw
        if cur:
            note_lines.append(cur)
    total_h += gap + 4.6 * len(note_lines) + margin
    total_h = max(total_h, min_h)
    cut = score = eng = eng2 = lab = ""
    for p, k, px, py in placed:
        o = _inst(p, k, px, py, p["qty"])
        cut += o["cut"]; score += o["score"]; eng += o["eng"]; eng2 += o["eng2"]; lab += o["lab"]
    ny = total_h - margin - 4.6 * (len(note_lines) - 1) if note_lines else 0
    for i, ln in enumerate(note_lines):
        lab += '<text x="%s" y="%s">%s</text>' % (f(margin), f(ny + 4.6 * i), ln)
    head = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            'width="%smm" height="%smm" viewBox="0 0 %s %s">\n' % (f(sheet_w), f(total_h), f(sheet_w), f(total_h)))
    head += "<title>%s</title>\n<desc>%s</desc>\n" % (title, desc)
    body = ""
    body += '<g id="CUT_절단" inkscape:groupmode="layer" inkscape:label="CUT_절단(빨강)" fill="none" stroke="%s" stroke-width="0.1" stroke-linejoin="round">%s</g>\n' % (RED, cut)
    body += '<g id="SCORE_선각인" inkscape:groupmode="layer" inkscape:label="SCORE_선각인(파랑)" fill="none" stroke="%s" stroke-width="0.1">%s</g>\n' % (BLUE, score)
    body += '<g id="ENGRAVE_면각인" inkscape:groupmode="layer" inkscape:label="ENGRAVE_면각인(검정)" fill="%s" stroke="none">%s</g>\n' % (BLACK, eng)
    if eng2:
        body += '<g id="ENGRAVE2_안쪽면각인" inkscape:groupmode="layer" inkscape:label="ENGRAVE2_안쪽면각인(보라, 판을 뒤집어서)" fill="%s" stroke="none">%s</g>\n' % (PURPLE, eng2)
    body += '<g id="LABEL_참고용" inkscape:groupmode="layer" inkscape:label="LABEL_참고용(가공 제외)" fill="%s" stroke="none" font-family="sans-serif" font-size="3">%s</g>\n' % (GRAY, lab)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(head + body + "</svg>\n")
    return dict(path=path, w=sheet_w, h=total_h, n=len(placed))
