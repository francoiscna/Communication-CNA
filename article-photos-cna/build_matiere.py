from PIL import Image, ImageDraw, ImageFilter, ImageChops
import os, math, random

OUT_DIR = r"C:\Users\francois.cellard\OneDrive - CELLARD NOTAIRES\Bureau\Claude 2026\Communication Cellard Notaires\article-photos-cna\charte-v3-matiere"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1280, 720

PALETTES = {
    "marine": {
        "bg_top": (10, 25, 45),
        "bg_bot": (25, 50, 80),
        "metal_dark": (140, 100, 50),
        "metal": (210, 165, 95),
        "metal_light": (240, 200, 130),
        "highlight": (255, 235, 180),
    },
    "petrole": {
        "bg_top": (15, 40, 50),
        "bg_bot": (35, 75, 85),
        "metal_dark": (130, 80, 60),
        "metal": (200, 135, 80),
        "metal_light": (235, 175, 110),
        "highlight": (255, 220, 160),
    },
    "minuit": {
        "bg_top": (15, 20, 50),
        "bg_bot": (40, 50, 90),
        "metal_dark": (110, 90, 130),
        "metal": (175, 145, 200),
        "metal_light": (215, 190, 235),
        "highlight": (255, 240, 255),
    },
    "carbone": {
        "bg_top": (15, 18, 25),
        "bg_bot": (45, 48, 60),
        "metal_dark": (130, 110, 60),
        "metal": (200, 170, 90),
        "metal_light": (240, 210, 130),
        "highlight": (255, 240, 180),
    },
}

def gradient_bg(top, bottom, w=W, h=H):
    img = Image.new("RGB", (w, h), top)
    px = img.load()
    for y in range(h):
        r = top[0] + int((bottom[0]-top[0]) * y / h)
        g = top[1] + int((bottom[1]-top[1]) * y / h)
        b = top[2] + int((bottom[2]-top[2]) * y / h)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img

def add_noise(img, intensity=8):
    """Texture matière subtile"""
    px = img.load()
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            n = random.randint(-intensity, intensity)
            r, g, b = px[x, y]
            px[x, y] = (max(0, min(255, r+n)), max(0, min(255, g+n)), max(0, min(255, b+n)))
    return img

def radial_glow(img, cx, cy, max_r, color, intensity=0.5):
    """Halo lumineux pour suggérer la matière qui reçoit la lumière"""
    px = img.load()
    for y in range(H):
        for x in range(W):
            d = math.sqrt((x-cx)**2 + (y-cy)**2)
            if d < max_r:
                t = (1 - d/max_r) ** 2
                old = px[x, y]
                r = int(old[0] + (color[0] - old[0]) * t * intensity)
                g = int(old[1] + (color[1] - old[1]) * t * intensity)
                b = int(old[2] + (color[2] - old[2]) * t * intensity)
                px[x, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def signature_bands(draw, p):
    draw.rectangle([0, 0, 3, H], fill=p["metal"])
    draw.rectangle([0, H-3, W, H], fill=p["metal"])

# ===================================================
# 1. CORDES TRESSÉES — palette MARINE (style proche du nœud original)
# Sujet : Pacte Dutreil — transmission / lien intergénérationnel
# ===================================================
def matiere_cordes(palette_name="marine"):
    p = PALETTES[palette_name]
    img = gradient_bg(p["bg_top"], p["bg_bot"])
    radial_glow(img, W//2, H//2, 500, p["highlight"], intensity=0.25)
    draw = ImageDraw.Draw(img)

    cx, cy = W//2, H//2 + 20
    # 3 cordes parallèles entrelacées (sin wave)
    NUM_STRANDS = 5
    STRAND_SPACING = 16
    AMPLITUDE = 75
    WAVELENGTH = 600
    THICKNESS = 28

    # Pour chaque corde, on dessine plusieurs lignes superposées en dégradé pour donner du volume
    base_y_offset = -(NUM_STRANDS-1) * STRAND_SPACING // 2

    # On dessine en plusieurs passes : ombre, milieu, highlight (effet relief)
    for strand_idx in range(NUM_STRANDS):
        y_offset = base_y_offset + strand_idx * STRAND_SPACING
        # Phase déphasée pour entrelacement
        phase = strand_idx * 0.3

        # Calculer les points de la courbe
        points = []
        for t in range(0, 300):
            x = 100 + (W - 200) * t / 300
            normalized_t = (x - 100) / (W - 200)
            y = cy + y_offset + math.sin(normalized_t * 2 * math.pi * 2 + phase) * AMPLITUDE
            points.append((x, y))

        # Dessiner chaque corde avec effet de volume (3 lignes superposées)
        for thickness_offset, color in [
            (THICKNESS, p["metal_dark"]),  # base/ombre
            (THICKNESS - 6, p["metal"]),    # milieu
            (THICKNESS - 14, p["metal_light"]),  # highlight
            (THICKNESS - 22, p["highlight"]),  # reflet
        ]:
            if thickness_offset > 0:
                for i in range(len(points)-1):
                    draw.line([points[i], points[i+1]], fill=color, width=thickness_offset)

    signature_bands(draw, p)
    add_noise(img, 5)

    p_out = os.path.join(OUT_DIR, f"01-cordes-{palette_name}.png")
    img.save(p_out, "PNG", optimize=True)
    print(f"OK 01 {palette_name}")
    return p_out

# ===================================================
# 2. ORBE EN RELIEF — palette PETROLE
# Sujet : Assurance-vie / Succession (protection, globalité)
# ===================================================
def matiere_orbe(palette_name="petrole"):
    p = PALETTES[palette_name]
    img = gradient_bg(p["bg_top"], p["bg_bot"])
    radial_glow(img, W//2 - 100, H//2 - 100, 600, p["highlight"], intensity=0.3)
    draw = ImageDraw.Draw(img)

    cx, cy = W//2, H//2
    R = 220

    # Effet sphère 3D : on dessine plusieurs cercles concentriques avec dégradé
    # Le bord est dans la palette métal_dark, le centre vers métal_light
    for radius in range(R, 0, -2):
        t = radius / R
        # Décaler le "centre apparent" en haut-gauche pour effet 3D
        offset_x = -int(40 * (1-t))
        offset_y = -int(40 * (1-t))
        # Couleur : du métal sombre (loin du centre lumineux) au métal clair (proche)
        color = lerp_color(p["highlight"], p["metal_dark"], t**1.5)
        draw.ellipse([cx - radius + offset_x, cy - radius + offset_y,
                     cx + radius + offset_x, cy + radius + offset_y],
                     fill=color)

    # Ombre portée sous l'orbe (ellipse aplatie)
    shadow = Image.new("RGBA", (W, H), (0,0,0,0))
    sh_draw = ImageDraw.Draw(shadow)
    sh_draw.ellipse([cx - R, cy + R + 5, cx + R, cy + R + 50], fill=(0,0,0,80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    img.paste(shadow, (0,0), shadow)
    draw = ImageDraw.Draw(img)

    # Méridien doré qui passe sur l'orbe
    arc_pts = []
    for i in range(101):
        t = i / 100
        y = cy - R + 2 * R * t
        # Demi-ellipse vue de face
        x_off = int(40 * math.sin(t * math.pi))
        arc_pts.append((cx + x_off, y))
    for i in range(len(arc_pts)-1):
        draw.line([arc_pts[i], arc_pts[i+1]], fill=p["highlight"], width=3)

    # Ligne équatoriale dorée
    eq_pts = []
    for i in range(101):
        t = i / 100
        x = cx - R + 2 * R * t
        y_off = int(35 * math.cos(t * math.pi))
        eq_pts.append((x, cy + y_off))
    for i in range(len(eq_pts)-1):
        draw.line([eq_pts[i], eq_pts[i+1]], fill=p["metal_light"], width=2)

    signature_bands(draw, p)
    add_noise(img, 5)

    p_out = os.path.join(OUT_DIR, f"02-orbe-{palette_name}.png")
    img.save(p_out, "PNG", optimize=True)
    print(f"OK 02 {palette_name}")
    return p_out

# ===================================================
# 3. ARCHE EN RELIEF — palette MINUIT (violet bleuté)
# Sujet : Holding / Patrimoine (architecture, structure)
# ===================================================
def matiere_arche(palette_name="minuit"):
    p = PALETTES[palette_name]
    img = gradient_bg(p["bg_top"], p["bg_bot"])
    radial_glow(img, W//2, H//2 - 150, 400, p["highlight"], intensity=0.25)
    draw = ImageDraw.Draw(img)

    cx, cy = W//2, H//2 + 80

    # Une grande arche en relief (style portique noble)
    arch_w = 380
    arch_h = 350

    # On dessine l'arche en couches concentriques pour effet 3D
    for offset in range(40, 0, -2):
        # Couleur en dégradé : sombre à l'extérieur, clair vers l'intérieur
        t = offset / 40
        color = lerp_color(p["metal_light"], p["metal_dark"], t)
        thickness = max(1, int(offset * 0.5))

        # Arche : 2 verticales + arc supérieur
        # Pilier gauche
        draw.line([(cx - arch_w + offset, cy + arch_h),
                  (cx - arch_w + offset, cy - arch_h//2)], fill=color, width=2)
        # Pilier droit
        draw.line([(cx + arch_w - offset, cy + arch_h),
                  (cx + arch_w - offset, cy - arch_h//2)], fill=color, width=2)
        # Arc supérieur
        arc_pts = []
        for i in range(101):
            angle_rad = math.radians(180 - i * 180/100)
            x = cx + (arch_w - offset) * math.cos(angle_rad)
            y = cy - arch_h//2 - (arch_w - offset) * math.sin(angle_rad) * 0.5
            arc_pts.append((x, y))
        for i in range(len(arc_pts)-1):
            draw.line([arc_pts[i], arc_pts[i+1]], fill=color, width=2)

    # Clé de voûte (pierre angulaire) en évidence : losange or
    keystone_h = 60
    draw.polygon([
        (cx, cy - arch_h//2 - arch_w//2 - 5),  # top
        (cx + 25, cy - arch_h//2 - arch_w//2 + keystone_h//2),  # right
        (cx, cy - arch_h//2 - arch_w//2 + keystone_h),  # bot
        (cx - 25, cy - arch_h//2 - arch_w//2 + keystone_h//2),  # left
    ], fill=p["metal_light"], outline=p["highlight"], width=2)

    # Sol/marches en bas
    for step_i in range(3):
        step_y = cy + arch_h + step_i * 12
        step_w = arch_w * 2 + 60 + step_i * 50
        # Dégradé selon profondeur (proche = clair, loin = sombre)
        t = step_i / 3
        color = lerp_color(p["metal_light"], p["metal_dark"], t)
        draw.rectangle([cx - step_w//2, step_y - 5, cx + step_w//2, step_y + 5], fill=color)

    signature_bands(draw, p)
    add_noise(img, 6)

    p_out = os.path.join(OUT_DIR, f"03-arche-{palette_name}.png")
    img.save(p_out, "PNG", optimize=True)
    print(f"OK 03 {palette_name}")
    return p_out

# ===================================================
# 4. STRATES SCULPTÉES — palette CARBONE (sombre + or)
# Sujet : Patrimoine / Strates / Capitalisation
# ===================================================
def matiere_strates(palette_name="carbone"):
    p = PALETTES[palette_name]
    img = gradient_bg(p["bg_top"], p["bg_bot"])
    radial_glow(img, W//2, H//2, 500, p["highlight"], intensity=0.2)
    draw = ImageDraw.Draw(img)

    cx, cy = W//2, H//2 + 100

    # Strates empilées (style sculpture en relief)
    # Chaque strate = ellipse aplatie avec ombre
    num_layers = 7
    base_w = 380
    layer_h = 35

    for i in range(num_layers):
        # De bas (large, sombre) à haut (étroit, clair)
        t = i / (num_layers - 1)
        w_lay = int(base_w - i * 35)
        y_lay = cy - i * (layer_h - 4)
        # Couleur : dégradé du sombre au clair vers le haut
        color = lerp_color(p["metal_dark"], p["highlight"], t)
        color_shade = lerp_color(p["bg_bot"], p["metal_dark"], t)

        # Ombre portée subtile
        if i > 0:
            sh = Image.new("RGBA", (W, H), (0,0,0,0))
            sh_draw = ImageDraw.Draw(sh)
            sh_draw.ellipse([cx - w_lay, y_lay + 2, cx + w_lay, y_lay + layer_h + 8],
                           fill=(0,0,0,60))
            sh = sh.filter(ImageFilter.GaussianBlur(5))
            img.paste(sh, (0,0), sh)
            draw = ImageDraw.Draw(img)

        # Strate principale (ellipse)
        draw.ellipse([cx - w_lay, y_lay, cx + w_lay, y_lay + layer_h],
                    fill=color, outline=p["highlight"], width=1)
        # Highlight supérieur (mini ellipse claire sur le haut de la strate)
        hi_w = int(w_lay * 0.7)
        draw.ellipse([cx - hi_w, y_lay + 3, cx + hi_w, y_lay + 10],
                    fill=p["highlight"])

    # Ligne or qui ascendante traverse les strates (le fil)
    fil_pts = []
    for i in range(50):
        t = i / 49
        x = cx + math.sin(t * math.pi * 1.5) * 25
        y = cy + 30 - t * (num_layers * (layer_h - 4) + 30)
        fil_pts.append((x, y))
    for i in range(len(fil_pts)-1):
        draw.line([fil_pts[i], fil_pts[i+1]], fill=p["highlight"], width=3)

    signature_bands(draw, p)
    add_noise(img, 4)

    p_out = os.path.join(OUT_DIR, f"04-strates-{palette_name}.png")
    img.save(p_out, "PNG", optimize=True)
    print(f"OK 04 {palette_name}")
    return p_out

# Generate all
random.seed(42)
matiere_cordes("marine")
matiere_orbe("petrole")
matiere_arche("minuit")
matiere_strates("carbone")
print("\nAll generated in:", OUT_DIR)
