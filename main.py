
import asyncio
import flet as ft


def main(page: ft.Page):
    # Configuración general
    page.title = "BRAIN RUSH"
    page.bgcolor = "#F0F4FF"
    page.padding = 25
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # Preguntas en inglés y español
    preguntas = [
        {
            "pregunta": {
                "en": "What is the capital of Canada?",
                "es": "¿Cuál es la capital de Canadá?"
            },
            "opciones": {
                "en": ["A) London", "B) Paris", "C) Madrid", "D) Ottawa"],
                "es": ["A) Londres", "B) París", "C) Madrid", "D) Ottawa"]
            },
            "correcta": 3
        },
        {
            "pregunta": {
                "en": "How many days are in a week?",
                "es": "¿Cuántos días tiene una semana?"
            },
            "opciones": {
                "en": ["A) Five", "B) Four", "C) Seven", "D) Eight"],
                "es": ["A) Cinco", "B) Cuatro", "C) Siete", "D) Ocho"]
            },
            "correcta": 2
        },
        {
            "pregunta": {
                "en": "Which planet is known as the Red Planet?",
                "es": "¿Qué planeta es conocido como el planeta rojo?"
            },
            "opciones": {
                "en": ["A) Mars", "B) Venus", "C) Jupiter", "D) Earth"],
                "es": ["A) Marte", "B) Venus", "C) Júpiter", "D) Tierra"]
            },
            "correcta": 0
        },
        {
            "pregunta": {
                "en": "What is 21 + 5?",
                "es": "¿Cuánto es 21 + 5?"
            },
            "opciones": {
                "en": ["A) 8", "B) 9", "C) 26", "D) 12"],
                "es": ["A) 8", "B) 9", "C) 26", "D) 12"]
            },
            "correcta": 2
        },
        {
            "pregunta": {
                "en": "Which animal is known as the king of the jungle?",
                "es": "¿Qué animal es conocido como el rey de la selva?"
            },
            "opciones": {
                "en": ["A) Tiger", "B) Lion", "C) Elephant", "D) Bear"],
                "es": ["A) Tigre", "B) León", "C) Elefante", "D) Oso"]
            },
            "correcta": 1
        }
    ]

    # Variables del juego
    numero = 0
    indice_actual = 0
    puntos = 0
    segundos = 10
    reloj_activo = False
    turno_id = 0
    idioma = "en"
    juego_iniciado = False
    juego_finalizado = False
    pregunta_respondida = False
    resultado = None

    # Textos de los dos idiomas
    textos = {
        "en": {
            "titulo": "🧠 BRAIN RUSH",
            "descripcion": "THINK FAST. ANSWER SMART!",
            "score": "SCORE",
            "question": "QUESTION",
            "of": "OF",
            "seconds": "SECONDS",
            "ready": "Are you ready for the challenge?",
            "start": "START GAME 🚀",
            "next": "NEXT QUESTION ➜",
            "again": "PLAY AGAIN 🔄",
            "correct": "CORRECT ANSWER! 🎉 +10 POINTS",
            "wrong": "WRONG ANSWER! Correct:",
            "timeout": "TIME'S UP! ⏰ Correct answer:",
            "completed": "🏆 GAME COMPLETED!",
            "finished": "YOU FINISHED ALL QUESTIONS!",
            "time_finished": "TIME FINISHED",
            "final_score": "FINAL SCORE",
            "spanish": "ESPAÑOL 🇪🇸",
            "english": "ENGLISH 🇬🇧"
        },
        "es": {
            "titulo": "🧠 BRAIN RUSH",
            "descripcion": "¡PIENSA RÁPIDO. RESPONDE INTELIGENTE!",
            "score": "PUNTOS",
            "question": "PREGUNTA",
            "of": "DE",
            "seconds": "SEGUNDOS",
            "ready": "¿Estás listo para el desafío?",
            "start": "INICIAR JUEGO 🚀",
            "next": "SIGUIENTE PREGUNTA ➜",
            "again": "JUGAR OTRA VEZ 🔄",
            "correct": "¡RESPUESTA CORRECTA! 🎉 +10 PUNTOS",
            "wrong": "¡RESPUESTA INCORRECTA! Correcta:",
            "timeout": "¡SE ACABÓ EL TIEMPO! ⏰ Respuesta:",
            "completed": "🏆 ¡JUEGO COMPLETADO!",
            "finished": "¡TERMINASTE TODAS LAS PREGUNTAS!",
            "time_finished": "TIEMPO TERMINADO",
            "final_score": "PUNTUACIÓN FINAL",
            "spanish": "ESPAÑOL 🇪🇸",
            "english": "ENGLISH 🇬🇧"
        }
    }

    # Título
    titulo = ft.Text(
        textos[idioma]["titulo"],
        size=38,
        weight=ft.FontWeight.BOLD,
        color="#2563EB"
    )

    descripcion = ft.Text(
        textos[idioma]["descripcion"],
        size=14,
        color="#64748B",
        text_align=ft.TextAlign.CENTER
    )

    # Botón para cambiar idioma
    boton_idioma = ft.Button(
        content="ESPAÑOL 🇪🇸",
        width=180,
        height=42,
        style=ft.ButtonStyle(
            bgcolor="#DBEAFE",
            color="#1D4ED8"
        )
    )

    # Puntuación
    marcador = ft.Text(
        "SCORE: 0 / 50",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#D69E00"
    )

    barra_puntos = ft.ProgressBar(
        value=0,
        color="#3B82F6",
        bgcolor="#DBEAFE",
        height=10
    )

    progreso = ft.Text(
        "QUESTION 0 OF 5",
        size=14,
        color="#64748B"
    )

    # Temporizador
    reloj = ft.Text(
        "⏳ 10 SECONDS",
        size=22,
        weight=ft.FontWeight.BOLD,
        color="#16A34A"
    )

    barra_tiempo = ft.ProgressBar(
        value=1,
        color="#22C55E",
        bgcolor="#DCFCE7",
        height=10
    )

    # Pregunta y mensaje
    pregunta = ft.Text(
        textos[idioma]["ready"],
        size=21,
        weight=ft.FontWeight.BOLD,
        color="#263B70",
        text_align=ft.TextAlign.CENTER
    )

    mensaje = ft.Text(
        "",
        size=16,
        color="#263B70",
        text_align=ft.TextAlign.CENTER
    )

    # Opciones en formato horizontal
    opciones = ft.Row(
        wrap=True,
        spacing=12,
        run_spacing=12,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Botones principales
    boton_inicio = ft.Button(
        content="START GAME 🚀",
        width=240,
        height=50,
        style=ft.ButtonStyle(
            bgcolor="#2563EB",
            color="#FFFFFF"
        )
    )

    siguiente = ft.Button(
        content="NEXT QUESTION ➜",
        width=240,
        height=50,
        disabled=True,
        visible=False,
        style=ft.ButtonStyle(
            bgcolor="#7C3AED",
            color="#FFFFFF"
        )
    )

    play_again = ft.Button(
        content="PLAY AGAIN 🔄",
        width=240,
        height=50,
        visible=False,
        style=ft.ButtonStyle(
            bgcolor="#16A34A",
            color="#FFFFFF"
        )
    )

    # Actualizar textos según el idioma
    def actualizar_idioma():
        t = textos[idioma]

        titulo.value = t["titulo"]
        descripcion.value = t["descripcion"]

        boton_idioma.content = (
            t["english"] if idioma == "es" else t["spanish"]
        )

        marcador.value = f"{t['score']}: {puntos} / 50"
        boton_inicio.content = t["start"]
        siguiente.content = t["next"]
        play_again.content = t["again"]

        if juego_finalizado:
            pregunta.value = t["completed"]
            progreso.value = t["finished"]
            reloj.value = t["time_finished"]

        elif juego_iniciado:
            pregunta.value = preguntas[indice_actual]["pregunta"][idioma]

            progreso.value = (
                f"{t['question']} {indice_actual + 1} "
                f"{t['of']} {len(preguntas)}"
            )

            if reloj_activo:
                reloj.value = f"⏳ {segundos} {t['seconds']}"

            # Actualizar opciones en formato horizontal
            opciones.controls.clear()

            for i, opcion in enumerate(
                preguntas[indice_actual]["opciones"][idioma]
            ):
                opciones.controls.append(
                    ft.Button(
                        content=opcion,
                        width=210,
                        height=65,
                        disabled=pregunta_respondida,
                        style=ft.ButtonStyle(
                            bgcolor="#E8EEFF",
                            color="#263B70",
                            shape=ft.RoundedRectangleBorder(radius=14)
                        ),
                        on_click=verificar_respuesta
                    )
                )

            # Actualizar mensaje de respuesta
            if resultado == "correct":
                mensaje.value = t["correct"]
                mensaje.color = "#16A34A"

            elif resultado == "wrong":
                correcta = preguntas[indice_actual]["opciones"][idioma][
                    preguntas[indice_actual]["correcta"]
                ]
                mensaje.value = f"{t['wrong']} {correcta}"
                mensaje.color = "#DC2626"

            elif resultado == "timeout":
                correcta = preguntas[indice_actual]["opciones"][idioma][
                    preguntas[indice_actual]["correcta"]
                ]
                mensaje.value = f"{t['timeout']} {correcta}"
                mensaje.color = "#DC2626"

            else:
                mensaje.value = ""

        else:
            pregunta.value = t["ready"]
            progreso.value = f"{t['question']} 0 {t['of']} 5"
            reloj.value = f"⏳ 10 {t['seconds']}"

        page.update()

    # Cambiar idioma
    def cambiar_idioma(e):
        nonlocal idioma

        if idioma == "en":
            idioma = "es"
        else:
            idioma = "en"

        actualizar_idioma()

    # Detener reloj
    def detener_reloj():
        nonlocal reloj_activo, turno_id

        reloj_activo = False
        turno_id += 1

    # Cuenta regresiva
    async def cuenta_regresiva():
        nonlocal segundos

        mi_turno = turno_id

        while reloj_activo and mi_turno == turno_id:
            await asyncio.sleep(1)

            if not reloj_activo or mi_turno != turno_id:
                break

            segundos -= 1
            reloj.value = f"⏳ {segundos} {textos[idioma]['seconds']}"
            barra_tiempo.value = segundos / 10

            if segundos <= 3:
                reloj.color = "#DC2626"
                barra_tiempo.color = "#EF4444"

            page.update()

            if segundos == 0:
                terminar_pregunta(False, tiempo_agotado=True)
                break

    # Iniciar reloj
    def iniciar_reloj():
        nonlocal segundos, reloj_activo

        segundos = 10
        reloj_activo = True

        reloj.value = f"⏳ 10 {textos[idioma]['seconds']}"
        reloj.color = "#16A34A"

        barra_tiempo.value = 1
        barra_tiempo.color = "#22C55E"

        page.run_task(cuenta_regresiva)

    # Mostrar pregunta
    def mostrar_pregunta():
        nonlocal indice_actual, pregunta_respondida, resultado

        indice_actual = numero
        pregunta_respondida = False
        resultado = None

        actualizar_idioma()
        iniciar_reloj()

        page.update()

    # Finalizar pregunta
    def terminar_pregunta(es_correcta, tiempo_agotado=False):
        nonlocal numero, puntos
        nonlocal pregunta_respondida, resultado, juego_finalizado

        detener_reloj()
        pregunta_respondida = True

        if tiempo_agotado:
            resultado = "timeout"

        elif es_correcta:
            puntos += 10
            resultado = "correct"

        else:
            resultado = "wrong"

        barra_puntos.value = puntos / 50

        if numero < len(preguntas) - 1:
            siguiente.disabled = False
            siguiente.visible = True

        else:
            juego_finalizado = True
            siguiente.visible = False
            play_again.visible = True

        numero += 1

        actualizar_idioma()
        page.update()

    # Comprobar respuesta
    def verificar_respuesta(e):
        if not reloj_activo or pregunta_respondida:
            return

        seleccion = e.control.content

        correcta = preguntas[indice_actual]["opciones"][idioma][
            preguntas[indice_actual]["correcta"]
        ]

        terminar_pregunta(seleccion == correcta)

    # Iniciar partida
    def iniciar_juego(e):
        nonlocal numero, puntos, juego_iniciado, juego_finalizado

        detener_reloj()

        numero = 0
        puntos = 0
        juego_iniciado = True
        juego_finalizado = False

        marcador.value = f"{textos[idioma]['score']}: 0 / 50"
        barra_puntos.value = 0

        boton_inicio.visible = False
        siguiente.visible = False
        play_again.visible = False

        mostrar_pregunta()

    # Siguiente pregunta
    def avanzar(e):
        siguiente.disabled = True
        siguiente.visible = False

        mostrar_pregunta()

    # Reiniciar juego
    def reiniciar_juego(e):
        iniciar_juego(e)

    # Conectar botones
    boton_idioma.on_click = cambiar_idioma
    boton_inicio.on_click = iniciar_juego
    siguiente.on_click = avanzar
    play_again.on_click = reiniciar_juego

    # Diseño principal
    contenido = ft.Column(
        controls=[
            boton_idioma,
            titulo,
            descripcion,
            ft.Divider(color="#DCE5F5"),
            marcador,
            barra_puntos,
            progreso,
            ft.Container(height=5),
            reloj,
            barra_tiempo,
            ft.Container(height=10),
            pregunta,
            opciones,
            mensaje,
            ft.Container(height=5),
            boton_inicio,
            siguiente,
            play_again
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=17
    )

    # Tarjeta principal
    pantalla = ft.Container(
        content=contenido,
        bgcolor="#FFFFFF",
        padding=35,
        border_radius=25,
        width=520,
        border=ft.Border.all(1, "#DCE5F5")
    )

    # Agregar pantalla
    page.add(
        ft.Row(
            controls=[pantalla],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    )


ft.run(main)
