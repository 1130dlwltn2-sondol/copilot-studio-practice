#!/usr/bin/env python3
"""개념도 3종 (PIL). 전부 '개념도, 실제 화면 아님'을 명시."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

IVORY = (250, 243, 232)
INK = (62, 44, 30)
ACCENT = (196, 110, 58)
SUB = (120, 96, 74)
CARD = (255, 252, 246)
LINE = (210, 185, 150)

def font(path, size):
    return ImageFont.truetype(path, size, index=1)

def center(d, cx, y, s, f, fill):
    bb = d.textbbox((0, 0), s, font=f)
    w = bb[2] - bb[0]
    d.text((cx - w / 2 - bb[0], y), s, font=f, fill=fill)

def left(d, x, y, s, f, fill):
    d.text((x, y), s, font=f, fill=fill)

def note(d, W, H):
    center(d, W / 2, H - 40, "개념도 (실제 화면 아님)", font(REG, 20), SUB)

# 1. 세 영역 개념도
W, H = 1000, 620
img = Image.new("RGB", (W, H), IVORY)
d = ImageDraw.Draw(img)
center(d, W / 2, 30, "앱·워크플로·에이전트 세 영역", font(BOLD, 40), INK)
boxes = [("앱", "사람이 보고 입력하는 화면", "구매 요청 입력 화면"), ("워크플로", "정해진 순서의 자동 실행", "금액 검증과 기록"), ("에이전트", "판단이 필요한 처리", "애매한 품목 분류")]
for i, (t, d1, d2) in enumerate(boxes):
    x = 40 + i * 310
    d.rounded_rectangle([x, 120, x + 280, 520], radius=24, fill=CARD, outline=LINE, width=3)
    center(d, x + 140, 150, t, font(BOLD, 40), ACCENT)
    center(d, x + 140, 230, d1, font(REG, 26), INK)
    center(d, x + 140, 280, d2, font(REG, 26), INK)
    if i < 2:
        d.line([x + 280, 320, x + 310, 320], fill=ACCENT, width=4)
        d.polygon([(x + 310, 308), (x + 310, 332), (x + 326, 320)], fill=ACCENT)
note(d, W, H)
img.save(os.path.join(ASSETS, "fig-three-areas.png"))

# 2. 구매 요청 흐름 개념도
W, H = 1000, 700
img = Image.new("RGB", (W, H), IVORY)
d = ImageDraw.Draw(img)
center(d, W / 2, 30, "가상 구매 요청 흐름", font(BOLD, 40), INK)
steps = ["신청서 접수", "금액·필수값 검증", "100만원 초과?", "팀장 승인", "결과 기록·알림"]
y = 130
for i, s in enumerate(steps):
    if s.endswith("?"):
        cx = W / 2
        d.polygon([(cx, y), (cx + 180, y + 55), (cx, y + 110), (cx - 180, y + 55)], fill=CARD, outline=ACCENT, width=3)
        center(d, cx, y + 32, s, font(BOLD, 28), INK)
        left(d, cx + 200, y + 30, "예 → 승인", font(REG, 24), SUB)
        left(d, cx - 340, y + 30, "아니오 → 기록", font(REG, 24), SUB)
        y += 150
    else:
        d.rounded_rectangle([W / 2 - 220, y, W / 2 + 220, y + 80], radius=18, fill=CARD, outline=LINE, width=3)
        center(d, W / 2, y + 22, s, font(BOLD, 30), INK)
        y += 110
note(d, W, H)
img.save(os.path.join(ASSETS, "fig-purchase-flow.png"))

# 3. 승인·평가·배포 검토 개념도
W, H = 1000, 620
img = Image.new("RGB", (W, H), IVORY)
d = ImageDraw.Draw(img)
center(d, W / 2, 30, "배포 전 세 단계 검토", font(BOLD, 40), INK)
gates = [("평가", "작업 완료·도구 정확도·안전성 측정"), ("Review 패널", "게시 전 막힘·경고 확인 (GA)"), ("Hooks", "실행 중 정해진 로직 삽입 (미리보기)")]
for i, (t, desc) in enumerate(gates):
    x = 40 + i * 310
    d.rounded_rectangle([x, 140, x + 280, 500], radius=24, fill=CARD, outline=LINE, width=3)
    center(d, x + 140, 170, f"{i+1}단계", font(REG, 26), SUB)
    center(d, x + 140, 220, t, font(BOLD, 38), ACCENT)
    # 줄바꿈 처리
    words, lines, cur = desc.replace("·", "· "), [], ""
    for ch in desc:
        cur += ch
        if len(cur) > 11:
            lines.append(cur); cur = ""
    if cur: lines.append(cur)
    yy = 300
    for ln in lines:
        center(d, x + 140, yy, ln, font(REG, 25), INK)
        yy += 40
note(d, W, H)
img.save(os.path.join(ASSETS, "fig-review-gates.png"))
print("diagrams saved")
