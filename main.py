import asyncio
import flet as ft


def main(page: ft.Page):
    # Configuración general
    page.title = "BRAIN RUSH"
    page.bgcolor = "#101426"
    page.padding = 25
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # Preguntas del juego
    preguntas = [
        {
            "pregunta": "What is the capital of Canada?",
            "opciones": ["A) London", "B) Paris", "C) Madrid", "D) Ottawa"],
            "correcta": "D) Ottawa"
        },
        {
            "pregunta": "How many days are in a week?",
            "opciones": ["A) Five", "B) Four", "C) Seven", "D) Eight"],
            "correcta": "C) Seven"
        },
        {
            "pregunta": "Which planet is known as the Red Planet?",
            "opciones": ["A) Mars", "B) Venus", "C) Jupiter", "D) Earth"],
            "correcta": "A) Mars"
        },
        {
            "pregunta": "What is 21 + 5?",
            "opciones": ["A) 8", "B) 9", "C) 26", "D) 12"],
            "correcta": "C) 26"
        },
        {
            "pregunta": "Which animal is known as the king of the jungle?",
            "opciones": ["A) Tiger", "B) Lion", "C) Elephant", "D) Bear"],
            "correcta": "B) Lion"
        }
    ]

    numero = 0
    puntos = 0
    segundos = 10
    reloj_activo = False
    turno_id = 0

    # Título
    titulo = ft.Text(
        "🧠 BRAIN RUSH",
        size=38,
        weight=ft.FontWeight.BOLD,
        color="#22D3EE"
    )

    descripcion = ft.Text(
        "THINK FAST. ANSWER SMART!",
        size=14,
        color="#C4B5FD"
    )

    # Puntuación
    marcador = ft.Text(
        "SCORE: 0 / 50",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#FACC15"
    )

    barra_puntos = ft.ProgressBar(
        value=0,
        color="#22D3EE",
        bgcolor="#344054",
        height=10
    )

    # Progreso de preguntas
    progreso = ft.Text(
        "QUESTION 0 OF 5",
        size=14,
        color="#A5B4FC"
    )

    # Temporizador
    reloj = ft.Text(
        "⏳ 10 SECONDS",
        size=22,
        weight=ft.FontWeight.BOLD,
        color="#4ADE80"
    )

    barra_tiempo = ft.ProgressBar(
        value=1,
        color="#4ADE80",
        bgcolor="#344054",
        height=10
    )

    # Pregunta y mensaje
    pregunta = ft.Text(
        "Are you ready for the challenge?",
        size=21,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER
    )

    mensaje = ft.Text(
        "",
        size=16,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER
    )

    # Opciones de respuesta
    opciones = ft.Column(
        spacing=12,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Botones principales
    boton_inicio = ft.Button(
        content="START GAME 🚀",
        width=240,
        height=50
    )

    siguiente = ft.Button(
        content="NEXT QUESTION ➜",
        width=240,
        height=50,
        disabled=True,
        visible=False
    )

    play_again = ft.Button(
        content="PLAY AGAIN 🔄",
        width=240,
        height=50,
        visible=False
    )

    # Detener el reloj
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
            reloj.value = f"⏳ {segundos} SECONDS"
            barra_tiempo.value = segundos / 10

            if segundos <= 3:
                reloj.color = ft.Colors.RED
                barra_tiempo.color = ft.Colors.RED

            page.update()

            if segundos == 0:
                terminar_pregunta(False, tiempo_agotado=True)
                break

    # Iniciar el reloj
    def iniciar_reloj():
        nonlocal segundos, reloj_activo

        segundos = 10
        reloj_activo = True

        reloj.value = "⏳ 10 SECONDS"
        reloj.color = "#4ADE80"

        barra_tiempo.value = 1
        barra_tiempo.color = "#4ADE80"

        page.run_task(cuenta_regresiva)

    # Mostrar pregunta
    def mostrar_pregunta():
        pregunta.value = preguntas[numero]["pregunta"]
        progreso.value = f"QUESTION {numero + 1} OF {len(preguntas)}"
        mensaje.value = ""

        opciones.controls.clear()

        for opcion in preguntas[numero]["opciones"]:
            opciones.controls.append(
                ft.Button(
                    content=opcion,
                    width=300,
                    height=52,
                    style=ft.ButtonStyle(
                        bgcolor="#293653",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=14)
                    ),
                    on_click=verificar_respuesta
                )
            )

        iniciar_reloj()
        page.update()

    # Finalizar pregunta
    def terminar_pregunta(es_correcta, tiempo_agotado=False):
        nonlocal numero, puntos

        detener_reloj()

        if tiempo_agotado:
            mensaje.value = (
                f"TIME'S UP! ⏰ Correct answer: "
                f"{preguntas[numero]['correcta']}"
            )
            mensaje.color = ft.Colors.RED

        elif es_correcta:
            puntos += 10
            mensaje.value = "CORRECT ANSWER! 🎉 +10 POINTS"
            mensaje.color = ft.Colors.GREEN

        else:
            correcta = preguntas[numero]["correcta"]
            mensaje.value = f"WRONG ANSWER! Correct: {correcta}"
            mensaje.color = ft.Colors.RED

        marcador.value = f"SCORE: {puntos} / 50"
        barra_puntos.value = puntos / 50

        for control in opciones.controls:
            control.disabled = True

        numero += 1

        if numero < len(preguntas):
            siguiente.disabled = False
            siguiente.visible = True
        else:
            pregunta.value = "🏆 GAME COMPLETED!"
            progreso.value = "YOU FINISHED ALL QUESTIONS!"
            reloj.value = "TIME FINISHED"
            barra_tiempo.value = 0

            mensaje.value += f"\nFINAL SCORE: {puntos} / 50"

            siguiente.visible = False
            play_again.visible = True

        page.update()

    # Comprobar respuesta
    def verificar_respuesta(e):
        if not reloj_activo:
            return

        seleccion = e.control.content
        correcta = preguntas[numero]["correcta"]

        terminar_pregunta(seleccion == correcta)

    # Iniciar partida
    def iniciar_juego(e):
        nonlocal numero, puntos

        detener_reloj()

        numero = 0
        puntos = 0

        marcador.value = "SCORE: 0 / 50"
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

    # Volver a jugar
    def reiniciar_juego(e):
        iniciar_juego(e)

    boton_inicio.on_click = iniciar_juego
    siguiente.on_click = avanzar
    play_again.on_click = reiniciar_juego

    # Diseño principal
    contenido = ft.Column(
        controls=[
            titulo,
            descripcion,
            ft.Divider(color="#344054"),
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
        bgcolor="#1B2542",
        padding=35,
        border_radius=25,
        width=520,
        border=ft.Border.all(1, "#34466B")
    )

    # Agregar pantalla con desplazamiento
    page.add(
        ft.Row(
            controls=[pantalla],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    )


ft.run(main)



