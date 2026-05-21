"""
Direction Finary-style adaptee Cellard : fond clair + objet metaphorique + or
"""
from PIL import Image, ImageDraw, ImageFilter
import os, math, random

OUT_DIR = r"C:\Users\francois.cellard\OneDrive - CELLARD NOTAIRES\Bureau\Claude 2026\Communication Cellard Notaires\article-photos-cna\charte-FINARY-STYLE"
os.makedirs(OUT_DIR, exist_ok=True)

SCALE = 2
W_FINAL, H_FINAL = 1280, 720
W, H = W_FINAL * SCALE, H_FINAL * SCALE

# Palettes claires inspirees Finary
PAL_IVOIRE = {
    "bg_top": (248, 242, 230),       # ivoire chaud
    "bg_bot": (235, 225, 205),        # sable doux
    "bg_accent": (245, 235, 215),
    "or_clair": (212, 175, 115),      # or doux
    "or": (185, 145, 80),             # or principal
    "or_fonce": (140, 100, 50),       # or accent profond
    "marine": (40, 55, 80),           # bleu marine accent
    "marine_dark": (25, 40, 65),
    "ombre": (180, 165, 140),
    "blanc": (255, 252, 245),
}

PAL_GRIS_PERLE = {
    "bg_top": (240, 240, 235),
    "bg_bot": (220, 220, 215),
    "bg_accent": (230, 230, 225),
    "or_clair": (218, 180, 120),
    "or": (190, 150, 85),
    "or_fonce": (145, 105, 55),
    "marine": (35, 50, 75),
    "marine_dark": (20, 35, 60),
    "ombre": (170, 170, 160),
    "blanc": (255, 255, 250),
}

PAL_SABLE = {
    "bg_top": (245, 232, 210),
    "bg_bot": (228, 210, 175),
    "bg_accent": (240, 225, 200),
    "or_clair": (215, 175, 110),
    "or": (180, 135, 65),
    "or_fonce": (135, 95, 40),
    "marine": (45, 60, 85),
    "marine_dark": (30, 45, 70),
    "ombre": (170, 145, 110),
    "blanc": (255, 250, 240),
}

def smooth_gradient_bg(top, bottom):
    img = Image.new("RGB", (W, H), top)
    px = img.load()
    for y in range(H):
        t = y / H
        t = (1 - math.cos(t * math.pi)) / 2
        r = int(top[0] * (1-t) + bottom[0] * t)
        g = int(top[1] * (1-t) + bottom[1] * t)
        b = int(top[2] * (1-t) + bottom[2] * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img

def radial_warm(img, cx, cy, max_r, color, intensity=0.3):
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    steps = 40
    for i in range(steps, 0, -1):
        r = int(max_r * i / steps)
        alpha = int(255 * intensity * (1 - i/steps) ** 2)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*color, alpha))
    overlay = overlay.filter(ImageFilter.GaussianBlur(50))
    img.paste(overlay, (0, 0), overlay)
    return img

def soft_shadow(img, shape_func, blur=30, offset=(0, 25), alpha=80):
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

def signature_minimal(draw, p):
    # Discrete signature en bas
    bar_w = 3 * SCALE
    draw.rectangle([W//2 - 30*SCALE, H - 12*SCALE, W//2 + 30*SCALE, H - 9*SCALE], fill=p["or"])

# =============================================================
# 1. ASSURANCE-VIE 70 ANS : Sablier de verre avec sable dore - IVOIRE
# =============================================================
def fy_sablier():
    p = PAL_IVOIRE
    img = smooth_gradient_bg(p["bg_top"], p["bg_bot"])
    img = radial_warm(img, W//2, H//2, 500*SCALE, p["or_clair"], 0.15)

    cx, cy = W//2, H//2 + 10*SCALE

    # Ombre portee sous le sablier
    def shadow_shape(draw, color):
        draw.ellipse([cx - 130*SCALE, cy + 165*SCALE,
                     cx + 130*SCALE, cy + 200*SCALE], fill=color)
    img = soft_shadow(img, shadow_shape, blur=25*SCALE//2, offset=(0, 20*SCALE), alpha=70)
    draw = ImageDraw.Draw(img)

    # Sablier - structure : 2 plateaux + 2 cones inverses
    SAB_W = 90 * SCALE
    SAB_H = 160 * SCALE

    # Plateaux haut et bas (en bois sombre / or)
    plate_h = 12 * SCALE
    plate_w = SAB_W + 25 * SCALE
    # Plateau haut
    draw.rectangle([cx - plate_w, cy - SAB_H - plate_h, cx + plate_w, cy - SAB_H], fill=p["or_fonce"])
    draw.rectangle([cx - plate_w, cy - SAB_H - plate_h, cx + plate_w, cy - SAB_H - plate_h + 4*SCALE], fill=p["or"])
    # Plateau bas
    draw.rectangle([cx - plate_w, cy + SAB_H, cx + plate_w, cy + SAB_H + plate_h], fill=p["or_fonce"])
    draw.rectangle([cx - plate_w, cy + SAB_H + plate_h - 4*SCALE, cx + plate_w, cy + SAB_H + plate_h], fill=p["or"])

    # 4 colonnes verticales (style sablier)
    for x_off in [-plate_w + 5*SCALE, plate_w - 5*SCALE]:
        draw.rectangle([cx + x_off - 3*SCALE, cy - SAB_H + 2*SCALE,
                       cx + x_off + 3*SCALE, cy + SAB_H - 2*SCALE], fill=p["or_fonce"])

    # Verre du sablier (en dessin transparent simulant la pluie de lumiere)
    # Cone superieur (verre vide ou presque)
    verre_top = [
        (cx - SAB_W, cy - SAB_H + 5*SCALE),
        (cx + SAB_W, cy - SAB_H + 5*SCALE),
        (cx + 3*SCALE, cy),
        (cx - 3*SCALE, cy),
    ]
    # Reflet de verre clair (highlight gauche)
    glass_overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    g_draw = ImageDraw.Draw(glass_overlay)
    g_draw.polygon(verre_top, fill=(255, 250, 235, 60), outline=(255, 245, 215, 200))
    # Highlight verre
    g_draw.line([(cx - SAB_W + 15*SCALE, cy - SAB_H + 15*SCALE),
                (cx - 5*SCALE, cy - 5*SCALE)], fill=(255, 250, 240, 180), width=int(2*SCALE))

    # Sable restant en haut
    h_sable = 35 * SCALE
    # Calcul des points du trapezoide de sable
    # Le sable est dans la partie basse du cone superieur
    sable_top_w = SAB_W * (h_sable / SAB_H)
    sable_top_y = cy - h_sable
    sable_points_haut = [
        (cx - sable_top_w, sable_top_y),
        (cx + sable_top_w, sable_top_y),
        (cx + 3*SCALE, cy),
        (cx - 3*SCALE, cy),
    ]
    # Sable degrade
    for i in range(int(h_sable), 0, -1):
        t = i / h_sable
        w_now = sable_top_w * t + 3*SCALE
        y_now = cy - i
        color = lerp(p["or_fonce"], p["or_clair"], 1 - t * 0.7)
        draw.line([(cx - w_now, y_now), (cx + w_now, y_now)], fill=color, width=int(SCALE))

    # Cone inferieur
    verre_bot = [
        (cx - 3*SCALE, cy),
        (cx + 3*SCALE, cy),
        (cx + SAB_W, cy + SAB_H - 5*SCALE),
        (cx - SAB_W, cy + SAB_H - 5*SCALE),
    ]
    g_draw.polygon(verre_bot, fill=(255, 250, 235, 60), outline=(255, 245, 215, 200))
    g_draw.line([(cx - 5*SCALE, cy + 5*SCALE),
                (cx - SAB_W + 15*SCALE, cy + SAB_H - 15*SCALE)], fill=(255, 250, 240, 180), width=int(2*SCALE))

    # Sable accumule en bas (forme pyramide)
    h_sable_bas = 70 * SCALE
    sable_bot_w = SAB_W * 0.95
    for i in range(int(h_sable_bas), 0, -1):
        t = i / h_sable_bas
        w_now = sable_bot_w * (1 - t)
        y_now = cy + SAB_H - 5*SCALE - i
        color = lerp(p["or_clair"], p["or_fonce"], t * 0.6)
        if w_now > 1:
            draw.line([(cx - w_now, y_now), (cx + w_now, y_now)], fill=color, width=int(SCALE))

    # Sable qui s'ecoule (fil tres fin)
    for i in range(0, int(SAB_H * 0.3)):
        y_fil = cy + i
        draw.line([(cx - 1, y_fil), (cx + 1, y_fil)], fill=p["or"], width=1)

    img.paste(glass_overlay, (0, 0), glass_overlay)
    draw = ImageDraw.Draw(img)
    signature_minimal(draw, p)
    img = subtle_noise(img, 3)

    final = downscale(img)
    p_out = os.path.join(OUT_DIR, "01-sablier-assurance-vie.png")
    final.save(p_out, "PNG", optimize=True)
    print("OK 01 sablier")

# =============================================================
# 2. SUCCESSION INTERNATIONALE : Boussole + carte stylisee - SABLE
# =============================================================
def fy_boussole():
    p = PAL_SABLE
    img = smooth_gradient_bg(p["bg_top"], p["bg_bot"])
    img = radial_warm(img, W//2, H//2, 550*SCALE, p["or_clair"], 0.18)

    cx, cy = W//2, H//2

    # Lignes/meridiens de carte (subtiles, sur tout le fond)
    map_overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    md = ImageDraw.Draw(map_overlay)
    # Lignes verticales (meridiens)
    for x_off in range(-W//2 + 80*SCALE, W//2 - 50*SCALE, 100*SCALE):
        md.line([(cx + x_off, 30*SCALE), (cx + x_off, H - 30*SCALE)], fill=(*p["or"], 30), width=1)
    # Lignes horizontales (paralleles)
    for y_off in range(-H//2 + 80*SCALE, H//2 - 50*SCALE, 100*SCALE):
        md.line([(30*SCALE, cy + y_off), (W - 30*SCALE, cy + y_off)], fill=(*p["or"], 30), width=1)
    img.paste(map_overlay, (0, 0), map_overlay)
    draw = ImageDraw.Draw(img)

    # Ombre portee de la boussole
    R_OUT = 200 * SCALE
    def shadow_compass(d, c):
        d.ellipse([cx - R_OUT, cy + R_OUT - 5*SCALE,
                  cx + R_OUT, cy + R_OUT + 25*SCALE], fill=c)
    img = soft_shadow(img, shadow_compass, blur=35*SCALE//2, offset=(0, 30*SCALE), alpha=90)
    draw = ImageDraw.Draw(img)

    # Boussole : cercle exterieur en or epais avec relief
    for r_inner in range(int(R_OUT), int(R_OUT - 25*SCALE), -1):
        t = (R_OUT - r_inner) / (25*SCALE)
        color = lerp(p["or"], p["or_clair"], t)
        draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner],
                    outline=color, width=int(2*SCALE))

    # Cercle interieur (cadran ivoire)
    R_IN = R_OUT - 25*SCALE
    draw.ellipse([cx - R_IN, cy - R_IN, cx + R_IN, cy + R_IN], fill=p["bg_accent"])

    # Cercle decoratif interieur
    R_DECO = R_IN - 10*SCALE
    draw.ellipse([cx - R_DECO, cy - R_DECO, cx + R_DECO, cy + R_DECO],
                outline=p["or"], width=int(2*SCALE))

    # Graduations N S E W (4 grandes) + 12 petites
    for i in range(36):
        angle = math.radians(i * 10 - 90)
        is_main = i % 9 == 0
        if is_main:
            r_start = R_DECO - 8*SCALE
            r_end = R_DECO - 35*SCALE
            line_w = int(3*SCALE)
            color = p["or_fonce"]
        elif i % 3 == 0:
            r_start = R_DECO - 8*SCALE
            r_end = R_DECO - 20*SCALE
            line_w = int(2*SCALE)
            color = p["or"]
        else:
            r_start = R_DECO - 8*SCALE
            r_end = R_DECO - 13*SCALE
            line_w = int(1*SCALE)
            color = p["or_clair"]
        x1 = cx + r_start * math.cos(angle)
        y1 = cy + r_start * math.sin(angle)
        x2 = cx + r_end * math.cos(angle)
        y2 = cy + r_end * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=line_w)

    # Aiguille de la boussole (en losange or)
    # Pointe nord (rouge sombre Pour Cellard : marine), Pointe sud (or pale)
    needle_len = R_DECO - 50*SCALE
    needle_w = 12 * SCALE
    # Calcul angle : pointe vers le NE (transmission a travers le monde)
    angle_deg = -65
    angle_rad = math.radians(angle_deg)
    # Centre de l'aiguille
    nx = math.cos(angle_rad)
    ny = math.sin(angle_rad)
    # Perpendiculaire
    px_perp = -ny * needle_w
    py_perp = nx * needle_w
    # Pointe nord (couleur marine - direction)
    pts_north = [
        (cx + nx * needle_len, cy + ny * needle_len),
        (cx + px_perp, cy + py_perp),
        (cx + nx * 5*SCALE, cy + ny * 5*SCALE),
    ]
    draw.polygon(pts_north, fill=p["marine"])
    # Pointe sud (or pale)
    pts_south = [
        (cx - nx * needle_len * 0.8, cy - ny * needle_len * 0.8),
        (cx - px_perp, cy - py_perp),
        (cx - nx * 5*SCALE, cy - ny * 5*SCALE),
    ]
    draw.polygon(pts_south, fill=p["or_clair"])
    # Triangle pointe au-dessus (highlight)
    pts_high = [
        (cx + nx * needle_len, cy + ny * needle_len),
        (cx + nx * needle_len * 0.5 + px_perp * 0.3, cy + ny * needle_len * 0.5 + py_perp * 0.3),
        (cx + nx * needle_len * 0.5, cy + ny * needle_len * 0.5),
    ]
    draw.polygon(pts_high, fill=p["marine_dark"])

    # Centre de l'aiguille : petit cercle dore
    draw.ellipse([cx - 12*SCALE, cy - 12*SCALE, cx + 12*SCALE, cy + 12*SCALE],
                fill=p["or_fonce"], outline=p["or_clair"], width=int(2*SCALE))
    draw.ellipse([cx - 5*SCALE, cy - 5*SCALE, cx + 5*SCALE, cy + 5*SCALE], fill=p["or_clair"])

    signature_minimal(draw, p)
    img = subtle_noise(img, 3)

    final = downscale(img)
    p_out = os.path.join(OUT_DIR, "02-boussole-succession.png")
    final.save(p_out, "PNG", optimize=True)
    print("OK 02 boussole")

# =============================================================
# 3. HOLDING : Cle ancienne ouvragee - GRIS PERLE
# =============================================================
def fy_cle():
    p = PAL_GRIS_PERLE
    img = smooth_gradient_bg(p["bg_top"], p["bg_bot"])
    img = radial_warm(img, W//2, H//2, 500*SCALE, p["or_clair"], 0.20)
    draw = ImageDraw.Draw(img)

    cx, cy = W//2, H//2

    # Ombre portee de la cle (allongee, diagonale)
    def shadow_key(d, c):
        # Anneau
        d.ellipse([cx - 320*SCALE, cy - 90*SCALE,
                  cx - 180*SCALE, cy + 50*SCALE], fill=c)
        # Tige
        d.rectangle([cx - 200*SCALE, cy - 15*SCALE,
                    cx + 280*SCALE, cy + 15*SCALE], fill=c)
        # Panneton
        d.rectangle([cx + 200*SCALE, cy - 40*SCALE,
                    cx + 280*SCALE, cy + 40*SCALE], fill=c)
    img = soft_shadow(img, shadow_key, blur=25*SCALE//2, offset=(15*SCALE, 25*SCALE), alpha=85)
    draw = ImageDraw.Draw(img)

    # Cle - anneau (couronne ouvragee a gauche)
    anneau_cx = cx - 250*SCALE
    anneau_r_out = 80*SCALE
    anneau_r_in = 50*SCALE

    # Anneau exterieur (degrade radial pour effet 3D)
    for r in range(int(anneau_r_out), int(anneau_r_in - 2), -1):
        t = (anneau_r_out - r) / (anneau_r_out - anneau_r_in + 2)
        color = lerp(p["or"], p["or_clair"], t * 0.7)
        draw.ellipse([anneau_cx - r, cy - r, anneau_cx + r, cy + r], outline=color, width=int(2*SCALE))

    # Cercle vide interieur de l'anneau
    draw.ellipse([anneau_cx - anneau_r_in, cy - anneau_r_in,
                 anneau_cx + anneau_r_in, cy + anneau_r_in], fill=p["bg_top"])

    # Ornements sur l'anneau : 4 petites pointes
    for angle_deg in [-45, 45, 135, -135, 90, -90, 0, 180]:
        angle_rad = math.radians(angle_deg)
        # On filtre pour ne pas chevaucher la tige (angle 0 = vers la tige)
        if abs(angle_deg) > 30 and abs(angle_deg) < 150:
            x1 = anneau_cx + anneau_r_out * math.cos(angle_rad)
            y1 = cy + anneau_r_out * math.sin(angle_rad)
            x2 = anneau_cx + (anneau_r_out + 12*SCALE) * math.cos(angle_rad)
            y2 = cy + (anneau_r_out + 12*SCALE) * math.sin(angle_rad)
            draw.line([(x1, y1), (x2, y2)], fill=p["or_fonce"], width=int(3*SCALE))
            draw.ellipse([x2 - 5*SCALE, y2 - 5*SCALE, x2 + 5*SCALE, y2 + 5*SCALE], fill=p["or_fonce"])

    # Tige de la cle (avec degrade en relief)
    tige_w = 22 * SCALE
    tige_start = anneau_cx + anneau_r_out - 5*SCALE
    tige_end = cx + 200*SCALE
    # Effet 3D : 3 couches (sombre/medium/clair)
    for offset_y, color in [(-2*SCALE, p["or_clair"]), (0, p["or"]), (tige_w//2 - 2*SCALE, p["or_fonce"])]:
        draw.rectangle([tige_start, cy - tige_w//2, tige_end + 20*SCALE, cy + tige_w//2 - offset_y*2],
                      fill=p["or"])
    # Highlight haut
    draw.rectangle([tige_start, cy - tige_w//2 + 2*SCALE,
                   tige_end + 20*SCALE, cy - tige_w//2 + 4*SCALE], fill=p["or_clair"])
    # Ombre bas
    draw.rectangle([tige_start, cy + tige_w//2 - 5*SCALE,
                   tige_end + 20*SCALE, cy + tige_w//2 - 2*SCALE], fill=p["or_fonce"])

    # Panneton (a droite)
    pan_x = cx + 200*SCALE
    pan_w = 50*SCALE
    pan_h = 65*SCALE
    # Bloc principal
    draw.rectangle([pan_x, cy - pan_h//2, pan_x + pan_w, cy + pan_h//2], fill=p["or"])
    draw.rectangle([pan_x, cy - pan_h//2 + 2*SCALE, pan_x + pan_w, cy - pan_h//2 + 5*SCALE], fill=p["or_clair"])
    draw.rectangle([pan_x, cy + pan_h//2 - 5*SCALE, pan_x + pan_w, cy + pan_h//2 - 2*SCALE], fill=p["or_fonce"])

    # 3 dents
    for dent_y_off, dent_h in [(-20*SCALE, 18*SCALE), (5*SCALE, 22*SCALE), (28*SCALE, 14*SCALE)]:
        draw.rectangle([pan_x + pan_w, cy - tige_w//2 + dent_y_off,
                       pan_x + pan_w + 25*SCALE, cy - tige_w//2 + dent_y_off + dent_h], fill=p["or"])
        draw.rectangle([pan_x + pan_w, cy - tige_w//2 + dent_y_off,
                       pan_x + pan_w + 25*SCALE, cy - tige_w//2 + dent_y_off + 2*SCALE], fill=p["or_clair"])

    signature_minimal(draw, p)
    img = subtle_noise(img, 3)

    final = downscale(img)
    p_out = os.path.join(OUT_DIR, "03-cle-holding.png")
    final.save(p_out, "PNG", optimize=True)
    print("OK 03 cle")

# =============================================================
# 4. PACTE DUTREIL : Sceau de cire avec ruban dore - SABLE
# =============================================================
def fy_sceau():
    p = PAL_SABLE
    img = smooth_gradient_bg(p["bg_top"], p["bg_bot"])
    img = radial_warm(img, W//2, H//2, 500*SCALE, p["or_clair"], 0.15)
    draw = ImageDraw.Draw(img)

    cx, cy = W//2, H//2 + 20*SCALE

    # Ruban dore qui passe derriere le sceau
    # Le ruban en S derriere
    ribbon_w = 35*SCALE
    ribbon_pts = []
    for t in range(0, 200):
        nt = t / 200
        x = 100*SCALE + (W - 200*SCALE) * nt
        # Forme en S autour du sceau
        y = cy + math.sin(nt * math.pi * 1.5) * 90*SCALE
        ribbon_pts.append((x, y))

    # Dessiner le ruban (sous le sceau)
    for offset_w, color in [
        (ribbon_w, p["or_fonce"]),
        (ribbon_w - 6*SCALE, p["or"]),
        (ribbon_w - 14*SCALE, p["or_clair"]),
    ]:
        if offset_w > 0:
            for i in range(len(ribbon_pts)-1):
                draw.line([ribbon_pts[i], ribbon_pts[i+1]], fill=color, width=offset_w)

    # Sceau de cire (cercle rouge profond) avec relief 3D
    SCEAU_R = 130*SCALE

    # Ombre portee du sceau
    def shadow_sceau(d, c):
        d.ellipse([cx - SCEAU_R, cy - SCEAU_R + 20*SCALE,
                  cx + SCEAU_R, cy + SCEAU_R + 20*SCALE], fill=c)
    img = soft_shadow(img, shadow_sceau, blur=20*SCALE//2, offset=(5*SCALE, 18*SCALE), alpha=120)
    draw = ImageDraw.Draw(img)

    # Sceau corps - couleur "cire" : entre marine fonce et or
    sceau_dark = (90, 30, 25)      # rouge bordeaux fonce (cire)
    sceau_mid = (140, 60, 45)
    sceau_light = (185, 90, 65)
    sceau_high = (220, 130, 95)

    # Cercle exterieur (bord du sceau) - relief
    for r in range(int(SCEAU_R), 0, -1):
        t = r / SCEAU_R
        # Decalage du centre pour effet 3D
        off_x = -int(20 * SCALE * (1-t))
        off_y = -int(20 * SCALE * (1-t))
        color = lerp(sceau_high, sceau_dark, t**1.3)
        draw.ellipse([cx - r + off_x, cy - r + off_y, cx + r + off_x, cy + r + off_y], fill=color)

    # Reflets et highlights
    refl = Image.new("RGBA", (W, H), (0,0,0,0))
    rd = ImageDraw.Draw(refl)
    rd.ellipse([cx - 60*SCALE, cy - 70*SCALE, cx + 30*SCALE, cy - 30*SCALE],
              fill=(255, 200, 170, 100))
    refl = refl.filter(ImageFilter.GaussianBlur(15))
    img.paste(refl, (0, 0), refl)
    draw = ImageDraw.Draw(img)

    # Bord ouvrage exterieur (sceau gauffrage)
    border_r = SCEAU_R - 18*SCALE
    draw.ellipse([cx - border_r, cy - border_r, cx + border_r, cy + border_r],
                outline=sceau_dark, width=int(3*SCALE))

    # Initiale "C" stylisee au centre (Cellard)
    initial_size = 80 * SCALE
    # C en arc avec relief or
    arc_r = initial_size // 2
    # Background du C : cercle ouvert
    draw.arc([cx - arc_r, cy - arc_r, cx + arc_r, cy + arc_r], 30, 330,
            fill=p["or_clair"], width=int(10*SCALE))
    draw.arc([cx - arc_r + 2*SCALE, cy - arc_r + 2*SCALE,
             cx + arc_r - 2*SCALE, cy + arc_r - 2*SCALE], 30, 330,
            fill=p["or"], width=int(5*SCALE))

    # Petites decorations autour du C
    for angle_deg in [-30, 30, 150, -150, 90, -90]:
        if abs(angle_deg) != 90:
            angle_rad = math.radians(angle_deg)
            x_dot = cx + (arc_r + 18*SCALE) * math.cos(angle_rad)
            y_dot = cy + (arc_r + 18*SCALE) * math.sin(angle_rad)
            draw.ellipse([x_dot - 3*SCALE, y_dot - 3*SCALE,
                         x_dot + 3*SCALE, y_dot + 3*SCALE], fill=p["or"])

    signature_minimal(draw, p)
    img = subtle_noise(img, 3)

    final = downscale(img)
    p_out = os.path.join(OUT_DIR, "04-sceau-pacte-dutreil.png")
    final.save(p_out, "PNG", optimize=True)
    print("OK 04 sceau")

if __name__ == "__main__":
    fy_sablier()
    fy_boussole()
    fy_cle()
    fy_sceau()
    print("\nAll 4 Finary-style saved in:", OUT_DIR)
