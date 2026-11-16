# -*- coding: utf-8 -*-
from gen_parts2 import *
import shutil

OUTDIR = OUT
SRC_TOL = r"D:/k-뉴딜 아카데미/side project_booknook/달수확농장 시제품_SVG/01_공차시험조각.svg"
FILES = {}

def flatten(*xs):
    out = []
    for x in xs:
        if isinstance(x, list):
            out += flatten(*x)
        else:
            out.append(x)
    return out

# ---- 02 합판 3mm 외장판
sh = build_sheet(os.path.join(OUTDIR, "02_합판3mm_외장판.svg"), "합판 3mm 외장판 (S1~S7)",
    "단위 mm, 1:1. 빨강=절단, 파랑=선 각인, 검정=면 각인(바깥면), 보라=면 각인(안쪽면, 판을 뒤집어서), 회색=참고(가공 제외). "
    "핑거: 폭 10, 간격 20, 7개, 옆판 홈 깊이 3+0.15. 3D-view.html 기준(폭 120×높이 250×깊이 147).",
    flatten(p_S1(), p_S2(), p_S3(), p_S4(HANG), p_S5(), p_S6(), p_S7()),
    notes=["3mm 합판(자작 권장) · 외형 120×250×147 = 옆판 깊이 144 + 앞판 3. 레이저 절단 폭(커프) 보정은 적용하지 않음 — 01_공차시험조각 결과로 조정.",
           "S2는 판 하나의 바깥면(검정)과 안쪽면(보라) 그림을 따로 그렸어요. 보라 'S2안쪽'은 새로 자르는 판이 아니라, S2를 뒤집어 안쪽이 위로 오게 놓고 새기는 그림(앞쪽이 왼쪽)이에요. S3: 바깥면 각인(앞쪽이 왼쪽).",
           "S4 위 구멍 C1~C7은 천장에서 매다는 실이 통과하는 자리(평면도: 위=뒤쪽, 오른쪽=3D 오른쪽). S7은 정면(앞쪽)을 보는 면에 별 55개 각인."])
FILES["02"] = sh

# ---- 03 합판 3mm 달 조명상자
ml = p_moon_layers()
sh = build_sheet(os.path.join(OUTDIR, "03_합판3mm_달_조명상자.svg"), "합판 3mm 달 조명상자 (M1, M2×4, 지지대 B×2)",
    "단위 mm, 1:1. 달 = 합판 5겹(15mm) + 앞면 유백 아크릴 3mm(=3D 몸통 15 + 앞판 3). 3D에서 달 전체를 z축 둘레로 0.26rad(14.9°) 기울여 설치.",
    ml + [p_bars()],
    notes=["M1(뒤판)의 지지대 구멍 2개는 달 로컬 (-18,±10) 위치이며 달의 기울기 0.26rad을 반대로 돌려 전역 수평으로 맞춤.",
           "M2 링 4장 = 가운데 빈 공간(안쪽 초승달) → LED/COB 설치 공간. 쌓는 순서: M1 → M2×4 → 앞판(08번 유백 아크릴).",
           "달 지지대 B 2개: 한쪽 탭 → M1 구멍, 다른 쪽 탭 → 속판 S7 슬롯(B1, B2). 달 중심 3D 좌표 (-16, 184, -8)."])
FILES["03"] = sh

# ---- 04 합판 3mm 덩굴 줄기
vpanels = []
vmeta = {}
for v in vine_defs():
    p, meta = build_vine_panel(v)
    vpanels.append(p); vmeta[v["id"]] = meta
sh = build_sheet(os.path.join(OUTDIR, "04_합판3mm_덩굴줄기.svg"), "합판 3mm 덩굴 줄기 3겹 (VA, VB, VC)",
    "단위 mm, 1:1. 정면에서 본 모습. 줄기 폭 3.4, 두께 3(앞뒤). 위·아래 탭이 아닌 아래 탭만 바닥판 슬롯에 꽂음. 파랑 표시 = 잎(선)·꽃(원)·별(마름모) 붙일 자리.",
    vpanels,
    notes=["VA: 앞(z=40) · VB: 가운데(z=13) · VC: 뒤(z=-18). VA·VB는 왼쪽 줄기가 아치 윗부분까지 이어져 오른쪽 스프링라인(y=189.5)에서 끝남.",
           "잎·꽃·별은 11번 종이 장식 시트. 3D에서 줄기는 공중에 떠 있어 줄기 폭 1.7 → 3.4, 줄기 x를 호 끝에 맞춤(VA -51→-48.5, VB -54→-46, 3D도 같은 값으로 수정). VB는 y>189.5 위의 잎 3·별 1은 아치 호와 겹쳐 생략(3D 대비)."])
FILES["04"] = sh

# ---- 05 합판 3mm 소품
parts05 = flatten(p_brackets(), p_basket(), p_can(), p_pots(), p_lantern(), p_corks())
sh = build_sheet(os.path.join(OUTDIR, "05_합판3mm_소품.svg"), "합판 3mm 소품 (선반받침, 바구니, 물뿌리개, 화분, 랜턴, 병마개)",
    "단위 mm, 1:1. 모두 3mm 합판. 3D의 입체 소품을 평면 층 겹침으로 단순화.",
    parts05,
    notes=["바구니 5층(밑→위 BK1~BK5) 접착 = 높이 15. 맨 윗층 BK5의 파랑 원 22개 = 꽃(종이 Ø6.8) 자리, 숫자 = 순서(11번 시트 색 지정).",
           "물뿌리개 4장 겹침(12mm). 화분 = 앞·뒤층(a) 사이에 가운데층(b, 새싹 홈) 끼움 = 9mm(스케일 0.85 화분은 약간 두꺼움).",
           "랜턴: 앞(LF)+가운데(LM)+뒤(LB 유백 아크릴) = 9mm. 지붕은 검정 도색. 선반 받침 6개는 선반 아래 접착(좌 x=-46, 우 x=-24)."])
FILES["05"] = sh

# ---- 06 합판 4mm 바닥·선반
sh = build_sheet(os.path.join(OUTDIR, "06_합판4mm_바닥_기둥_선반.svg"), "합판 4mm 바닥판·선반 기둥·선반 3개",
    "단위 mm, 1:1. 바닥판은 평면도(뒤=위). 슬롯 위치는 3D 좌표에서 환산(u=x+57, v=z+70.5).",
    [p_floor(), p_pillar(), p_shelf()],
    notes=["바닥판 슬롯: 기둥 1, 울타리 말뚝 6, 사다리 발 4(18.3° 기울임), 덩굴 3, 모종삽 1. 파랑 점 = 풀잎(45)·작은 꽃(15) 종이 붙일 자리.",
           "선반: 윗면 y=49.75 / 87.75 / 125.75. 기둥은 왼쪽 옆판 안쪽면에서 0.75 떨어진 위치(x=-54)에 세우고 벽에 접착."])
FILES["06"] = sh

# ---- 07 합판 2mm
parts07 = flatten(p_fence(), p_ladder_front(), p_rungcaps(), p_ladder_back(), p_ladder_step(), p_trowel(), p_shoes())
sh = build_sheet(os.path.join(OUTDIR, "07_합판2mm_울타리_사다리_모종삽_신발.svg"), "합판 2mm 울타리·사다리·모종삽·신발",
    "단위 mm, 1:1. 사다리 = 앞 다리판(LD1) + 발판 덧댐 9(LD2) + 뒤 다리판(LD3) + 윗발판(LD4). 앞·뒤 다리판은 각각 ±0.13rad 기울여 A자.",
    parts07,
    notes=["사다리 조립: LD1 앞면에 LD2 9개를 접착(발판 깊이 2+2=4) → LD1·LD3 윗탭을 LD4 양끝 슬롯에 함께 끼움 → 아래 탭을 바닥 슬롯에 끼움(사다리 전체를 18.3° 돌려 설치).",
           "LD4의 기울어진 슬롯에 아이 실루엣(CH) 발 탭을 꽂음. 신발은 4장(=한 켤레)을 2장씩 접착해 바구니 오른쪽 앞 바닥에 놓음."])
FILES["07"] = sh

# ---- 08 아크릴 3mm
parts08 = flatten(p_opal_moon(), p_jar_discs(), p_lantern_back())
sh = build_sheet(os.path.join(OUTDIR, "08_아크릴3mm_유백달_투명병_랜턴창.svg"), "아크릴 3mm (유백 달 앞판, 투명 병 디스크, 랜턴 뒷층)",
    "단위 mm, 1:1. 달 앞판·랜턴 뒷층 = 유백(우윳빛) 아크릴, 병 디스크 = 투명 아크릴.",
    parts08,
    notes=["병 1개 = 투명 디스크 5장 접착(가운데 한 장은 초승달 각인) + 병마개(05번 합판 Ø8.6) 1장 = 높이 18.",
           "달 앞판은 03번 달 링 4장 위에 접착. 크레이터 6개는 면 각인(좌표는 달 로컬)."])
FILES["08"] = sh

# ---- 09 아크릴 2mm 검정 실루엣
sh = build_sheet(os.path.join(OUTDIR, "09_아크릴2mm_검정_아이실루엣.svg"), "아크릴 2mm 검정 아이 실루엣",
    "단위 mm, 1:1. 정면에서 본 모습. 3D의 폴리곤 좌표 그대로. 아래 탭(폭 5×길이 3)이 사다리 윗발판 슬롯에 꽂힘.",
    [p_child()],
    notes=["설치 위치: 3D 좌표에서 실루엣 발 변(탭 위)이 x=26.2~35.2, y=111, z=12~14. 손끝과 달 앞판 사이 틈이 이 장면의 핵심 — 설치 후 틈을 확인."])
FILES["09"] = sh

# ---- 10 아크릴 2mm 유백 별·달·새싹
sh = build_sheet(os.path.join(OUTDIR, "10_아크릴2mm_유백_별_달_새싹.svg"), "아크릴 2mm 유백 (매달 별 3, 매달 달 4, 달 새싹 2)",
    "단위 mm, 1:1. 3D의 hangingCoords 7개와 화분 새싹 2개.", flatten(p_charms(), p_sprouts()),
    notes=["매달 장식 3D 좌표(x, y, z, 종류): " + "; ".join("C%d (%s, %s, %s, %s)" % (i + 1, f(h[0]), f(h[1]), f(h[2]), "별" if h[3] else "달") for i, h in enumerate(HANG)),
           "실 길이 = 246 - y (바닥 기준): " + ", ".join("C%d %s" % (i + 1, f(246 - h[1])) for i, h in enumerate(HANG)) + " mm. 실 위쪽은 S4 구멍 C1~C7 위로 올려 고정."])
FILES["10"] = sh

# ---- 11 종이 장식
def leaf_diamond():
    return poly([(0, 2.5), (3.6, 5), (7.4, 2.5), (3.6, 0)])

flower_colors = ["분홍(#F48FB1)", "살구(#FFAB91)", "크림(#FFF3A1)", "흰색(유백)"]
vine_c = [0, 0, 0]; arch_c = [0, 0, 0]
# 스택 줄기 꽃
for v in vine_defs():
    L = v["layer"]; y = L["ymin"]
    while y <= L["ymax"] + 1e-9:
        if (y + v["idx"] * 7) % 2 == 0:
            vine_c[(y + v["idx"]) % 3] += 1
        y += L["step"]
    if v["arch"]:
        A = v["arch"]
        for i in range(A["count"] + 1):
            if i % 3 == A["aIdx"]:
                arch_c[(i + A["aIdx"]) % 3] += 1
tot_c = [vine_c[i] + arch_c[i] for i in range(3)]
bask_c = [0, 0, 0]
for i in range(22):
    bask_c[i % 3] += 1
floor_c = [0, 0, 0, 0]
for i in range(45):
    if i % 3 == 0:
        floor_c[i % 4] += 1
leaves = sum(m["leaf"] for m in vmeta.values())
stars_v = sum(m["star"] for m in vmeta.values())

paper = [part("LF", "잎 (연두 종이)", 7.4, 5, leaves, [leaf_diamond()], [], [], note="길이 7.4 × 폭 5")]
for i, nm in enumerate(["분홍", "살구", "크림"]):
    if tot_c[i]:
        paper.append(part("FV%d" % (i + 1), "덩굴·아치 꽃 %s Ø6" % nm, 6, 6, tot_c[i], [circle(3, 3, 3)], [], [], note="중심 Ø1.9 갈색 점은 펜으로"))
for i, nm in enumerate(["분홍", "살구", "크림"]):
    if bask_c[i]:
        paper.append(part("FB%d" % (i + 1), "바구니 꽃 %s Ø6.8" % nm, 6.8, 6.8, bask_c[i], [circle(3.4, 3.4, 3.4)], [], [], note="중심 Ø2.3 갈색 점"))
for i, nm in enumerate(["분홍", "살구", "크림", "흰색"]):
    if floor_c[i]:
        paper.append(part("FF%d" % (i + 1), "바닥 작은 꽃 %s Ø3.2" % nm, 3.2, 3.2, floor_c[i], [circle(1.6, 1.6, 1.6)], [], [], note=""))
paper.append(part("GS", "덩굴 별(금색 종이)", 5, 5, stars_v, [star(2.5, 2.5, 4, 2.5, 0.75)], [], [], note="바깥반지름 2.5"))
paper.append(part("GR", "풀잎 (진초록 종이)", 2.4, 4.2, 45, [poly([(1.2, 0), (2.4, 4.2), (0, 4.2)])], [], [], note="폭 2.4 × 높이 4.2, 바닥판 파랑 점 위에 세워 접착"))
sh = build_sheet(os.path.join(OUTDIR, "11_종이_잎_꽃_별_풀.svg"), "종이 장식 (잎, 꽃, 별, 풀잎)",
    "단위 mm, 1:1. 종이/얇은 보드 절단선만 있음(빨강). 개수는 3D-view.html 코드의 반복문에서 계산.",
    paper,
    maxw=300,
    notes=["덩굴 줄기 위 위치는 04번 파랑 표시: 선=잎, 원=꽃, 마름모=별. 아치 호 위 잎은 호의 바깥쪽 방향으로 붙임.",
           "개수: 잎 %d, 덩굴·아치 꽃 %d (분홍 %d·살구 %d·크림 %d), 덩굴 별 %d, 바구니 꽃 22, 바닥 꽃 15, 풀잎 45." % (leaves, sum(tot_c), tot_c[0], tot_c[1], tot_c[2], stars_v)])
FILES["11"] = sh

# ---- 01 공차 시험 조각 (기존 파일 재사용)
dst01 = os.path.join(OUTDIR, "01_공차시험조각.svg")
if os.path.exists(SRC_TOL):
    shutil.copyfile(SRC_TOL, dst01)   # 이미 있으면 그대로 두고, 원본이 없어도 오류 없이 진행

for k, v in FILES.items():
    print(k, os.path.basename(v["path"]), "%.0fx%.0f" % (v["w"], v["h"]), v["n"], "pieces")
print("flowers", tot_c, bask_c, floor_c, "leaves", leaves, "stars", stars_v)
print("bar positions", moon_bar_positions())
print("floor slots", [(n, round(u, 2), round(v, 2)) for (n, u, v, a, b, d) in floor_slots()])
