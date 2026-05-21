"""
Direction artistique 'Lumiere notariale' : bleu lumineux dominant + or accent
"""
from PIL import Image, ImageDraw, ImageFilter
import os, math, random

OUT_DIR = r"C:\Users\francois.cellard\OneDrive - CELLARD NOTAIRES\Bureau\Claude 2026\Communication Cellard Notaires\article-photos-cna\charte-LUMIERE-NOTARIALE"
os.makedirs(OUT_DIR, exist_ok=True)

SCALE = 2
W_FINAL, H_FINAL = 1280, 720
W, H = W_FINAL * SCALE, H_FINAL * SCALE

# Palettes BLEU LUMINEUX (jamais sombre)
PAL_AZUR = {
    "bg_top": (208, 225, 240),       # bleu poudre tres clair
    "bg_bot": (175, 200, 225),        # bleu paon doux
    "bg_accent": (220, 235, 245),
    "or_clair": (220, 185, 125),
    "or": (190, 155, 90),
    "or_fonce": (145, 110, 55),
    "marine": (60, 90, 130),          # marine doux (touche d'accent)
    "ombre": (140, 160, 180),
    "blanc": (252, 250, 245),
    "name": "azur"
}

PAL_PAON = {
    "bg_top": (195, 220, 230),
    "bg_bot": (155, 195, 215),
    "bg_accent": (210, 230, 240),
    "or_clair": (218, 180, 115),
    "or": (185, 145, 85),
    "or_fonce": (140, 100, 50),
    "marine": (55, 95, 125),
    "ombre": (130, 160, 175),
    "blanc": (253, 252, 248),
    "name": "paon"
}

PAL_CIEL = {
    "bg_top": (215, 230, 245),
    "bg_bot": (185, 210, 230),
    "bg_accent": (225, 238, 248),
    "or_clair": (225, 190, 130),
    "or": (195, 160, 95),
    "or_fonce": (150, 115, 60),
    "marine": (65, 95, 135),
    "ombre": (145, 165, 180),
    "blanc": (255, 252, 248),
    "name": "ciel"
}

PAL_GLACE = {
    "bg_top": (220, 232, 240),
    "bg_bot": (190, 208, 222),
    "bg_accent": (230, 240, 246),
    "or_clair": (222, 188, 128),
    "or": (190, 155, 92),
    "or_fonce": (145, 108, 55),
    "marine": (60, 90, 125),
    "ombre": (140, 160, 175),
    "blanc": (253, 251, 247),
    "name": "glace"
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

def warm_glow(img, cx, cy, max_r, color, intensity=0.25):
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    steps = 35
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

def lerp(c1, c2, t):
    t = max(0, min(1, t))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def subtle_noise(img, intensity=2):
    px = img.load()
    random.seed(42)
    for y in range(0, H, 3):
        for x in range(0, W, 3):
            n = random.randint(-intensity, intensity)
            r, g, b = px[x, y][:3]
            px[x, y] = (max(0, min(255, r+n)), max(0, min(255, g+n)), max(0, min(255, b+n)))
    return img

def signature(draw, p):
    # Petit trait or centre en bas
    bar_w = 60 * SCALE
    bar_h = 3 * SCALE
    draw.rectangle([W//2 - bar_w//2, H - 18*SCALE, W//2 + bar_w//2, H - 18*SCALE + bar_h], fill=p["or"])
    # Tres petite ligne marine au-dessus, alignee
    line2_w = 25 * SCALE
    draw.rectangle([W//2 - line2_w//2, H - 30*SCALE, W//2 + line2_w//2, H - 30*SCALE + 2*SCALE],
                  fill=p["marine"])

# =============================================================
# 1. ASSURANCE-VIE 70 ANS : Sablier verre+or - palette AZUR
# =============================================================
def lumiere_sablier():
    p = PAL_AZUR
    img = smooth_gradient(p["bg_top"], p["bg_bot"])
    img = warm_glow(img, W//2, H//2, 600*SCALE, p["bg_accent"], 0.35)

    cx, cy = W//2, H//2 + 10*SCALE

    # Ombre portee
    def shadow(d, c):
        d.ellipse([cx - 100*SCALE, cy + 170*SCALE, cx + 100*SCALE, cy + 210*SCALE], fill=c)
    img = soft_shadow(img, shadow, blur=22*SCALE//2, offset=(0, 15*SCALE), alpha=60)
    draw = ImageDraw.Draw(img)

    # Sablier
    SAB_W = 90 * SCALE
    SAB_H = 160 * SCALE
    plate_h = 12 * SCALE
    plate_w = SAB_W + 25 * SCALE

    # Plateaux : effet bois sombre/or
    # Plateau haut
    draw.rectangle([cx - plate_w, cy - SAB_H - plate_h, cx + plate_w, cy - SAB_H], fill=p["or_fonce"])
    draw.rectangle([cx - plate_w, cy - SAB_H - plate_h, cx + plate_w, cy - SAB_H - plate_h + 4*SCALE], fill=p["or_clair"])
    draw.rectangle([cx - plate_w, cy - SAB_H - 2*SCALE, cx + plate_w, cy - SAB_H], fill=p["or"])
    # Plateau bas
    draw.rectangle([cx - plate_w, cy + SAB_H, cx + plate_w, cy + SAB_H + plate_h], fill=p["or_fonce"])
    draw.rectangle([cx - plate_w, cy + SAB_H + plate_h - 4*SCALE, cx + plate_w, cy + SAB_H + plate_h], fill=p["or"])
    draw.rectangle([cx - plate_w, cy + SAB_H, cx + plate_w, cy + SAB_H + 2*SCALE], fill=p["or_clair"])

    # 2 colonnes verticales (cotes du sablier)
    for x_off in [-plate_w + 5*SCALE, plate_w - 5*SCALE]:
        draw.rectangle([cx + x_off - 3*SCALE, cy - SAB_H + 2*SCALE,
                       cx + x_off + 3*SCALE, cy + SAB_H - 2*SCALE], fill=p["or"])
        # Highlight
        draw.rectangle([cx + x_off - 3*SCALE, cy - SAB_H + 2*SCALE,
                       cx + x_off - 1*SCALE, cy + SAB_H - 2*SCALE], fill=p["or_clair"])

    # Verre transparent (overlay)
    glass = Image.new("RGBA", (W, H), (0,0,0,0))
    g_draw = ImageDraw.Draw(glass)
    # Cone superieur
    verre_top = [
        (cx - SAB_W, cy - SAB_H + 5*SCALE),
        (cx + SAB_W, cy - SAB_H + 5*SCALE),
        (cx + 3*SCALE, cy),
        (cx - 3*SCALE, cy),
    ]
    g_draw.polygon(verre_top, fill=(255, 255, 255, 40), outline=(255, 255, 255, 180))
    # Cone inferieur
    verre_bot = [
        (cx - 3*SCALE, cy),
        (cx + 3*SCALE, cy),
        (cx + SAB_W, cy + SAB_H - 5*SCALE),
        (cx - SAB_W, cy + SAB_H - 5*SCALE),
    ]
    g_draw.polygon(verre_bot, fill=(255, 255, 255, 40), outline=(255, 255, 255, 180))
    # Highlights
    g_draw.line([(cx - SAB_W + 15*SCALE, cy - SAB_H + 15*SCALE),
                (cx - 5*SCALE, cy - 5*SCALE)], fill=(255, 255, 255, 200), width=int(2*SCALE))
    g_draw.line([(cx - 5*SCALE, cy + 5*SCALE),
                (cx - SAB_W + 15*SCALE, cy + SAB_H - 15*SCALE)], fill=(255, 255, 255, 200), width=int(2*SCALE))

    # Sable haut (en train de descendre - trapezoidal)
    h_sable_haut = 35 * SCALE
    sable_w_top = SAB_W * (h_sable_haut / SAB_H)
    for i in range(int(h_sable_haut), 0, -1):
        t = i / h_sable_haut
        w_now = sable_w_top * t + 3*SCALE
        y_now = cy - i
        color = lerp(p["or_fonce"], p["or_clair"], 1 - t * 0.6)
        draw.line([(cx - w_now, y_now), (cx + w_now, y_now)], fill=color, width=int(SCALE))

    # Sable accumule en bas (pyramide)
    h_sable_bas = 75 * SCALE
    sable_w_bas = SAB_W * 0.92
    for i in range(int(h_sable_bas), 0, -1):
        t = i / h_sable_bas
        w_now = sable_w_bas * (1 - t)
        y_now = cy + SAB_H - 5*SCALE - i
        color = lerp(p["or_clair"], p["or"], t * 0.5)
        if w_now > 1:
            draw.line([(cx - w_now, y_now), (cx + w_now, y_now)], fill=color, width=int(SCALE))

    # Fil de sable qui s'ecoule (tres fin)
    for i in range(0, int(SAB_H * 0.35)):
        y_fil = cy + i
        # legere variation pour aspect tactile
        draw.line([(cx - 1, y_fil), (cx + 1, y_fil)], fill=p["or"], width=1)

    img.paste(glass, (0, 0), glass)
    draw = ImageDraw.Draw(img)
    signature(draw, p)
    img = subtle_noise(img, 2)

    final = downscale(img)
    final.save(os.path.join(OUT_DIR, "01-assurance-vie-sablier-azur.png"), "PNG", optimize=True)
    print(f"OK 01 sablier {p['name']}")

# =============================================================
# 2. SUCCESSION INTERNATIONALE : Boussole detaillee - palette PAON
# =============================================================
def lumiere_boussole():
    p = PAL_PAON
    img = smooth_gradient(p["bg_top"], p["bg_bot"])
    img = warm_glow(img, W//2, H//2, 550*SCALE, p["bg_accent"], 0.30)

    cx, cy = W//2, H//2

    # Carte filigrane en arriere-plan (lignes tres subtiles)
    map_overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    md = ImageDraw.Draw(map_overlay)
    for x_off in range(-W//2 + 60*SCALE, W//2 - 30*SCALE, 80*SCALE):
        md.line([(cx + x_off, 20*SCALE), (cx + x_off, H - 20*SCALE)], fill=(*p["marine"], 25), width=1)
    for y_off in range(-H//2 + 60*SCALE, H//2 - 30*SCALE, 80*SCALE):
        md.line([(20*SCALE, cy + y_off), (W - 20*SCALE, cy + y_off)], fill=(*p["marine"], 25), width=1)
    img.paste(map_overlay, (0, 0), map_overlay)
    draw = ImageDraw.Draw(img)

    # Ombre boussole
    R_OUT = 195 * SCALE
    def shadow_compass(d, c):
        d.ellipse([cx - R_OUT, cy + R_OUT - 5*SCALE,
                  cx + R_OUT, cy + R_OUT + 30*SCALE], fill=c)
    img = soft_shadow(img, shadow_compass, blur=30*SCALE//2, offset=(0, 25*SCALE), alpha=85)
    draw = ImageDraw.Draw(img)

    # Boitier extérieur de la boussole (or avec relief)
    for r in range(int(R_OUT), int(R_OUT - 28*SCALE), -1):
        t = (R_OUT - r) / (28*SCALE)
        color = lerp(p["or"], p["or_clair"], t * 0.6)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=int(2*SCALE))

    # Cadran interieur (creme tres clair)
    R_IN = R_OUT - 28*SCALE
    draw.ellipse([cx - R_IN, cy - R_IN, cx + R_IN, cy + R_IN], fill=p["blanc"])

    # Bordure decorative
    R_DECO = R_IN - 8*SCALE
    draw.ellipse([cx - R_DECO, cy - R_DECO, cx + R_DECO, cy + R_DECO],
                outline=p["or"], width=int(2*SCALE))

    # 4 lettres cardinales NSEW (forme rose des vents stylisee)
    # 4 grandes pointes triangulaires
    for angle_deg, color in [(0, p["or_fonce"]), (90, p["or"]), (180, p["or"]), (270, p["or"])]:
        ang = math.radians(angle_deg - 90)
        # Grande pointe
        tip = (cx + (R_DECO - 18*SCALE) * math.cos(ang),
               cy + (R_DECO - 18*SCALE) * math.sin(ang))
        # Cote 1 et 2
        ang_l = ang + math.pi/16
        ang_r = ang - math.pi/16
        side1 = (cx + 20*SCALE * math.cos(ang_l), cy + 20*SCALE * math.sin(ang_l))
        side2 = (cx + 20*SCALE * math.cos(ang_r), cy + 20*SCALE * math.sin(ang_r))
        draw.polygon([tip, side1, (cx, cy), side2], fill=color)
        # Highlight (ligne plus claire d'un cote)
        draw.line([tip, side1], fill=p["or_clair"], width=int(2*SCALE))

    # 4 petites pointes intermediaires (NE, SE, SW, NW)
    for angle_deg in [45, 135, 225, 315]:
        ang = math.radians(angle_deg - 90)
        tip = (cx + (R_DECO - 50*SCALE) * math.cos(ang),
               cy + (R_DECO - 50*SCALE) * math.sin(ang))
        ang_l = ang + math.pi/20
        ang_r = ang - math.pi/20
        side1 = (cx + 15*SCALE * math.cos(ang_l), cy + 15*SCALE * math.sin(ang_l))
        side2 = (cx + 15*SCALE * math.cos(ang_r), cy + 15*SCALE * math.sin(ang_r))
        draw.polygon([tip, side1, (cx, cy), side2], fill=p["or_clair"])

    # Centre de la boussole : cabochon dore
    center_r = 14*SCALE
    draw.ellipse([cx - center_r, cy - center_r, cx + center_r, cy + center_r], fill=p["or_fonce"])
    draw.ellipse([cx - center_r + 3*SCALE, cy - center_r + 3*SCALE,
                 cx + center_r - 5*SCALE, cy + center_r - 5*SCALE], fill=p["or_clair"])

    # 4 letters NSEW (petits points or pres du bord)
    for angle_deg in [0, 90, 180, 270]:
        ang = math.radians(angle_deg - 90)
        x_p = cx + (R_DECO + 12*SCALE) * math.cos(ang)
        y_p = cy + (R_DECO + 12*SCALE) * math.sin(ang)
        # Cercle decoratif
        draw.ellipse([x_p - 4*SCALE, y_p - 4*SCALE, x_p + 4*SCALE, y_p + 4*SCALE],
                    fill=p["marine"])

    signature(draw, p)
    img = subtle_noise(img, 2)

    final = downscale(img)
    final.save(os.path.join(OUT_DIR, "02-succession-boussole-paon.png"), "PNG", optimize=True)
    print(f"OK 02 boussole {p['name']}")

# =============================================================
# 3. HOLDING : Cle ornee - palette CIEL
# =============================================================
def lumiere_cle():
    p = PAL_CIEL
    img = smooth_gradient(p["bg_top"], p["bg_bot"])
    img = warm_glow(img, W//2, H//2, 550*SCALE, p["bg_accent"], 0.30)
    draw = ImageDraw.Draw(img)

    cx, cy = W//2, H//2

    # Ombre de la cle
    def shadow_key(d, c):
        d.ellipse([cx - 290*SCALE, cy - 90*SCALE, cx - 165*SCALE, cy + 30*SCALE], fill=c)
        d.rectangle([cx - 200*SCALE, cy - 15*SCALE, cx + 270*SCALE, cy + 25*SCALE], fill=c)
        d.rectangle([cx + 195*SCALE, cy - 40*SCALE, cx + 270*SCALE, cy + 45*SCALE], fill=c)
    img = soft_shadow(img, shadow_key, blur=22*SCALE//2, offset=(10*SCALE, 20*SCALE), alpha=70)
    draw = ImageDraw.Draw(img)

    # Anneau de la cle (a gauche)
    anneau_cx = cx - 230*SCALE
    anneau_r_out = 85*SCALE
    anneau_r_in = 55*SCALE

    # Anneau exterieur avec gradient
    for r in range(int(anneau_r_out), int(anneau_r_in), -1):
        t = (anneau_r_out - r) / (anneau_r_out - anneau_r_in)
        color = lerp(p["or"], p["or_clair"], 0.3 + t * 0.5)
        draw.ellipse([anneau_cx - r, cy - r, anneau_cx + r, cy + r], outline=color, width=int(2*SCALE))

    # Cercle vide interieur (laisse voir le fond bleu)
    draw.ellipse([anneau_cx - anneau_r_in, cy - anneau_r_in,
                 anneau_cx + anneau_r_in, cy + anneau_r_in], fill=p["bg_top"])
    # Mais avec un petit anneau decoratif interieur
    draw.ellipse([anneau_cx - anneau_r_in, cy - anneau_r_in,
                 anneau_cx + anneau_r_in, cy + anneau_r_in], outline=p["or_clair"], width=int(2*SCALE))

    # 8 fleurons decoratifs autour
    for angle_deg in [60, 80, 100, 120, 240, 260, 280, 300]:
        ang = math.radians(angle_deg - 90)
        x1 = anneau_cx + anneau_r_out * math.cos(ang)
        y1 = cy + anneau_r_out * math.sin(ang)
        x2 = anneau_cx + (anneau_r_out + 14*SCALE) * math.cos(ang)
        y2 = cy + (anneau_r_out + 14*SCALE) * math.sin(ang)
        # Pointe
        draw.line([(x1, y1), (x2, y2)], fill=p["or"], width=int(3*SCALE))
        # Boule au bout
        draw.ellipse([x2 - 4*SCALE, y2 - 4*SCALE, x2 + 4*SCALE, y2 + 4*SCALE], fill=p["or"])

    # Tige de la cle avec relief
    tige_w = 24 * SCALE
    tige_start = anneau_cx + anneau_r_out - 5*SCALE
    tige_end = cx + 195*SCALE

    # Corps tige
    draw.rectangle([tige_start, cy - tige_w//2, tige_end + 15*SCALE, cy + tige_w//2], fill=p["or"])
    # Highlight haut
    draw.rectangle([tige_start, cy - tige_w//2, tige_end + 15*SCALE, cy - tige_w//2 + 4*SCALE], fill=p["or_clair"])
    # Ombre bas
    draw.rectangle([tige_start, cy + tige_w//2 - 4*SCALE, tige_end + 15*SCALE, cy + tige_w//2], fill=p["or_fonce"])

    # Element decoratif au milieu de la tige (anneau)
    mid_x = (tige_start + tige_end) / 2
    draw.rectangle([mid_x - 15*SCALE, cy - tige_w//2 - 8*SCALE,
                   mid_x + 15*SCALE, cy + tige_w//2 + 8*SCALE], fill=p["or"], outline=p["or_clair"], width=int(2*SCALE))

    # Panneton (a droite)
    pan_x = cx + 195*SCALE
    pan_w = 55*SCALE
    pan_h = 75*SCALE
    draw.rectangle([pan_x, cy - pan_h//2, pan_x + pan_w, cy + pan_h//2], fill=p["or"])
    draw.rectangle([pan_x, cy - pan_h//2, pan_x + pan_w, cy - pan_h//2 + 4*SCALE], fill=p["or_clair"])
    draw.rectangle([pan_x, cy + pan_h//2 - 4*SCALE, pan_x + pan_w, cy + pan_h//2], fill=p["or_fonce"])

    # Dents du panneton
    for dent_y, dent_h in [(cy - 25*SCALE, 18*SCALE), (cy + 5*SCALE, 22*SCALE), (cy + 30*SCALE, 12*SCALE)]:
        draw.rectangle([pan_x + pan_w, dent_y, pan_x + pan_w + 28*SCALE, dent_y + dent_h], fill=p["or"])
        draw.rectangle([pan_x + pan_w, dent_y, pan_x + pan_w + 28*SCALE, dent_y + 2*SCALE], fill=p["or_clair"])
        draw.rectangle([pan_x + pan_w, dent_y + dent_h - 2*SCALE, pan_x + pan_w + 28*SCALE, dent_y + dent_h], fill=p["or_fonce"])

    signature(draw, p)
    img = subtle_noise(img, 2)

    final = downscale(img)
    final.save(os.path.join(OUT_DIR, "03-holding-cle-ciel.png"), "PNG", optimize=True)
    print(f"OK 03 cle {p['name']}")

# =============================================================
# 4. PACTE DUTREIL : Sceau de cire avec ruban - palette GLACE
# =============================================================
def lumiere_sceau():
    p = PAL_GLACE
    img = smooth_gradient(p["bg_top"], p["bg_bot"])
    img = warm_glow(img, W//2, H//2, 500*SCALE, p["bg_accent"], 0.30)
    draw = ImageDraw.Draw(img)

    cx, cy = W//2, H//2 + 10*SCALE

    # Ruban dore qui passe derriere le sceau (forme S)
    ribbon_w = 38*SCALE
    ribbon_pts = []
    for t in range(0, 200):
        nt = t / 200
        x = 100*SCALE + (W - 200*SCALE) * nt
        y = cy + math.sin(nt * math.pi * 1.5) * 100*SCALE
        ribbon_pts.append((x, y))

    # Ruban en 3 passes pour relief
    for offset_w, color in [
        (ribbon_w, p["or_fonce"]),
        (ribbon_w - 8*SCALE, p["or"]),
        (ribbon_w - 18*SCALE, p["or_clair"]),
    ]:
        if offset_w > 0:
            for i in range(len(ribbon_pts)-1):
                draw.line([ribbon_pts[i], ribbon_pts[i+1]], fill=color, width=offset_w)

    # Sceau de cire (couleur marine au lieu de rouge pour rester dans la palette bleue)
    SCEAU_R = 135*SCALE
    # Sceau couleur : bleu marine fonce + reflets
    sceau_dark = (35, 60, 90)
    sceau_mid = (60, 90, 125)
    sceau_light = (95, 130, 165)
    sceau_high = (140, 175, 200)

    # Ombre portee
    def shadow_sceau(d, c):
        d.ellipse([cx - SCEAU_R, cy - SCEAU_R + 22*SCALE,
                  cx + SCEAU_R, cy + SCEAU_R + 22*SCALE], fill=c)
    img = soft_shadow(img, shadow_sceau, blur=22*SCALE//2, offset=(6*SCALE, 18*SCALE), alpha=110)
    draw = ImageDraw.Draw(img)

    # Sceau corps : degrade radial
    for r in range(int(SCEAU_R), 0, -1):
        t = r / SCEAU_R
        off_x = -int(20 * SCALE * (1-t))
        off_y = -int(20 * SCALE * (1-t))
        color = lerp(sceau_high, sceau_dark, t**1.3)
        draw.ellipse([cx - r + off_x, cy - r + off_y, cx + r + off_x, cy + r + off_y], fill=color)

    # Reflet brillant
    refl = Image.new("RGBA", (W, H), (0,0,0,0))
    rd = ImageDraw.Draw(refl)
    rd.ellipse([cx - 65*SCALE, cy - 75*SCALE, cx + 25*SCALE, cy - 30*SCALE],
              fill=(200, 220, 240, 120))
    refl = refl.filter(ImageFilter.GaussianBlur(20))
    img.paste(refl, (0, 0), refl)
    draw = ImageDraw.Draw(img)

    # Bord ouvrage (gauffrage exterieur)
    border_r = SCEAU_R - 18*SCALE
    draw.ellipse([cx - border_r, cy - border_r, cx + border_r, cy + border_r],
                outline=sceau_dark, width=int(3*SCALE))

    # Petits points en cercle decoratif autour du bord
    for deg in range(0, 360, 18):
        rad = math.radians(deg)
        x_d = cx + (border_r + 6*SCALE) * math.cos(rad)
        y_d = cy + (border_r + 6*SCALE) * math.sin(rad)
        draw.ellipse([x_d - 2*SCALE, y_d - 2*SCALE, x_d + 2*SCALE, y_d + 2*SCALE], fill=p["or_clair"])

    # Initiale C centrale (en or, en gros)
    initial_r = 55 * SCALE
    # Arc principal du C
    draw.arc([cx - initial_r, cy - initial_r, cx + initial_r, cy + initial_r], 35, 325,
            fill=p["or_clair"], width=int(12*SCALE))
    draw.arc([cx - initial_r + 3*SCALE, cy - initial_r + 3*SCALE,
             cx + initial_r - 3*SCALE, cy + initial_r - 3*SCALE], 35, 325,
            fill=p["or"], width=int(6*SCALE))
    # Highlight bord interieur
    draw.arc([cx - initial_r + 8*SCALE, cy - initial_r + 8*SCALE,
             cx + initial_r - 8*SCALE, cy + initial_r - 8*SCALE], 35, 325,
            fill=p["or_clair"], width=int(2*SCALE))

    # Serifs aux extremites du C
    end_top_x = cx + initial_r * math.cos(math.radians(35))
    end_top_y = cy + initial_r * math.sin(math.radians(35))
    end_bot_x = cx + initial_r * math.cos(math.radians(325))
    end_bot_y = cy + initial_r * math.sin(math.radians(325))
    draw.ellipse([end_top_x - 8*SCALE, end_top_y - 8*SCALE,
                 end_top_x + 8*SCALE, end_top_y + 8*SCALE], fill=p["or_clair"])
    draw.ellipse([end_bot_x - 8*SCALE, end_bot_y - 8*SCALE,
                 end_bot_x + 8*SCALE, end_bot_y + 8*SCALE], fill=p["or_clair"])

    signature(draw, p)
    img = subtle_noise(img, 2)

    final = downscale(img)
    final.save(os.path.join(OUT_DIR, "04-pacte-dutreil-sceau-glace.png"), "PNG", optimize=True)
    print(f"OK 04 sceau {p['name']}")

if __name__ == "__main__":
    lumiere_sablier()
    lumiere_boussole()
    lumiere_cle()
    lumiere_sceau()
    print("\nAll 4 'Lumiere notariale' saved in:", OUT_DIR)
