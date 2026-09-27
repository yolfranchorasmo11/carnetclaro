#!/usr/bin/env python3
"""Generador estático de Carnet Claro.

Uso:  python3 build.py        -> genera la web completa en ./dist

Contenido:
  content/articulos/*.md   artículos (cabecera YAML + Markdown)
  content/tests/*.yaml     tests con explicación
  content/paginas/*.md     páginas legales e institucionales
  site.json                datos generales (nombre, dominio, AdSense...)
"""
import datetime as dt
import html
import json
import re
import shutil
from pathlib import Path

import markdown
import yaml

import signs

RAIZ = Path(__file__).parent
DIST = RAIZ / "dist"
import os
SITE = json.loads((RAIZ / "site.json").read_text(encoding="utf-8"))
# En Render se usa la dirección real del servidor hasta tener dominio propio
BASE = (os.environ.get("SITE_BASE_URL") or SITE["base_url"]).rstrip("/")

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
CATEGORIAS = {
    "examen": "Examen",
    "normas": "Normas",
    "senales": "Señales",
    "actualidad": "Actualidad",
}


def fecha_larga(d):
    if isinstance(d, str):
        d = dt.date.fromisoformat(d)
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def leer_md(ruta):
    texto = ruta.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", texto, re.S)
    if not m:
        raise ValueError(f"{ruta} no tiene cabecera YAML")
    meta = yaml.safe_load(m.group(1))
    return meta, m.group(2)


def figura_senal(m):
    nombre = m.group(1)
    pie = m.group(2)
    svg = signs.CATALOGO[nombre]()
    cap = f"<figcaption>{html.escape(pie)}</figcaption>" if pie else ""
    return f'<figure class="figura">{svg}{cap}</figure>'


def md_a_html(texto):
    # {{senal:nombre|pie de foto}} -> figura con la señal dibujada
    texto = re.sub(r"\{\{senal:([a-z0-9_]+)(?:\|([^}]*))?\}\}", figura_senal, texto)
    return markdown.markdown(texto, extensions=["tables", "md_in_html", "sane_lists", "attr_list"])


# ---------------------------------------------------------------- plantilla

def pagina(titulo, descripcion, ruta, cuerpo, activo="", extra_head="", tipo="website"):
    url = f"{BASE}{ruta}"
    titulo_completo = titulo if titulo == SITE["name"] else f"{titulo} | {SITE['name']}"
    adsense = ""
    if SITE.get("adsense_client"):
        adsense = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
                   f'{SITE["adsense_client"]}" crossorigin="anonymous"></script>')

    def enlace(href, texto, clave):
        cur = ' aria-current="page"' if clave == activo else ""
        return f'<a href="{href}"{cur}>{texto}</a>'

    menu = "".join([
        enlace("/tests/", "Tests", "tests"),
        enlace("/senales/", "Señales", "senales"),
        enlace("/articulos/", "Guías", "articulos"),
        enlace("/examen-teorico/", "El examen", "examen"),
    ])
    anio = dt.date.today().year
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo_completo)}</title>
<meta name="description" content="{html.escape(descripcion)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{tipo}">
<meta property="og:title" content="{html.escape(titulo)}">
<meta property="og:description" content="{html.escape(descripcion)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="es_ES">
<meta name="theme-color" content="#1c2024">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
{adsense}
{extra_head}
</head>
<body>
<header class="cabecera">
  <div class="contenedor">
    <a class="marca" href="/">{signs.logo()}<span>Carnet <b>Claro</b></span></a>
    <nav class="menu" aria-label="Principal">{menu}</nav>
  </div>
</header>
<main>
{cuerpo}
</main>
<footer class="pie">
  <div class="contenedor">
    <div>
      <h4>Carnet Claro</h4>
      <p>Guías, tests y señales del carnet de conducir en España, explicados con claridad y contrastados con la normativa oficial (DGT y BOE).</p>
      <button class="tema-btn" type="button">Cambiar modo claro / oscuro</button>
    </div>
    <div>
      <h4>Aprende</h4>
      <a href="/tests/">Tests con explicación</a>
      <a href="/senales/">Guía de señales</a>
      <a href="/articulos/">Todas las guías</a>
      <a href="/examen-teorico/">Cómo es el examen</a>
    </div>
    <div>
      <h4>El proyecto</h4>
      <a href="/sobre-nosotros/">Sobre Carnet Claro</a>
      <a href="/contacto/">Contacto</a>
      <a href="/aviso-legal/">Aviso legal</a>
      <a href="/privacidad/">Privacidad</a>
      <a href="/cookies/">Cookies</a>
    </div>
    <div class="legal">© {anio} Carnet Claro. Web informativa independiente, sin relación con la Dirección General de Tráfico. Ante cualquier duda, la referencia final es siempre la normativa publicada en el BOE y la información de la DGT.</div>
  </div>
</footer>
<script src="/app.js" defer></script>
</body>
</html>
"""


def tarjeta_articulo(a):
    cat = a["categoria"]
    return f"""<a class="tarjeta" href="/articulos/{a['slug']}/">
  <span class="categoria cat-{cat}">{CATEGORIAS[cat]}</span>
  <h3>{html.escape(a['titulo'])}</h3>
  <p>{html.escape(a['resumen'])}</p>
  <span class="meta">Revisado el {fecha_larga(a['revisado'])}</span>
</a>"""


def tarjeta_test(t):
    n = len(t["preguntas"])
    return f"""<a class="tarjeta" href="/tests/{t['slug']}/">
  <span class="categoria cat-examen">{n} preguntas</span>
  <h3>{html.escape(t['titulo'])}</h3>
  <p>{html.escape(t['descripcion'])}</p>
  <span class="meta">Cada respuesta, explicada</span>
</a>"""


# ---------------------------------------------------------------- generación

def escribir(ruta, contenido):
    destino = DIST / ruta.strip("/") / "index.html" if not ruta.endswith(".html") else DIST / ruta.strip("/")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido, encoding="utf-8")


def cargar_articulos():
    arts = []
    for f in sorted((RAIZ / "content/articulos").glob("*.md")):
        meta, cuerpo = leer_md(f)
        meta["cuerpo_html"] = md_a_html(cuerpo)
        meta["fecha"] = str(meta["fecha"])
        meta["revisado"] = str(meta.get("revisado", meta["fecha"]))
        if meta.get("borrador"):
            continue
        arts.append(meta)
    arts.sort(key=lambda a: (a["fecha"], a["slug"]), reverse=True)
    return arts


def cargar_tests():
    tests = []
    for f in sorted((RAIZ / "content/tests").glob("*.yaml")):
        t = yaml.safe_load(f.read_text(encoding="utf-8"))
        t["fecha"] = str(t["fecha"])
        tests.append(t)
    tests.sort(key=lambda t: t.get("orden", 99))
    return tests


def generar_articulo(a, relacionados):
    fuentes = ""
    if a.get("fuentes"):
        items = "".join(f'<li><a href="{html.escape(f["url"])}" rel="nofollow noopener" target="_blank">{html.escape(f["titulo"])}</a></li>'
                        for f in a["fuentes"])
        fuentes = f'<aside class="fuentes"><h2>Fuentes oficiales consultadas</h2><ul>{items}</ul></aside>'
    rel = ""
    if relacionados:
        rel = ('<section class="seccion"><div class="contenedor"><div class="seccion-titulo"><h2>Sigue aprendiendo</h2></div>'
               f'<div class="rejilla">{"".join(tarjeta_articulo(r) for r in relacionados)}</div></div></section>')
    ld = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": a["titulo"], "description": a["resumen"],
        "datePublished": a["fecha"], "dateModified": a["revisado"],
        "inLanguage": "es-ES",
        "mainEntityOfPage": f"{BASE}/articulos/{a['slug']}/",
        "publisher": {"@type": "Organization", "name": SITE["name"]},
    }
    cuerpo = f"""<div class="contenedor"><nav class="migas" aria-label="Migas"><a href="/">Inicio</a> › <a href="/articulos/">Guías</a> › {CATEGORIAS[a['categoria']]}</nav></div>
<article class="articulo">
  <span class="categoria cat-{a['categoria']}">{CATEGORIAS[a['categoria']]}</span>
  <h1>{html.escape(a['titulo'])}</h1>
  <p class="resumen">{html.escape(a['resumen'])}</p>
  <div class="sello"><span class="ok">✓ Contrastado con fuentes oficiales</span><span>Publicado el {fecha_larga(a['fecha'])}</span><span>Revisado el {fecha_larga(a['revisado'])}</span></div>
  {a['cuerpo_html']}
  {fuentes}
</article>
{rel}"""
    extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    escribir(f"/articulos/{a['slug']}/", pagina(a["titulo"], a["resumen"], f"/articulos/{a['slug']}/", cuerpo,
                                              "articulos", extra, "article"))


def generar_test(t):
    preguntas = []
    for p in t["preguntas"]:
        assert 0 <= p["correcta"] < len(p["opciones"]), p["enunciado"]
        item = {
            "enunciado": p["enunciado"],
            "opciones": p["opciones"],
            "correcta": p["correcta"],
            "explicacion_html": markdown.markdown(p["explicacion"])[3:-4] if p["explicacion"].count("\n\n") == 0
            else markdown.markdown(p["explicacion"]),
        }
        if p.get("senal"):
            item["dibujo"] = signs.CATALOGO[p["senal"]]()
        preguntas.append(item)
    datos = json.dumps({"preguntas": preguntas}, ensure_ascii=False).replace("</", "<\\/")
    # Preguntas también en HTML plano (noscript) para buscadores y accesibilidad
    plano = "".join(
        f"<li><b>{html.escape(p['enunciado'])}</b> Respuesta: {html.escape(p['opciones'][p['correcta']])}.</li>"
        for p in t["preguntas"])
    cuerpo = f"""<div class="contenedor"><nav class="migas" aria-label="Migas"><a href="/">Inicio</a> › <a href="/tests/">Tests</a></nav></div>
<section class="test">
  <h1>{html.escape(t['titulo'])}</h1>
  <p class="resumen">{html.escape(t['descripcion'])} Pulsa una respuesta: verás al momento si es correcta y por qué.</p>
  <div class="marcador"><span id="progreso">0 / 0</span><div class="barra"><i></i></div><span class="fallos-cont" id="fallos">0 fallos</span></div>
  <div id="preguntas"></div>
  <div id="resultado" class="resultado" aria-live="polite"></div>
  <noscript><ol>{plano}</ol></noscript>
</section>
<script type="application/json" id="datos-test">{datos}</script>"""
    escribir(f"/tests/{t['slug']}/", pagina(t["titulo"], t["descripcion"], f"/tests/{t['slug']}/", cuerpo, "tests"))


FAMILIAS = [
    ("Peligro", "otros_peligros", "Triángulo con borde rojo. Avisan de un peligro que tienes delante para que reduzcas la velocidad y prestes atención.",
     [("otros_peligros", "Otros peligros", "Peligro distinto de los que tienen señal propia; suele llevar un panel que lo explica."),
      ("curva_derecha", "Curva peligrosa a la derecha", "Curva que puede exigir reducir la velocidad."),
      ("interseccion", "Intersección con prioridad a la derecha", "Cruce donde rige la regla general: pasa primero quien viene por tu derecha.")]),
    ("Prioridad", "ceda", "Ordenan quién pasa primero en un cruce. Tienen formas únicas para reconocerlas aunque estén sucias o tapadas por nieve.",
     [("ceda", "Ceda el paso", "Debes ceder el paso a los vehículos de la otra vía. No es obligatorio parar si no viene nadie."),
      ("stop", "STOP", "Detención obligatoria siempre, venga o no venga alguien, y después ceder el paso."),
      ("calzada_prioridad", "Calzada con prioridad", "Circulas por una vía con prioridad en los próximos cruces.")]),
    ("Prohibición", "entrada_prohibida", "Círculo con borde rojo. Te prohíben algo desde la señal hasta el siguiente cruce o hasta una señal de fin.",
     [("entrada_prohibida", "Entrada prohibida", "Prohibido entrar a cualquier vehículo."),
      ("velocidad_50", "Velocidad máxima", "No puedes superar la velocidad indicada, en km/h."),
      ("estacionamiento_prohibido", "Estacionamiento prohibido", "Una barra: puedes parar, pero no estacionar."),
      ("parada_prohibida", "Parada y estacionamiento prohibidos", "Dos barras en aspa: ni parar ni estacionar."),
      ("fin_prohibiciones", "Fin de prohibiciones", "Terminan las prohibiciones que te habían señalizado antes.")]),
    ("Obligación", "sentido_obligatorio", "Círculo azul. Te obligan a hacer algo concreto.",
     [("sentido_obligatorio", "Sentido obligatorio", "Debes seguir la dirección que marca la flecha.")]),
    ("Indicación", "estacionamiento", "Cuadradas o rectangulares, normalmente azules. Te informan, no te prohíben ni te obligan.",
     [("estacionamiento", "Estacionamiento", "Lugar donde está permitido estacionar.")]),
    ("Circunstanciales", "obras", "Colocadas de forma temporal. Con el nuevo catálogo, las de obras llevan fondo amarillo.",
     [("obras", "Peligro por obras", "Versión de fondo amarillo: la situación es temporal y prevalece sobre la señalización fija.")]),
]


def generar_senales():
    bloques = []
    for nombre, icono, desc, lista in FAMILIAS:
        items = "".join(f'<div class="senal">{signs.CATALOGO[k]()}<b>{html.escape(t)}</b><span>{html.escape(d)}</span></div>'
                        for k, t, d in lista)
        bloques.append(f"""<section class="familia">
  <div class="familia-cabecera">{signs.CATALOGO[icono]()}<div><h2>{nombre}</h2></div></div>
  <p>{html.escape(desc)}</p>
  <div class="senales">{items}</div>
</section>""")
    cuerpo = f"""<div class="contenedor"><nav class="migas"><a href="/">Inicio</a> › Señales</nav></div>
<div class="articulo" style="max-width:var(--ancho)">
  <h1>Guía de señales de tráfico</h1>
  <p class="resumen">La forma y el color de una señal ya te dicen qué tipo de mensaje da, antes de leer el dibujo. Aprende la familia y tendrás medio examen de señales ganado.</p>
  <div class="aviso"><b>El truco de la forma</b> Triángulo = peligro. Círculo rojo = prohibición. Círculo azul = obligación. Cuadrado o rectángulo = indicación. El octógono (STOP) y el triángulo invertido (ceda el paso) son únicos a propósito.</div>
  {''.join(bloques)}
  <p>Todas las señales de esta página están dibujadas por Carnet Claro a partir de la señalización oficial española. Los códigos y el catálogo completo están en el anexo I del Reglamento General de Circulación, actualizado por el Real Decreto 465/2025.</p>
</div>"""
    escribir("/senales/", pagina("Guía de señales de tráfico explicadas", "Todas las familias de señales de tráfico en España explicadas de forma clara: peligro, prioridad, prohibición, obligación, indicación y las nuevas circunstanciales de fondo amarillo.", "/senales/", cuerpo, "senales"))


def generar_portada(arts, tests):
    ultimos = "".join(tarjeta_articulo(a) for a in arts[:6])
    tts = "".join(tarjeta_test(t) for t in tests[:3])
    mini = "".join(signs.CATALOGO[k]() for k in ["stop", "ceda", "velocidad_50", "otros_peligros", "sentido_obligatorio", "calzada_prioridad"])
    cuerpo = f"""<section class="portada">
  <div class="contenedor">
    <div>
      <span class="etiqueta-verif">✓ Contrastado con la DGT y el BOE</span>
      <h1>Apruébalo entendiendo, <em>no memorizando</em>.</h1>
      <p class="entrada">Tests del permiso B donde cada respuesta viene explicada, guías claras y la normativa al día. Gratis y sin registrarte.</p>
      <div class="botones"><a class="boton boton-amarillo" href="/tests/">Hacer un test</a><a class="boton boton-linea" href="/senales/">Ver las señales</a></div>
    </div>
    <div class="portada-senales" aria-hidden="true">{mini}</div>
  </div>
</section>
<section class="seccion">
  <div class="contenedor tres-claves">
    <div class="clave"><b>Cada respuesta explicada</b><p>No solo te decimos cuál es la correcta: te contamos el porqué, para que no vuelvas a fallarla.</p></div>
    <div class="clave"><b>Normativa verificada</b><p>Cada guía indica sus fuentes oficiales y la fecha de su última revisión.</p></div>
    <div class="clave"><b>Al día de los cambios</b><p>Alcohol, señales nuevas, puntos: separamos lo que está en vigor de lo que solo es una propuesta.</p></div>
  </div>
</section>
<hr class="divisor">
<section class="seccion">
  <div class="contenedor">
    <div class="seccion-titulo"><h2>Tests para practicar</h2><a href="/tests/">Ver todos</a></div>
    <div class="rejilla">{tts}</div>
  </div>
</section>
<hr class="divisor">
<section class="seccion">
  <div class="contenedor">
    <div class="seccion-titulo"><h2>Últimas guías</h2><a href="/articulos/">Ver todas</a></div>
    <div class="rejilla">{ultimos}</div>
  </div>
</section>"""
    ld = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"], "url": BASE + "/", "inLanguage": "es-ES"}
    escribir("/", pagina(SITE["name"], "Tests del carnet de conducir con cada respuesta explicada, guía de señales y normativa de tráfico al día, contrastada con la DGT y el BOE.",
                         "/", cuerpo, "", f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'))


def generar_listados(arts, tests):
    grupos = ""
    for clave, nombre in CATEGORIAS.items():
        lista = [a for a in arts if a["categoria"] == clave]
        if lista:
            grupos += f'<h2>{nombre}</h2><div class="rejilla">{"".join(tarjeta_articulo(a) for a in lista)}</div>'
    cuerpo = f"""<div class="contenedor"><nav class="migas"><a href="/">Inicio</a> › Guías</nav>
<h1>Guías del carnet de conducir</h1>
<p class="resumen" style="max-width:60ch;color:var(--tinta-suave)">Normas, examen, señales y novedades, explicado con claridad. Cada guía indica sus fuentes oficiales y la fecha de revisión.</p>
{grupos}<div style="height:48px"></div></div>"""
    escribir("/articulos/", pagina("Guías del carnet de conducir", "Guías claras sobre normas de tráfico, el examen teórico, señales y novedades de la DGT.", "/articulos/", cuerpo, "articulos"))

    cuerpo = f"""<div class="contenedor"><nav class="migas"><a href="/">Inicio</a> › Tests</nav>
<h1>Tests del permiso B con explicación</h1>
<p class="resumen" style="max-width:60ch;color:var(--tinta-suave)">Practica por temas. Al responder verás al instante si has acertado y la explicación de la norma. Se aprueba con el mismo criterio que el examen real: como máximo un 10&nbsp;% de fallos.</p>
<div class="rejilla">{"".join(tarjeta_test(t) for t in tests)}</div><div style="height:48px"></div></div>"""
    escribir("/tests/", pagina("Tests del permiso B con explicación", "Tests gratuitos del carnet de conducir B por temas, con la explicación de cada respuesta.", "/tests/", cuerpo, "tests"))


def generar_paginas():
    for f in sorted((RAIZ / "content/paginas").glob("*.md")):
        meta, cuerpo = leer_md(f)
        texto = cuerpo.replace("{{titular}}", SITE.get("owner_name") or "[Nombre del titular]")
        texto = texto.replace("{{email}}", SITE.get("contact_email") or "[correo de contacto]")
        texto = texto.replace("{{dominio}}", BASE.replace("https://", ""))
        cuerpo_html = f'<div class="contenedor"><nav class="migas"><a href="/">Inicio</a> › {html.escape(meta["titulo"])}</nav></div><div class="paginas-legales"><h1>{html.escape(meta["titulo"])}</h1>{md_a_html(texto)}</div>'
        escribir(f"/{meta['slug']}/", pagina(meta["titulo"], meta["resumen"], f"/{meta['slug']}/", cuerpo_html, meta.get("activo", "")))


def generar_extras(arts, tests):
    hoy = dt.date.today().isoformat()
    urls = [("/", hoy), ("/tests/", hoy), ("/senales/", hoy), ("/articulos/", hoy)]
    urls += [(f"/articulos/{a['slug']}/", a["revisado"]) for a in arts]
    urls += [(f"/tests/{t['slug']}/", t["fecha"]) for t in tests]
    urls += [(f"/{m}/", hoy) for m in ["examen-teorico", "sobre-nosotros", "contacto", "aviso-legal", "privacidad", "cookies"]]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls)
    xml += "</urlset>\n"
    (DIST / "sitemap.xml").write_text(xml, encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    if SITE.get("adsense_client"):
        pub = SITE["adsense_client"].replace("ca-", "")
        (DIST / "ads.txt").write_text(f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
    (DIST / "favicon.svg").write_text(signs.logo(), encoding="utf-8")
    cuerpo = '<div class="contenedor" style="padding:80px 16px;text-align:center">' + signs.otros_peligros() .replace("<svg ", '<svg style="width:120px" ') + '<h1>Esta página no existe</h1><p>Puede que la dirección haya cambiado. <a href="/">Vuelve al inicio</a> o prueba con <a href="/tests/">un test</a>.</p></div>'
    (DIST / "404.html").write_text(pagina("Página no encontrada", "Página no encontrada.", "/404.html", cuerpo), encoding="utf-8")


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    for f in (RAIZ / "static").iterdir():
        shutil.copy(f, DIST / f.name)
    arts = cargar_articulos()
    tests = cargar_tests()
    for a in arts:
        rel = [r for r in arts if r["slug"] != a["slug"] and r["categoria"] == a["categoria"]][:2]
        rel += [r for r in arts if r["slug"] != a["slug"] and r not in rel][: 3 - len(rel)]
        generar_articulo(a, rel)
    for t in tests:
        generar_test(t)
    generar_senales()
    generar_portada(arts, tests)
    generar_listados(arts, tests)
    generar_paginas()
    generar_extras(arts, tests)
    print(f"OK: {len(arts)} artículos, {len(tests)} tests -> {DIST}")


if __name__ == "__main__":
    main()
