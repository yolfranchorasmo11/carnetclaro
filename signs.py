"""Biblioteca de señales dibujadas a mano en SVG (sin imágenes externas ni de pago).
Colores aproximados a la señalización española. Cada función devuelve un <svg> completo."""

ROJO = "#c8102e"
AZUL = "#0a55a6"
AMARILLO = "#f2b705"
NEGRO = "#1c2024"
BLANCO = "#ffffff"


def _svg(cuerpo, titulo):
    return (
        f'<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{titulo}"><title>{titulo}</title>{cuerpo}</svg>'
    )


def triangulo_peligro(interior="", fondo=BLANCO, titulo="Señal de peligro"):
    c = (
        f'<path d="M50 6 L95 88 Q96 92 92 92 L8 92 Q4 92 5 88 Z" fill="{ROJO}"/>'
        f'<path d="M50 24 L81 81 L19 81 Z" fill="{fondo}"/>' + interior
    )
    return _svg(c, titulo)


def otros_peligros(fondo=BLANCO, titulo="Otros peligros"):
    i = f'<rect x="46.5" y="40" width="7" height="24" rx="3" fill="{NEGRO}"/><circle cx="50" cy="72" r="4.2" fill="{NEGRO}"/>'
    return triangulo_peligro(i, fondo, titulo)


def curva_derecha():
    i = (f'<path d="M42 76 L42 58 Q42 46 54 44" stroke="{NEGRO}" stroke-width="7" fill="none" stroke-linecap="round"/>'
         f'<path d="M52 36 L64 44 L52 52 Z" fill="{NEGRO}"/>')
    return triangulo_peligro(i, BLANCO, "Curva peligrosa hacia la derecha")


def interseccion():
    i = (f'<rect x="46" y="38" width="8" height="40" fill="{NEGRO}"/>'
         f'<rect x="32" y="52" width="36" height="8" fill="{NEGRO}"/>')
    return triangulo_peligro(i, BLANCO, "Intersección con prioridad a la derecha")


def ceda_el_paso():
    c = (f'<path d="M8 12 Q4 12 6 16 L48 90 Q50 94 52 90 L94 16 Q96 12 92 12 Z" fill="{ROJO}"/>'
         f'<path d="M24 22 L76 22 L50 70 Z" fill="{BLANCO}"/>')
    return _svg(c, "Ceda el paso")


def stop():
    oct_ = "30,4 70,4 96,30 96,70 70,96 30,96 4,70 4,30"
    oct2 = "32,9 68,9 91,32 91,68 68,91 32,91 9,68 9,32"
    c = (f'<polygon points="{oct_}" fill="{BLANCO}"/><polygon points="{oct2}" fill="{ROJO}"/>'
         f'<text x="50" y="59" text-anchor="middle" font-family="Barlow Condensed, Arial Narrow, sans-serif" '
         f'font-weight="700" font-size="27" fill="{BLANCO}" letter-spacing="1">STOP</text>')
    return _svg(c, "Detención obligatoria (STOP)")


def entrada_prohibida():
    c = (f'<circle cx="50" cy="50" r="46" fill="{ROJO}"/>'
         f'<rect x="20" y="42" width="60" height="16" fill="{BLANCO}"/>')
    return _svg(c, "Entrada prohibida")


def velocidad_maxima(n=50):
    c = (f'<circle cx="50" cy="50" r="46" fill="{ROJO}"/><circle cx="50" cy="50" r="35" fill="{BLANCO}"/>'
         f'<text x="50" y="63" text-anchor="middle" font-family="Barlow Condensed, Arial Narrow, sans-serif" '
         f'font-weight="700" font-size="{38 if n < 100 else 32}" fill="{NEGRO}">{n}</text>')
    return _svg(c, f"Velocidad máxima {n} km/h")


def estacionamiento_prohibido():
    c = (f'<circle cx="50" cy="50" r="46" fill="{ROJO}"/><circle cx="50" cy="50" r="35" fill="{AZUL}"/>'
         f'<line x1="26" y1="26" x2="74" y2="74" stroke="{ROJO}" stroke-width="10"/>')
    return _svg(c, "Estacionamiento prohibido")


def parada_prohibida():
    c = (f'<circle cx="50" cy="50" r="46" fill="{ROJO}"/><circle cx="50" cy="50" r="35" fill="{AZUL}"/>'
         f'<line x1="26" y1="26" x2="74" y2="74" stroke="{ROJO}" stroke-width="10"/>'
         f'<line x1="74" y1="26" x2="26" y2="74" stroke="{ROJO}" stroke-width="10"/>')
    return _svg(c, "Parada y estacionamiento prohibidos")


def sentido_obligatorio():
    c = (f'<circle cx="50" cy="50" r="46" fill="{AZUL}"/>'
         f'<rect x="44" y="40" width="12" height="38" fill="{BLANCO}"/>'
         f'<path d="M50 18 L72 44 L28 44 Z" fill="{BLANCO}"/>')
    return _svg(c, "Sentido obligatorio")


def fin_prohibiciones():
    c = (f'<circle cx="50" cy="50" r="46" fill="{BLANCO}" stroke="{NEGRO}" stroke-width="2"/>'
         f'<clipPath id="fp"><circle cx="50" cy="50" r="44"/></clipPath>'
         f'<g clip-path="url(#fp)" stroke="{NEGRO}" stroke-width="3">'
         + "".join(f'<line x1="{10 + d}" y1="{90 + d}" x2="{90 + d}" y2="{10 + d}"/>' for d in (-12, -6, 0, 6, 12))
         + "</g>")
    return _svg(c, "Fin de prohibiciones")


def estacionamiento():
    c = (f'<rect x="6" y="6" width="88" height="88" rx="10" fill="{AZUL}"/>'
         f'<rect x="12" y="12" width="76" height="76" rx="6" fill="none" stroke="{BLANCO}" stroke-width="2.5"/>'
         f'<text x="50" y="72" text-anchor="middle" font-family="Barlow, Arial, sans-serif" font-weight="700" '
         f'font-size="58" fill="{BLANCO}">P</text>')
    return _svg(c, "Estacionamiento")


def calzada_prioridad():
    c = (f'<rect x="18" y="18" width="64" height="64" rx="4" transform="rotate(45 50 50)" fill="{BLANCO}" stroke="{NEGRO}" stroke-width="2"/>'
         f'<rect x="29" y="29" width="42" height="42" transform="rotate(45 50 50)" fill="{AMARILLO}"/>')
    return _svg(c, "Calzada con prioridad")


def obras_circunstancial():
    """Señal de peligro con fondo amarillo: circunstancial por obras (RD 465/2025)."""
    return otros_peligros(fondo=AMARILLO, titulo="Peligro circunstancial por obras (fondo amarillo)")


def logo():
    return (
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        f'<rect x="16" y="16" width="68" height="68" rx="8" transform="rotate(45 50 50)" fill="{BLANCO}"/>'
        f'<rect x="27" y="27" width="46" height="46" rx="3" transform="rotate(45 50 50)" fill="{AMARILLO}"/>'
        f'<path d="M38 51 L47 60 L63 42" stroke="{NEGRO}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        "</svg>"
    )


# Nombre -> función, para usar en artículos y tests como {{senal:nombre}}
CATALOGO = {
    "ceda": ceda_el_paso,
    "stop": stop,
    "entrada_prohibida": entrada_prohibida,
    "velocidad_30": lambda: velocidad_maxima(30),
    "velocidad_50": lambda: velocidad_maxima(50),
    "velocidad_90": lambda: velocidad_maxima(90),
    "velocidad_120": lambda: velocidad_maxima(120),
    "estacionamiento_prohibido": estacionamiento_prohibido,
    "parada_prohibida": parada_prohibida,
    "sentido_obligatorio": sentido_obligatorio,
    "fin_prohibiciones": fin_prohibiciones,
    "estacionamiento": estacionamiento,
    "calzada_prioridad": calzada_prioridad,
    "otros_peligros": otros_peligros,
    "curva_derecha": curva_derecha,
    "interseccion": interseccion,
    "obras": obras_circunstancial,
}
