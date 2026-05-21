"""
Rendus definitifs - supersampling 2x pour anti-aliasing professionnel
Direction : Matiere noble
"""
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance
import os, math, random

OUT_DIR = r"C:\Users\francois.cellard\OneDrive - CELLARD NOTAIRES\Bureau\Claude 2026\Communication Cellard Notaires\article-photos-cna\charte-FINAL"
os.makedirs(OUT_DIR, exist_ok=True)

# Final : 1280x720 - on dessine en 2x puis downsample
SCALE = 2
W_FINAL, H_FINAL = 1280, 720
W, H = W_FINAL * SCALE, H_FINAL * SCALE

PALETTES = {
    "marine": {
        "bg_top": (8, 22, 42),
        "bg_bot": (28, 58, 90),
        "metal_dark": (130, 90, 40),
        "metal": (205, 160, 90),
        "metal_light": (235, 195, 125),
        "highlight": (255, 235, 175),
        "shadow": (4, 14, 28),
    },
    "petrole": {
        "bg_top": (12, 35, 45),
        "bg_bot": (40, 75, 85),
        "metal_dark": (120, 70, 50),
        "metal": (195, 130, 80),
        "metal_light": (230, 170, 110),
        "highlight": (255, 220, 160),
        "shadow": (5, 18, 22),
    },
    "carbone": {
        "bg_top": (15, 18, 25),
        "bg_bot": (45, 48, 60),
        "metal_dark": (130, 105, 55),
        "metal": (200, 168, 90),
        "metal_light": (235, 205, 130),
        "highlight": (255, 235, 180),
        "shadow": (5, 5, 10),
    },
    "minuit": {
        "bg_top": (18, 22, 50),
        "bg_bot": (45, 55, 95),
        "metal_dark": (115, 92, 130),
        "metal": (180, 148, 198),
        "metal_light": (218, 192, 232),
        "highlight": (245, 230, 252),
        "shadow": (8, 10, 25),
    },
}

def smooth_gradient_bg(top, bottom):
    img = Image.new("RGB", (W, H), top)
    px = img.load()
    for y in range(H):
        # Easing : courbe smooth (cosine)
        t = y / H
        t = (1 - math.cos(t * math.pi)) / 2  # easing in-out
        r = int(top[0] * (1-t) + bottom[0] * t)
        g = int(top[1] * (1-t) + bottom[1] * t)
        b = int(top[2] * (1-t) + bottom[2] * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img

def add_vignette(img, intensity=0.4):
    """Vignette sombre sur les bords"""
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = W // 2, H // 2
    max_d = math.sqrt(cx**2 + cy**2)
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            d = math.sqrt((x-cx)**2 + (y-cy)**2)
            t = (d / max_d) ** 2
            alpha = int(255 * intensity * t)
            draw.rectangle([x, y, x+2, y+2], fill=(0, 0, 0, alpha))
    img.paste(overlay, (0, 0), overlay)
    return img

def radial_light(img, cx, cy, max_r, color, intensity=0.6):
    """Lumiere radiale douce - utilise PIL ellipses pour rapidite"""
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    steps = 40
    for i in range(steps, 0, -1):
        r = int(max_r * i / steps)
        alpha = int(255 * intensity * (1 - i/steps) ** 2)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*color, alpha))
    overlay = overlay.filter(ImageFilter.GaussianBlur(30))
    img.paste(overlay, (0, 0), overlay)
    return img

def soft_noise(img, intensity=4):
    """Bruit doux pour texture"""
    px = img.load()
    random.seed(42)
    for y in range(0, H, 3):
        for x in range(0, W, 3):
            n = random.randint(-intensity, intensity)
            r, g, b = px[x, y][:3]
            px[x, y] = (max(0, min(255, r+n)), max(0, min(255, g+n)), max(0, min(255, b+n)))
    return img

def signature_bands(draw, p):
    bar_w = 6 * SCALE
    draw.rectangle([0, 0, bar_w, H], fill=p["metal"])
    draw.rectangle([0, H-bar_w, W, H], fill=p["metal"])

def lerp_color(c1, c2, t):
    t = max(0, min(1, t))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def drop_shadow(img, shape_func, blur=20, offset=(0, 15), alpha=120):
    """Genere une ombre portee via flou sur masque"""
    shadow = Image.new("RGBA", (W, H), (0,0,0,0))
    s_draw = ImageDraw.Draw(shadow)
    shape_func(s_draw, (0, 0, 0, alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    # Decalage
    final = Image.new("RGBA", (W, H), (0,0,0,0))
    final.paste(shadow, offset)
    img.paste(final, (0, 0), final)
    return img

def downscale_final(img):
    """Downsample 2x pour anti-aliasing"""
    return img.resize((W_FINAL, H_FINAL), Image.LANCZOS)

# =============================================================
# 1. ASSURANCE-VIE APRES 70 ANS : Orbe enveloppant - palette PETROLE
# =============================================================
def final_assurance_vie():
    p = PALETTES["petrole"]
    img = smooth_gradient_bg(p["bg_top"], p["bg_bot"])
    img = radial_light(img, W//2 - 80*SCALE, H//2 - 80*SCALE, 600*SCALE, p["highlight"], 0.35)

    cx, cy = W//2, H//2 + 20*SCALE
    R = 240 * SCALE

    # Ombre portee sous l'orbe
    def shadow_shape(draw, color):
        draw.ellipse([cx - R, cy + R - 20*SCALE, cx + R, cy + R + 60*SCALE], fill=color)
    img = drop_shadow(img, shadow_shape, blur=35*SCALE//2, offset=(0, 20*SCALE), alpha=150)
    draw = ImageDraw.Draw(img)

    # Orbe principal avec gradient radial cuivre/or
    for radius in range(R, 0, -1):
        t = radius / R
        # Decalage du centre apparent pour effet 3D
        off_x = -int(35 * SCALE * (1-t))
        off_y = -int(35 * SCALE * (1-t))
        color = lerp_color(p["highlight"], p["metal_dark"], t**1.3)
        draw.ellipse([cx - radius + off_x, cy - radius + off_y,
                     cx + radius + off_x, cy + radius + off_y],
                     fill=color)

    # Reflet brillant en haut-gauche
    refl_overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    rd = ImageDraw.Draw(refl_overlay)
    for i in range(60, 0, -1):
        t = i / 60
        rd.ellipse([cx - 100*SCALE - 40*SCALE, cy - 130*SCALE - 30*SCALE,
                   cx - 100*SCALE + 40*SCALE, cy - 130*SCALE + 30*SCALE],
                  fill=(255, 240, 200, int(120 * t)))
    refl_overlay = refl_overlay.filter(ImageFilter.GaussianBlur(20))
    img.paste(refl_overlay, (0, 0), refl_overlay)
    draw = ImageDraw.Draw(img)

    # Meridiens (lignes courbes sur l'orbe)
    for offset_x_pct, opacity in [(-0.4, 0.6), (0, 0.9), (0.4, 0.6)]:
        for i in range(120):
            t = i / 120
            angle = math.pi * t
            x = cx + R * offset_x_pct * math.sin(angle)
            y_top = cy - R * math.cos(angle * 0.95)
            x_off = math.sin(t * math.pi) * 30 * SCALE * offset_x_pct
            draw.ellipse([x + x_off - 2, y_top - 2, x + x_off + 2, y_top + 2],
                        fill=p["highlight"])

    # Ligne equatoriale
    for i in range(120):
        t = i / 120
        angle = math.pi * t
        x = cx - R + 2 * R * t
        y_off = -math.cos(angle) * 35 * SCALE
        draw.ellipse([x - 2, cy + y_off - 2, x + 2, cy + y_off + 2], fill=p["metal_light"])

    signature_bands(draw, p)
    img = add_vignette(img, 0.35)
    img = soft_noise(img, 4)

    final = downscale_final(img)
    p_out = os.path.join(OUT_DIR, "01-assurance-vie-orbe.png")
    final.save(p_out, "PNG", optimize=True)
    print(f"OK 01 assurance-vie")
    return p_out

# =============================================================
# 2. SUCCESSION INTERNATIONALE : Cordes traversant un globe - palette MARINE
# =============================================================
def final_succession_internationale():
    p = PALETTES["marine"]
    img = smooth_gradient_bg(p["bg_top"], p["bg_bot"])
    img = radial_light(img, W//2, H//2, 700*SCALE, p["metal_light"], 0.20)

    cx, cy = W//2, H//2
    R = 220 * SCALE

    draw = ImageDraw.Draw(img)

    # Globe filaire : meridiens en ellipse
    # On dessine le globe (uniquement les lignes, fond transparent)
    for tilt_deg in range(0, 180, 15):
        tilt = math.radians(tilt_deg)
        ew = abs(R * math.cos(tilt))
        if ew > 4 * SCALE:
            # Couleur qui s'assombrit selon angle (effet 3D)
            t = abs(math.sin(tilt))
            color = lerp_color(p["metal_dark"], p["metal_light"], t)
            draw.ellipse([cx-ew, cy-R, cx+ew, cy+R], outline=color, width=int(2*SCALE))

    # Paralleles
    for y_ratio in [-0.7, -0.5, -0.25, 0, 0.25, 0.5, 0.7]:
        y_off = y_ratio * R
        d = math.sqrt(R**2 - y_off**2)
        # Couleur degradee selon position
        t = 1 - abs(y_ratio)
        color = lerp_color(p["metal_dark"], p["metal_light"], t)
        draw.line([(cx-d, cy+y_off), (cx+d, cy+y_off)], fill=color, width=int(2*SCALE))

    # Equateur principal (plus epais)
    draw.ellipse([cx-R, cy-int(R*0.12), cx+R, cy+int(R*0.12)], outline=p["metal"], width=int(3*SCALE))

    # Cordes dorees qui traversent le globe (5 cordes entrelacees)
    NUM = 4
    AMPL = 90 * SCALE
    SPACE = 22 * SCALE
    for strand_idx in range(NUM):
        y_offset = (strand_idx - (NUM-1)/2) * SPACE
        phase = strand_idx * 0.4
        points = []
        for t in range(0, 200):
            x = 60*SCALE + (W - 120*SCALE) * t / 200
            normalized = (x - 60*SCALE) / (W - 120*SCALE)
            y = cy + y_offset + math.sin(normalized * 2 * math.pi * 1.5 + phase) * AMPL * 0.5
            points.append((x, y))
        # Effet relief : 4 passes
        for thick, color in [
            (16*SCALE, p["metal_dark"]),
            (12*SCALE, p["metal"]),
            (7*SCALE, p["metal_light"]),
            (3*SCALE, p["highlight"]),
        ]:
            for i in range(len(points)-1):
                draw.line([points[i], points[i+1]], fill=color, width=thick)

    # 3 points connectes : capitales / points cles de succession
    pts = [(cx - 150*SCALE, cy - 50*SCALE),
           (cx + 50*SCALE, cy + 70*SCALE),
           (cx + 180*SCALE, cy - 90*SCALE)]
    for x, y in pts:
        # Halo
        for r_inner in range(int(20*SCALE), 0, -2):
            t = r_inner / (20*SCALE)
            alpha_col = (*p["highlight"], int(180 * (1-t)))
            overlay = Image.new("RGBA", (W, H), (0,0,0,0))
            od = ImageDraw.Draw(overlay)
            od.ellipse([x-r_inner, y-r_inner, x+r_inner, y+r_inner], fill=alpha_col)
            img.paste(overlay, (0,0), overlay)
        draw = ImageDraw.Draw(img)
        draw.ellipse([x-6*SCALE, y-6*SCALE, x+6*SCALE, y+6*SCALE],
                    fill=p["highlight"], outline=p["metal"], width=int(2*SCALE))

    signature_bands(draw, p)
    img = add_vignette(img, 0.30)
    img = soft_noise(img, 4)

    final = downscale_final(img)
    p_out = os.path.join(OUT_DIR, "02-succession-internationale.png")
    final.save(p_out, "PNG", optimize=True)
    print(f"OK 02 succession-internationale")
    return p_out

# =============================================================
# 3. HOLDING PATRIMONIALE : Strates en relief - palette CARBONE
# =============================================================
def final_holding():
    p = PALETTES["carbone"]
    img = smooth_gradient_bg(p["bg_top"], p["bg_bot"])
    img = radial_light(img, W//2, H//2 - 50*SCALE, 600*SCALE, p["highlight"], 0.30)

    cx, cy = W//2, H//2 + 110*SCALE
    draw = ImageDraw.Draw(img)

    NUM = 8
    BASE_W = 380 * SCALE
    LAYER_H = 32 * SCALE

    for i in range(NUM):
        t = i / (NUM - 1)
        w_lay = int(BASE_W - i * 32*SCALE)
        y_lay = cy - i * (LAYER_H - 4*SCALE)
        # Couleur degrade
        color = lerp_color(p["metal_dark"], p["highlight"], t)
        color_top = lerp_color(p["metal"], p["highlight"], t)

        # Ombre portee (legere)
        if i > 0:
            sh = Image.new("RGBA", (W, H), (0,0,0,0))
            sh_draw = ImageDraw.Draw(sh)
            sh_draw.ellipse([cx - w_lay, y_lay + 2*SCALE, cx + w_lay, y_lay + LAYER_H + 12*SCALE],
                           fill=(0,0,0,80))
            sh = sh.filter(ImageFilter.GaussianBlur(10*SCALE//2))
            img.paste(sh, (0,0), sh)
            draw = ImageDraw.Draw(img)

        # Strate principale (ellipse) - corps en metal sombre/clair
        draw.ellipse([cx - w_lay, y_lay, cx + w_lay, y_lay + LAYER_H],
                    fill=color)

        # Top de la strate (lumiere) - ellipse plus claire et plus petite
        hi_w = int(w_lay * 0.85)
        draw.ellipse([cx - hi_w, y_lay + 2*SCALE, cx + hi_w, y_lay + 6*SCALE],
                    fill=color_top)

        # Top brilliant - tres mince ellipse highlight
        super_hi_w = int(w_lay * 0.5)
        draw.ellipse([cx - super_hi_w, y_lay + 1*SCALE, cx + super_hi_w, y_lay + 3*SCALE],
                    fill=p["highlight"])

        # Outline subtil
        draw.ellipse([cx - w_lay, y_lay, cx + w_lay, y_lay + LAYER_H],
                    outline=p["metal_light"], width=1)

    # Sommet : petit globe doré sur la strate du haut
    top_y = cy - (NUM-1) * (LAYER_H - 4*SCALE)
    crown_r = 25 * SCALE
    crown_cx, crown_cy = cx, top_y - crown_r
    # Globe sommet avec degrade
    for radius in range(crown_r, 0, -1):
        t = radius / crown_r
        color = lerp_color(p["highlight"], p["metal_dark"], t**1.2)
        draw.ellipse([crown_cx - radius - int(5*SCALE*(1-t)),
                     crown_cy - radius - int(5*SCALE*(1-t)),
                     crown_cx + radius - int(5*SCALE*(1-t)),
                     crown_cy + radius - int(5*SCALE*(1-t))],
                     fill=color)

    signature_bands(draw, p)
    img = add_vignette(img, 0.40)
    img = soft_noise(img, 3)

    final = downscale_final(img)
    p_out = os.path.join(OUT_DIR, "03-holding-strates.png")
    final.save(p_out, "PNG", optimize=True)
    print(f"OK 03 holding")
    return p_out

# =============================================================
# 4. PACTE DUTREIL : Cordes tressees en relief - palette MARINE
# =============================================================
def final_pacte_dutreil():
    p = PALETTES["marine"]
    img = smooth_gradient_bg(p["bg_top"], p["bg_bot"])
    img = radial_light(img, W//2, H//2, 600*SCALE, p["metal_light"], 0.22)

    cx, cy = W//2, H//2
    draw = ImageDraw.Draw(img)

    # Cordes tressees - plus de cordes et plus epais avec relief tres prononce
    NUM_STRANDS = 7
    STRAND_SPACING = 18 * SCALE
    AMPLITUDE = 100 * SCALE
    WAVELENGTH = 700 * SCALE
    THICKNESS = 32 * SCALE

    base_y_offset = -(NUM_STRANDS-1) * STRAND_SPACING // 2

    # Ombre portee globale
    sh = Image.new("RGBA", (W, H), (0,0,0,0))
    sh_draw = ImageDraw.Draw(sh)
    for strand_idx in range(NUM_STRANDS):
        y_offset = base_y_offset + strand_idx * STRAND_SPACING
        phase = strand_idx * 0.35
        points = []
        for t in range(0, 200):
            x = 100*SCALE + (W - 200*SCALE) * t / 200
            normalized = (x - 100*SCALE) / (W - 200*SCALE)
            y = cy + y_offset + math.sin(normalized * 2 * math.pi * 2 + phase) * AMPLITUDE
            points.append((x, y + 15*SCALE))  # offset pour ombre
        for i in range(len(points)-1):
            sh_draw.line([points[i], points[i+1]], fill=(0,0,0,150), width=THICKNESS)
    sh = sh.filter(ImageFilter.GaussianBlur(8*SCALE))
    img.paste(sh, (0,0), sh)
    draw = ImageDraw.Draw(img)

    # Cordes (4 passes pour le relief)
    for strand_idx in range(NUM_STRANDS):
        y_offset = base_y_offset + strand_idx * STRAND_SPACING
        phase = strand_idx * 0.35
        points = []
        for t in range(0, 300):
            x = 100*SCALE + (W - 200*SCALE) * t / 300
            normalized = (x - 100*SCALE) / (W - 200*SCALE)
            y = cy + y_offset + math.sin(normalized * 2 * math.pi * 2 + phase) * AMPLITUDE
            points.append((x, y))

        for thick, color in [
            (THICKNESS, p["metal_dark"]),
            (THICKNESS - 8*SCALE, p["metal"]),
            (THICKNESS - 16*SCALE, p["metal_light"]),
            (THICKNESS - 24*SCALE, p["highlight"]),
        ]:
            if thick > 0:
                for i in range(len(points)-1):
                    draw.line([points[i], points[i+1]], fill=color, width=thick)

    signature_bands(draw, p)
    img = add_vignette(img, 0.35)
    img = soft_noise(img, 4)

    final = downscale_final(img)
    p_out = os.path.join(OUT_DIR, "04-pacte-dutreil-cordes.png")
    final.save(p_out, "PNG", optimize=True)
    print(f"OK 04 pacte-dutreil")
    return p_out

if __name__ == "__main__":
    final_assurance_vie()
    final_succession_internationale()
    final_holding()
    final_pacte_dutreil()
    print("\nAll 4 final renders saved in:", OUT_DIR)
