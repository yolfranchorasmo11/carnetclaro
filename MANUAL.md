# Carnet Claro — Manual de funcionamiento diario

Este archivo es la memoria del proyecto. Cada ejecución diaria empieza leyéndolo.

## Objetivo
Web informativa sobre el carnet de conducir en España (permiso B), monetizada con Google AdSense.
Propietario: Eduardo. Presupuesto: **cero** (nada de herramientas de pago, ni imágenes de pago).

## Reglas de calidad (no negociables)
1. **Exactitud:** todo dato normativo se verifica en fuentes oficiales (BOE, dgt.es, revista.dgt.es, sede.dgt.gob.es) o, como apoyo, RACE/RACC. Si un dato no se puede verificar, no se publica.
2. **Vigente vs. propuesto:** separar siempre lo que está en vigor de lo que es una propuesta o noticia. Nada es "nuevo" hasta que está publicado en el BOE con fecha de entrada en vigor.
3. **Redacción propia:** nunca copiar frases de otras webs. Explicar con palabras propias, con ejemplos, trucos y errores típicos.
4. **Un artículo al día, no más.** Google penaliza el contenido masivo. Calidad > cantidad.
5. **Longitud:** 600–1.200 palabras, útiles de verdad. Nada de relleno.
6. **Imágenes:** solo señales/esquemas dibujados en SVG (signs.py). Nunca imágenes de bancos ni generadas con servicios de pago.
7. **Fecha de revisión:** cada artículo lleva `fecha` y `revisado`. Si se corrige uno antiguo, actualizar `revisado`.
8. **Sin datos personales** del propietario salvo los que él indique en site.json.

## Cómo publicar un artículo
1. Elegir el siguiente tema pendiente de la lista (o una novedad de tráfico verificada de esta semana, que tiene prioridad).
2. Investigar con búsquedas web y fuentes oficiales.
3. Crear `content/articulos/<slug>.md` con la cabecera YAML (ver artículos existentes como modelo): titulo, slug, resumen (≤160 caracteres), categoria (examen | normas | senales | actualidad), fecha, revisado, fuentes.
4. Usar bloques `<div class="truco" markdown="1">`, `aviso`, `error-tipico` y señales con `{{senal:nombre|pie}}` cuando aporten.
5. Enlazar a 1–2 guías o tests existentes relacionados.
6. Cada 3 artículos, añadir un test nuevo de 10 preguntas en `content/tests/` (orden siguiente) con preguntas basadas SOLO en contenido ya verificado.
7. Ejecutar `pip install markdown pyyaml && python3 build.py` y comprobar que no hay errores.
8. Anotar el artículo en el REGISTRO (abajo), hacer commit y push.

## Temas pendientes (en orden de prioridad)
- [ ] Glorietas: quién tiene preferencia y cómo salir correctamente
- [ ] Prioridad de paso en intersecciones sin señalizar (la regla de la derecha)
- [ ] Documentación obligatoria en el coche en 2026
- [ ] Distancia de seguridad: cómo calcularla y la regla de los segundos
- [ ] Adelantamientos: cuándo está prohibido adelantar
- [ ] Marcas viales: línea continua, discontinua, cebreados
- [ ] Luces: cuándo usar cruce, carretera, antiniebla y emergencia
- [ ] Qué es un conductor novel: obligaciones y la señal L
- [ ] Etiquetas ambientales de la DGT y Zonas de Bajas Emisiones
- [ ] Sistemas de retención infantil: normas vigentes
- [ ] Parar y estacionar: diferencias y dónde está prohibido
- [ ] Examen práctico: faltas eliminatorias, deficientes y leves
- [ ] Qué hacer en caso de accidente (PAS: proteger, avisar, socorrer)
- [ ] Carnet por puntos: cómo recuperar puntos
- [ ] Autopistas y autovías: incorporación, carril izquierdo, salidas
- [ ] Semáforos: significado de cada luz, incluidas las intermitentes
- [ ] Peatones y pasos de peatones: obligaciones del conductor
- [ ] Ciclistas y VMP (patinetes): cómo convivir y adelantar
- [ ] Neumáticos: profundidad mínima de dibujo y presión
- [ ] ITV: frecuencias y qué pasa si caduca
- [ ] Seguro obligatorio: qué cubre y multas por no tenerlo
- [ ] Túneles: normas específicas
- [ ] Pasos a nivel
- [ ] Conducción en lluvia, niebla y nieve (cadenas)
- [ ] Carga del vehículo y remolques ligeros con permiso B
- [ ] Permisos que se obtienen con el B (moto 125 cc con 3 años)
- [ ] Cansancio y somnolencia al volante
- [ ] Drogas y medicamentos al volante
- [ ] Cómo reservar cita para el examen teórico
- [ ] Trucos para el día del examen teórico

## Pendiente del propietario (Eduardo)
- [x] Correo de contacto: carnetclaro@outlook.com (ya en site.json).
- [ ] Nombre completo del titular para `site.json` (aviso legal, privacidad).
- [ ] Dominio propio (necesario para solicitar AdSense).
- [ ] Cuenta de AdSense → cuando esté, poner `adsense_client` en `site.json`.
- [ ] Al activar AdSense: activar el mensaje de consentimiento (CMP) gratuito de Google en "Privacidad y mensajes".

## REGISTRO de publicaciones
| Fecha | Tipo | Slug |
|---|---|---|
| 2026-09-27 | artículo | tasa-alcohol-2026 |
| 2026-09-27 | artículo | limites-velocidad-espana |
| 2026-09-27 | artículo | baliza-v16-conectada |
| 2026-09-27 | artículo | nuevo-catalogo-senales-2025 |
| 2026-09-27 | artículo | puntos-movil-cinturon |
| 2026-09-27 | artículo | ceda-el-paso-o-stop |
| 2026-09-27 | test | velocidad-y-alcohol |
| 2026-09-27 | test | senales-y-prioridad |
| 2026-09-27 | test | novedades-2026 |
| 2026-09-27 | página | examen-teorico |
| 2026-09-27 | artículo (novedad RD 518/2026) | cambios-reglamento-circulacion-octubre-2026 |
