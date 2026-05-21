from PIL import Image, ImageDraw
import os, math

OUT_DIR = r"C:\Users\francois.cellard\OneDrive - CELLARD NOTAIRES\Bureau\Claude 2026\Communication Cellard Notaires\article-photos-cna\charte-v2-neoclassique"
os.makedirs(OUT_DIR, exist_ok=True)

NAVY = (26, 58, 82)
NAVY_DARK = (12, 28, 45)
OR = (201, 166, 107)
OR_LIGHT = (224, 196, 144)
OR_DARK = (160, 130, 80)
WHITE = (245, 240, 225)

W, H = 1280, 720

def gradient_bg(top, bottom):
    img = Image.new("RGB", (W, H), top)
    px = img.load()
    for y in range(H):
        r = top[0] + int((bottom[0]-top[0]) * y / H)
        g = top[1] + int((bottom[1]-top[1]) * y / H)
        b = top[2] + int((bottom[2]-top[2]) * y / H)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img

def draw_arc_points(cx, cy, r, start_deg, end_deg, steps=50):
    pts = []
    for i in range(steps+1):
        deg = start_deg + (end_deg-start_deg) * i / steps
        rad = math.radians(deg)
        pts.append((cx + r*math.cos(rad), cy + r*math.sin(rad)))
    return pts

def signature_bands(draw):
    draw.rectangle([0, 0, 4, H], fill=OR)
    draw.rectangle([0, H-4, W, H], fill=OR)

def circle_outline(draw, cx, cy, r, color, width=2):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=width)

# ====================================================
# 1. PACTE DUTREIL : sceau + sablier
# ====================================================
def illu_pacte_dutreil():
    img = gradient_bg(NAVY_DARK, NAVY)
    draw = ImageDraw.Draw(img)
    signature_bands(draw)
    cx, cy = W // 2, H // 2

    for r, c, w in [(280, OR_DARK, 1), (260, OR, 2), (240, OR, 1), (210, OR_LIGHT, 1)]:
        circle_outline(draw, cx, cy, r, c, width=w)

    for deg in range(0, 360, 15):
        x = cx + 260 * math.cos(math.radians(deg))
        y = cy + 260 * math.sin(math.radians(deg))
        draw.ellipse([x-3, y-3, x+3, y+3], fill=OR)

    sab_w, sab_h = 80, 200
    draw.polygon([(cx-sab_w, cy-sab_h//2), (cx+sab_w, cy-sab_h//2), (cx, cy)],
                 outline=OR_LIGHT, width=3)
    draw.polygon([(cx-sab_w, cy+sab_h//2), (cx+sab_w, cy+sab_h//2), (cx, cy)],
                 fill=OR, outline=OR_LIGHT)
    draw.line([(cx-sab_w-15, cy-sab_h//2), (cx+sab_w+15, cy-sab_h//2)], fill=WHITE, width=3)
    draw.line([(cx-sab_w-15, cy+sab_h//2), (cx+sab_w+15, cy+sab_h//2)], fill=WHITE, width=3)
    draw.line([(cx, cy-5), (cx, cy+5)], fill=OR_LIGHT, width=2)

    col_w = 12
    for i, x_off in enumerate([-380, -340, -300]):
        h_col = 60 + i * 30
        draw.rectangle([cx + x_off - col_w//2, cy + h_col//2 - h_col,
                       cx + x_off + col_w//2, cy + h_col//2], fill=OR_LIGHT, outline=OR)
    for i, x_off in enumerate([300, 340, 380]):
        h_col = 60 + (2-i) * 30
        draw.rectangle([cx + x_off - col_w//2, cy + h_col//2 - h_col,
                       cx + x_off + col_w//2, cy + h_col//2], fill=OR_LIGHT, outline=OR)

    img.save(os.path.join(OUT_DIR, "01-pacte-dutreil-sceau-sablier.png"), "PNG", optimize=True)
    print("OK 01")

# ====================================================
# 2. ASSURANCE-VIE : bouclier + spirale Fibonacci
# ====================================================
def illu_assurance_vie():
    img = gradient_bg(NAVY_DARK, NAVY)
    draw = ImageDraw.Draw(img)
    signature_bands(draw)
    cx, cy = W // 2, H // 2

    shield_w, shield_h = 240, 320
    top_y = cy - shield_h // 2
    pts = []
    pts.append((cx - shield_w, top_y))
    pts.append((cx + shield_w, top_y))
    pts.append((cx + shield_w, top_y + shield_h * 0.4))
    arc1 = draw_arc_points(cx, top_y + shield_h * 0.4, shield_w, 0, 90, 30)
    pts.extend(arc1[1:])
    arc2 = draw_arc_points(cx, top_y + shield_h * 0.4, shield_w, 90, 180, 30)
    pts.extend(arc2[1:])
    pts.append((cx - shield_w, top_y))
    draw.line(pts + [pts[0]], fill=OR, width=4)

    sp_cx, sp_cy = cx, cy + 30
    spiral_pts = []
    for i in range(120):
        angle = i * 0.25
        r = 5 + i * 1.2
        x = sp_cx + r * math.cos(angle)
        y = sp_cy + r * math.sin(angle)
        spiral_pts.append((x, y))
    for i in range(len(spiral_pts)-1):
        t = i / len(spiral_pts)
        c_r = int(OR[0] * (1-t) + OR_LIGHT[0] * t)
        c_g = int(OR[1] * (1-t) + OR_LIGHT[1] * t)
        c_b = int(OR[2] * (1-t) + OR_LIGHT[2] * t)
        draw.line([spiral_pts[i], spiral_pts[i+1]], fill=(c_r, c_g, c_b), width=3)

    draw.line([(cx - 30, top_y - 20), (cx, top_y - 50), (cx + 30, top_y - 20)],
              fill=OR_LIGHT, width=3)
    draw.ellipse([cx - 6, top_y - 56, cx + 6, top_y - 44], fill=OR)

    for r in [350, 400, 450]:
        circle_outline(draw, cx, cy, r, OR_DARK, width=1)

    img.save(os.path.join(OUT_DIR, "02-assurance-vie-bouclier-spirale.png"), "PNG", optimize=True)
    print("OK 02")

# ====================================================
# 3. SUCCESSION INTERNATIONALE : globe + meridiens + etoiles
# ====================================================
def illu_succession_international():
    img = gradient_bg(NAVY_DARK, NAVY)
    draw = ImageDraw.Draw(img)
    signature_bands(draw)
    cx, cy = W // 2, H // 2

    r_globe = 220
    circle_outline(draw, cx, cy, r_globe, OR, width=3)
    for tilt in [10, 30, 50, 70, 90]:
        ew = int(r_globe * math.cos(math.radians(tilt)))
        if ew > 5:
            draw.ellipse([cx-ew, cy-r_globe, cx+ew, cy+r_globe], outline=OR_LIGHT, width=1)
    for y_off in [-r_globe*0.6, -r_globe*0.3, 0, r_globe*0.3, r_globe*0.6]:
        d = math.sqrt(r_globe**2 - y_off**2)
        draw.line([(cx-d, cy+y_off), (cx+d, cy+y_off)], fill=OR_LIGHT, width=1)
    draw.ellipse([cx-r_globe, cy-int(r_globe*0.15), cx+r_globe, cy+int(r_globe*0.15)],
                 outline=OR, width=2)

    star_r = r_globe + 80
    for i in range(12):
        deg = -90 + i * 30
        sx = cx + star_r * math.cos(math.radians(deg))
        sy = cy + star_r * math.sin(math.radians(deg))
        star_size = 10
        star_pts = []
        for j in range(10):
            angle = math.radians(j * 36 - 90)
            r_use = star_size if j % 2 == 0 else star_size // 2
            star_pts.append((sx + r_use * math.cos(angle), sy + r_use * math.sin(angle)))
        draw.polygon(star_pts, fill=OR_LIGHT)

    p1 = (cx - 130, cy - 60)
    p2 = (cx + 30, cy + 40)
    p3 = (cx + 150, cy - 100)
    for x, y in [p1, p2, p3]:
        draw.ellipse([x-8, y-8, x+8, y+8], fill=OR, outline=WHITE, width=2)

    def dashed_line(p_a, p_b):
        steps = 20
        for i in range(0, steps, 2):
            x1 = p_a[0] + (p_b[0]-p_a[0]) * i/steps
            y1 = p_a[1] + (p_b[1]-p_a[1]) * i/steps
            x2 = p_a[0] + (p_b[0]-p_a[0]) * (i+1)/steps
            y2 = p_a[1] + (p_b[1]-p_a[1]) * (i+1)/steps
            draw.line([(x1, y1), (x2, y2)], fill=OR_LIGHT, width=2)
    dashed_line(p1, p2)
    dashed_line(p2, p3)

    img.save(os.path.join(OUT_DIR, "03-succession-internationale-globe.png"), "PNG", optimize=True)
    print("OK 03")

# ====================================================
# 4. HOLDING : colonnes neoclassiques + fronton
# ====================================================
def illu_holding():
    img = gradient_bg(NAVY_DARK, NAVY)
    draw = ImageDraw.Draw(img)
    signature_bands(draw)
    cx, cy = W // 2, H // 2

    col_count = 4
    col_w = 50
    col_h = 320
    col_spacing = 130

    for i in range(col_count):
        x = cx + (i - (col_count-1)/2) * col_spacing
        base_h = 20
        draw.rectangle([x - col_w//2 - 10, cy + col_h//2 - base_h,
                       x + col_w//2 + 10, cy + col_h//2], outline=OR, width=2)
        draw.rectangle([x - col_w//2 - 15, cy + col_h//2,
                       x + col_w//2 + 15, cy + col_h//2 + 10], fill=OR, outline=OR_LIGHT)

        draw.rectangle([x - col_w//2, cy - col_h//2 + 20,
                       x + col_w//2, cy + col_h//2 - base_h], outline=OR, width=2)
        for cn in [-15, 0, 15]:
            draw.line([(x + cn, cy - col_h//2 + 25), (x + cn, cy + col_h//2 - base_h - 5)],
                     fill=OR_DARK, width=1)

        cap_h = 30
        cap_y = cy - col_h//2
        draw.rectangle([x - col_w//2 - 15, cap_y, x + col_w//2 + 15, cap_y + 8],
                      fill=OR, outline=OR_LIGHT)
        draw.ellipse([x - col_w//2 - 18, cap_y + 8, x - col_w//2 + 2, cap_y + 26],
                    outline=OR_LIGHT, width=2)
        draw.ellipse([x + col_w//2 - 2, cap_y + 8, x + col_w//2 + 18, cap_y + 26],
                    outline=OR_LIGHT, width=2)

    pediment_left = cx - (col_count-1)/2 * col_spacing - col_w//2 - 25
    pediment_right = cx + (col_count-1)/2 * col_spacing + col_w//2 + 25
    pediment_top = cy - col_h//2 - 60
    pediment_bot = cy - col_h//2 - 12
    draw.polygon([(pediment_left, pediment_bot), (pediment_right, pediment_bot),
                 (cx, pediment_top)], outline=OR, width=2)
    draw.ellipse([cx - 10, pediment_top + 30, cx + 10, pediment_top + 50], outline=OR_LIGHT, width=2)

    floor_y = cy + col_h//2 + 12
    floor_w = (pediment_right - pediment_left) + 60
    for step_i in range(3):
        step_y = floor_y + step_i * 10
        step_w = floor_w + step_i * 30
        draw.line([(cx - step_w//2, step_y), (cx + step_w//2, step_y)],
                  fill=OR_LIGHT, width=2)

    img.save(os.path.join(OUT_DIR, "04-holding-colonnes-fronton.png"), "PNG", optimize=True)
    print("OK 04")

illu_pacte_dutreil()
illu_assurance_vie()
illu_succession_international()
illu_holding()
print("\nDone:", OUT_DIR)
