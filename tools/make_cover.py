#!/usr/bin/env python3
"""표지 합성: AI 일러스트 + 한글 타이틀 (1000x1300)"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

W, H = 1000, 1300
illust = Image.open(os.path.join(ASSETS, "media-generation-cover-illustration-0-a1315332-d578-494f-a32f-3dccc9d1b7ca.png")).convert("RGB")
# 상단 일러스트 영역: 원본 상단부를 1000x760에 맞춤
top = illust.crop((0, 0, illust.width, int(illust.width * 0.76))).resize((W, 760), Image.LANCZOS)

cover = Image.new("RGB", (W, H), (250, 243, 232))
cover.paste(top, (0, 0))
d = ImageDraw.Draw(cover)

def font(path, size):
    return ImageFont.truetype(path, size, index=1)

def center(cx, y, s, f, fill):
    bb = d.textbbox((0, 0), s, font=f)
    w = bb[2] - bb[0]
    d.text((cx - w / 2 - bb[0], y), s, font=f, fill=fill)

INK = (62, 44, 30)
ACCENT = (196, 110, 58)
SUB = (120, 96, 74)

center(W / 2, 800, "Copilot Studio로", font(BOLD, 72), INK)
center(W / 2, 900, "업무 앱·워크플로 만들기", font(BOLD, 64), INK)
center(W / 2, 1000, "앱·규칙형 자동화·AI 에이전트를 연결하는", font(REG, 30), SUB)
center(W / 2, 1045, "노코드 실무 입문", font(REG, 30), SUB)
d.line([(300, 1120), (700, 1120)], fill=(210, 185, 150), width=2)
center(W / 2, 1150, "이준수 지음", font(BOLD, 34), ACCENT)

cover.save(os.path.join(ASSETS, "cover.png"))
print("cover.png saved", cover.size)
