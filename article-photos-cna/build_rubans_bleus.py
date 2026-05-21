"""
Direction 'Rubans bleus' : abstraite, ton sur ton bleu lumineux, relief subtil
Inspiration directe du noeud bleu existant
"""
from PIL import Image, ImageDraw, ImageFilter
import os, math, random

OUT_DIR = r"C:\Users\francois.cellard\OneDrive - CELLARD NOTAIRES\Bureau\Claude 2026\Communication Cellard Notaires\article-photos-cna\charte-RUBANS-BLEUS"
os.makedirs(OUT_DIR, exist_ok=True)

SCALE = 2
W_FINAL, H_FINAL = 1280, 720
W, H = W_FINAL * SCALE, H_FINAL * SCALE

# Palettes bleu lumineux ton sur ton (inspire du noeud existant)
PAL_ROYAL = {
    "bg_top": (60, 90, 145),         # bleu royal lumineux
    "bg_bot": (85, 115, 170),         # bleu royal plus clair
    "ruban_ombre": (45, 70, 120),     # ombre des rubans
    "ruban_base": (95, 125, 175),     # base ruban
    "ruban_mid": (130, 160, 200),     # medium
    "ruban_clair": (170, 195, 225),   # clair (highlight)
    "ruban_reflet": (210, 225, 240),  # reflet brillant
    "name": "royal"
}

PAL_AZUR_LUM = {
    "bg_top": (95, 135, 190),
    "bg_bot": (120, 155, 200),
    "ruban_ombre": (70, 105, 160),
    "ruban_base": (135, 170, 210),
    "ruban_mid": (165, 195, 225),
    "ruban_clair": (200, 220, 240),
    "ruban_reflet": (230, 240, 250),
    "name": "azur-lum"
}

PAL_OCEAN = {
    "bg_top": (50, 100, 140),
    "bg_bot": (80, 130, 165),
    "ruban_ombre": (35, 80, 115),
    "ruban_base": (90, 140, 175),
    "ruban_mid": (130, 175, 205),
    "ruban_clair": (170, 205, 225),
    "ruban_reflet": (210, 230, 240),
    "name": "ocean"
}

PAL_SAPHIR = {
    "bg_top": (70, 110, 165),
    "bg_bot": (95, 135, 185),
    "ruban_ombre": (50, 85, 140),
    "ruban_base": (105, 145, 190),
    "ruban_mid": (140, 175, 215),
    "ruban_clair": (175, 205, 235),
    "ruban_reflet": (215, 230, 245),
    "name": "saphir"
}

def smooth_gradient(top, bottom):
    img = Image.new("RGB", (W, H), top)
    px = img.load()
    for y in range(H):
        t = (1 - math.cos(y/H * math.pi)) / 2
        r = int(top[0] * (1-t) + bottom[0] * t)
        g = int(top[1] * (1-t) + bottom[1] * t)
        b = int(top[2] * (1-t) + bottom[2] * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img

def central_glow(img, cx, cy, max_r, color, intensity=0.30):
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    steps = 40
    for i in range(steps, 0, -1):
        r = int(max_r * i / steps)
        alpha = int(255 * intensity * (1 - i/steps) ** 2)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*color, alpha))
    overlay = overlay.filter(ImageFilter.GaussianBlur(60))
    img.paste(overlay, (0, 0), overlay)
    return img

def soft_shadow(img, shape_func, blur=25, offset=(0, 20), alpha=80):
    shadow = Image.new("RGBA", (W, H), (0,0,0,0))
    s_draw = ImageDraw.Draw(shadow)
    shape_func(s_draw, (0, 0, 0, alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    final = Image.new("RGBA", (W, H), (0,0,0,0))
    final.paste(shadow, offset)
    img.paste(final, (0, 0), final)
    return img

def downscale(img):
    return img.resize((W_FINAL, H_FINAL), Image.LANCZOS)

def subtle_noise(img, intensity=2):
    px = img.load()
    random.seed(42)
    for y in range(0, H, 3):
        for x in range(0, W, 3):
            n = random.randint(-intensity, intensity)
            r, g, b = px[x, y][:3]
            px[x, y] = (max(0, min(255, r+n)), max(0, min(255, g+n)), max(0, min(255, b+n)))
    return img

def draw_ribbon_strand(draw, points, thickness, p):
    """Trace une bande/ruban avec relief 4 couches"""
    layers = [
        (thickness, p["ruban_ombre"]),
        (max(1, thickness - 6*SCALE), p["ruban_base"]),
        (max(1, thickness - 14*SCALE), p["ruban_mid"]),
        (max(1, thickness - 22*SCALE), p["ruban_clair"]),
        (max(1, thickness - 30*SCALE), p["ruban_reflet"]),
    ]
    for thick, color in layers:
        if thick > 0:
            for i in range(len(points)-1):
                draw.line([points[i], points[i+1]], fill=color, width=thick)

# =============================================================
# 1. PACTE DUTREIL : Noeud entrelace - palette ROYAL
# Inspiration directe du noeud existant
# =============================================================
def rubans_noeud():
    p = PAL_ROYAL
    img = smooth_gradient(p["bg_top"], p["bg_bot"])
    img = central_glow(img, W//2, H//2, 600*SCALE, p["ruban_reflet"], 0.18)

    cx, cy = W//2, H//2
    draw = ImageDraw.Draw(img)

    # Noeud horizontal : 5 rubans paralleles qui forment un noeud
    NUM_STRANDS = 5
    SPACING = 18 * SCALE
    THICKNESS = 38 * SCALE
    base_y = -(NUM_STRANDS - 1) * SPACING / 2

    # Ombre portee globale
    shadow_layer = Image.new("RGBA", (W, H), (0,0,0,0))
    sl_draw = ImageDraw.Draw(shadow_layer)
    for strand_idx in range(NUM_STRANDS):
        y_off = base_y + strand_idx * SPACING
        points = []
        for t in range(0, 250):
            nt = t / 250
            x = 150*SCALE + (W - 300*SCALE) * nt
            # Forme de noeud : sinusoide qui se croise
            phase = strand_idx * 0.4
            y = cy + y_off + math.sin(nt * math.pi * 2.5 + phase) * 90*SCALE
            points.append((x, y + 18*SCALE))
        for i in range(len(points)-1):
            sl_draw.line([points[i], points[i+1]], fill=(0,0,0,140), width=THICKNESS)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(15*SCALE))
    img.paste(shadow_layer, (0, 0), shadow_layer)
    draw = ImageDraw.Draw(img)

    # Rubans principaux
    for strand_idx in range(NUM_STRANDS):
        y_off = base_y + strand_idx * SPACING
        phase = strand_idx * 0.4
        points = []
        for t in range(0, 400):
            nt = t / 400
            x = 150*SCALE + (W - 300*SCALE) * nt
            y = cy + y_off + math.sin(nt * math.pi * 2.5 + phase) * 90*SCALE
            points.append((x, y))
        draw_ribbon_strand(draw, points, THICKNESS, p)

    img = subtle_noise(img, 2)
    final = downscale(img)
    final.save(os.path.join(OUT_DIR, "01-noeud-pacte-dutreil.png"), "PNG", optimize=True)
    print(f"OK 01 noeud {p['name']}")

# =============================================================
# 2. ASSURANCE-VIE 70 ANS : Spirale en relief - palette AZUR LUMINEUX
# Symbolise capitalisation et temps
# =============================================================
def rubans_spirale():
    p = PAL_AZUR_LUM
    img = smooth_gradient(p["bg_top"], p["bg_bot"])
    img = central_glow(img, W//2, H//2, 550*SCALE, p["ruban_reflet"], 0.22)

    cx, cy = W//2, H//2
    draw = ImageDraw.Draw(img)

    # Spirale qui s'enroule vers l'exterieur
    THICKNESS = 42 * SCALE
    points = []
    # Spirale logarithmique
    for i in range(0, 800):
        t = i / 800
        angle = t * math.pi * 3.5
        r = 25*SCALE + t * 220*SCALE
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))

    # Ombre portee
    shadow_layer = Image.new("RGBA", (W, H), (0,0,0,0))
    sl_draw = ImageDraw.Draw(shadow_layer)
    for i in range(len(points)-1):
        sl_draw.line([(points[i][0], points[i][1] + 15*SCALE),
                     (points[i+1][0], points[i+1][1] + 15*SCALE)],
                    fill=(0,0,0,120), width=THICKNESS)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(12*SCALE))
    img.paste(shadow_layer, (0, 0), shadow_layer)
    draw = ImageDraw.Draw(img)

    # Ruban en spirale avec relief
    draw_ribbon_strand(draw, points, THICKNESS, p)

    img = subtle_noise(img, 2)
    final = downscale(img)
    final.save(os.path.join(OUT_DIR, "02-spirale-assurance-vie.png"), "PNG", optimize=True)
    print(f"OK 02 spirale {p['name']}")

# =============================================================
# 3. SUCCESSION INTERNATIONALE : Anneaux entrelaces / Möbius - palette OCEAN
# Symbolise liens entre juridictions
# =============================================================
def rubans_anneaux():
    p = PAL_OCEAN
    img = smooth_gradient(p["bg_top"], p["bg_bot"])
    img = central_glow(img, W//2, H//2, 600*SCALE, p["ruban_reflet"], 0.20)
    draw = ImageDraw.Draw(img)

    cx, cy = W//2, H//2
    THICKNESS = 40 * SCALE

    # 3 anneaux entrelaces (style olympique mais alignes)
    R = 130 * SCALE
    centers = [
        (cx - 180*SCALE, cy),
        (cx, cy + 30*SCALE),
        (cx + 180*SCALE, cy),
    ]

    # Ombre portee
    shadow_layer = Image.new("RGBA", (W, H), (0,0,0,0))
    sl_draw = ImageDraw.Draw(shadow_layer)
    for c_x, c_y in centers:
        # Cercle approxime par segments
        pts = []
        for i in range(150):
            t = i / 150
            ang = t * 2 * math.pi
            pts.append((c_x + R * math.cos(ang), c_y + R * math.sin(ang) + 15*SCALE))
        for i in range(len(pts)-1):
            sl_draw.line([pts[i], pts[i+1]], fill=(0,0,0,130), width=THICKNESS)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(12*SCALE))
    img.paste(shadow_layer, (0, 0), shadow_layer)
    draw = ImageDraw.Draw(img)

    # Anneaux entrelaces
    for c_x, c_y in centers:
        pts = []
        for i in range(400):
            t = i / 400
            ang = t * 2 * math.pi - math.pi/2
            pts.append((c_x + R * math.cos(ang), c_y + R * math.sin(ang)))
        draw_ribbon_strand(draw, pts, THICKNESS, p)

    img = subtle_noise(img, 2)
    final = downscale(img)
    final.save(os.path.join(OUT_DIR, "03-anneaux-succession.png"), "PNG", optimize=True)
    print(f"OK 03 anneaux {p['name']}")

# =============================================================
# 4. HOLDING : Pyramide de lignes / strates - palette SAPHIR
# Symbolise structure hierarchique
# =============================================================
def rubans_pyramide():
    p = PAL_SAPHIR
    img = smooth_gradient(p["bg_top"], p["bg_bot"])
    img = central_glow(img, W//2, H//2, 550*SCALE, p["ruban_reflet"], 0.22)
    draw = ImageDraw.Draw(img)

    cx, cy = W//2, H//2

    # 5 lignes superposees en pyramide
    NUM = 5
    SPACING = 50 * SCALE
    THICKNESS = 38 * SCALE
    BASE_W = 380 * SCALE

    # Ombre portee
    shadow_layer = Image.new("RGBA", (W, H), (0,0,0,0))
    sl_draw = ImageDraw.Draw(shadow_layer)
    for i in range(NUM):
        y_pos = cy + 100*SCALE - i * SPACING
        w_now = BASE_W - i * 50*SCALE
        # Ligne legerement arquee (effet ruban suspendu)
        pts = []
        for t in range(0, 200):
            nt = t / 200
            x = cx - w_now/2 + w_now * nt
            y_arc = y_pos + math.sin(nt * math.pi) * 15*SCALE
            pts.append((x, y_arc + 15*SCALE))
        for j in range(len(pts)-1):
            sl_draw.line([pts[j], pts[j+1]], fill=(0,0,0,120), width=THICKNESS)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(12*SCALE))
    img.paste(shadow_layer, (0, 0), shadow_layer)
    draw = ImageDraw.Draw(img)

    # 5 rubans en pyramide
    for i in range(NUM):
        y_pos = cy + 100*SCALE - i * SPACING
        w_now = BASE_W - i * 50*SCALE
        pts = []
        for t in range(0, 300):
            nt = t / 300
            x = cx - w_now/2 + w_now * nt
            y_arc = y_pos + math.sin(nt * math.pi) * 15*SCALE
            pts.append((x, y_arc))
        # Plus on monte, plus le ruban est mis en avant (avec un peu plus de eclat)
        draw_ribbon_strand(draw, pts, THICKNESS, p)

    img = subtle_noise(img, 2)
    final = downscale(img)
    final.save(os.path.join(OUT_DIR, "04-pyramide-holding.png"), "PNG", optimize=True)
    print(f"OK 04 pyramide {p['name']}")

if __name__ == "__main__":
    rubans_noeud()
    rubans_spirale()
    rubans_anneaux()
    rubans_pyramide()
    print("\nAll 4 saved in:", OUT_DIR)
