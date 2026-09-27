// Carnet Claro — motor de tests. Sin cookies ni almacenamiento: todo en memoria.
(function () {
  var datos = document.getElementById("datos-test");
  if (!datos) return;
  var test = JSON.parse(datos.textContent);
  var cont = document.getElementById("preguntas");
  var barra = document.querySelector(".barra i");
  var txtProg = document.getElementById("progreso");
  var txtFallos = document.getElementById("fallos");
  var res = document.getElementById("resultado");
  var total = test.preguntas.length;
  var maxFallos = Math.floor(total * 0.1); // mismo criterio que el examen real: 3 de 30
  var respondidas = 0, fallos = 0;
  var letras = ["A", "B", "C"];

  function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }

  test.preguntas.forEach(function (p, i) {
    var art = document.createElement("article");
    art.className = "pregunta";
    var html = '<h3><span class="num">' + (i + 1) + "</span>" + esc(p.enunciado) + "</h3>";
    if (p.dibujo) html += '<div class="dibujo">' + p.dibujo + "</div>";
    p.opciones.forEach(function (o, j) {
      html += '<button class="opcion" type="button" data-j="' + j + '"><span class="letra">' + letras[j] + "</span><span>" + esc(o) + "</span></button>";
    });
    html += '<div class="explicacion" role="status"><b></b> ' + p.explicacion_html + "</div>";
    art.innerHTML = html;
    cont.appendChild(art);

    var botones = art.querySelectorAll(".opcion");
    botones.forEach(function (b) {
      b.addEventListener("click", function () {
        var j = +b.getAttribute("data-j");
        botones.forEach(function (x) { x.disabled = true; });
        botones[p.correcta].classList.add("correcta");
        var exp = art.querySelector(".explicacion");
        if (j === p.correcta) {
          exp.querySelector("b").textContent = "¡Correcto!";
        } else {
          b.classList.add("incorrecta");
          fallos++;
          exp.querySelector("b").textContent = "Respuesta correcta: " + letras[p.correcta] + ".";
        }
        exp.classList.add("visible");
        respondidas++;
        actualizar();
      });
    });
  });

  function actualizar() {
    barra.style.width = (respondidas / total * 100) + "%";
    txtProg.textContent = respondidas + " / " + total;
    txtFallos.textContent = fallos + (fallos === 1 ? " fallo" : " fallos");
    if (respondidas === total) {
      var ok = fallos <= maxFallos;
      res.className = "resultado visible " + (ok ? "aprobado" : "suspenso");
      res.innerHTML = "<h2>" + (ok ? "Aprobado" : "Suspenso") + "</h2><p>Has tenido <b>" + fallos +
        "</b> " + (fallos === 1 ? "fallo" : "fallos") + " de " + total + " preguntas. En el examen real se permite un máximo de 3 fallos en 30 preguntas (el 10&nbsp;%), así que aquí el límite es " +
        maxFallos + ".</p><p><a class=\"boton boton-amarillo\" href=\"\">Repetir el test</a> <a class=\"boton\" href=\"/tests/\">Más tests</a></p>";
      res.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }
  actualizar();
})();

// Cambio de tema claro/oscuro (sin guardar nada en el navegador)
(function () {
  var b = document.querySelector(".tema-btn");
  if (!b) return;
  b.addEventListener("click", function () {
    var r = document.documentElement;
    var oscuro = r.getAttribute("data-theme") === "dark" ||
      (!r.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
    r.setAttribute("data-theme", oscuro ? "light" : "dark");
  });
})();
