import flet as ft


def main(page: ft.Page):
    # Configuración de la ventana
    page.title = "BRAIN RUSH"
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.padding = 25

    # Preguntas del juego
    preguntas = [
        {
            "pregunta": "What is the capital of France?",
            "opciones": ["A) London", "B) Paris", "C) Madrid", "D) Rome"],
            "correcta": "B) Paris"
        },
        {
            "pregunta": "How many days are in a week?",
            "opciones": ["A) Five", "B) Six", "C) Seven", "D) Eight"],
            "correcta": "C) Seven"
        },
        {
            "pregunta": "Which planet is known as the Red Planet?",
            "opciones": ["A) Mars", "B) Venus", "C) Jupiter", "D) Earth"],
            "correcta": "A) Mars"
        },
        {
            "pregunta": "What is 5 + 5?",
            "opciones": ["A) 8", "B) 9", "C) 10", "D) 12"],
            "correcta": "C) 10"
        },
        {
            "pregunta": "Which animal is known as the king of the jungle?",
            "opciones": ["A) Tiger", "B) Lion", "C) Elephant", "D) Bear"],
            "correcta": "B) Lion"
        }
    ]

    numero = 0
    puntos = 0

    # Título
    titulo = ft.Text(
        "BRAIN RUSH",
        size=35,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.CYAN
    )

    descripcion = ft.Text(
        "Test your knowledge and challenge your mind!",
        color=ft.Colors.WHITE
    )

    pregunta = ft.Text(
        "Are you ready for the challenge?",
        size=20,
        color=ft.Colors.WHITE
    )

    marcador = ft.Text(
        "Points: 0",
        size=18,
        color=ft.Colors.YELLOW
    )

    mensaje = ft.Text(
        "",
        size=16,
        color=ft.Colors.WHITE
    )

    opciones = ft.Column(
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Botón para iniciar
    boton = ft.Button(
        "START GAME"
    )

    # Botón para avanzar
    siguiente = ft.Button(
        "NEXT QUESTION",
        disabled=True
    )

    # Mostrar pregunta y opciones
    def mostrar_pregunta():
        pregunta.value = preguntas[numero]["pregunta"]
        marcador.value = f"Points: {puntos}"
        mensaje.value = ""

        opciones.controls.clear()

        for opcion in preguntas[numero]["opciones"]:
            opciones.controls.append(
                ft.Button(
                    content=opcion,
                    width=300,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_GREY_700,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=12)
                    ),
                    on_click=verificar_respuesta
                )
            )

        page.update()

    # Comprobar respuesta seleccionada
    def verificar_respuesta(e):
        nonlocal numero, puntos

        seleccion = e.control.content

        if seleccion == preguntas[numero]["correcta"]:
            puntos += 10
            mensaje.value = "Correct answer! Great job! 🎉"
            mensaje.color = ft.Colors.GREEN
        else:
            mensaje.value = "Wrong answer! ❌"
            mensaje.color = ft.Colors.RED

        # Desactivar los botones después de responder
        for control in opciones.controls:
            control.disabled = True

        numero += 1

        if numero < len(preguntas):
            siguiente.disabled = False
        else:
            pregunta.value = "Game completed! 🏆"
            marcador.value = f"Final points: {puntos}"
            siguiente.text = "PLAY AGAIN"
            siguiente.disabled = False

        page.update()

    # Iniciar o reiniciar el juego
    def iniciar_juego(e):
        nonlocal numero, puntos

        numero = 0
        puntos = 0

        boton.visible = False
        siguiente.text = "NEXT QUESTION"
        siguiente.disabled = True

        mostrar_pregunta()

    # Pasar a la siguiente pregunta
    def avanzar(e):
        nonlocal numero, puntos

        if numero >= len(preguntas):
            numero = 0
            puntos = 0
            boton.visible = True
            siguiente.text = "NEXT QUESTION"
            siguiente.disabled = True

            pregunta.value = "Are you ready for the challenge?"
            marcador.value = "Points: 0"
            mensaje.value = ""
            opciones.controls.clear()

        else:
            siguiente.disabled = True
            mostrar_pregunta()

        page.update()

    boton.on_click = iniciar_juego
    siguiente.on_click = avanzar

    # Organizar los elementos
    contenido = ft.Column(
        controls=[
            titulo,
            descripcion,
            boton,
            marcador,
            pregunta,
            opciones,
            mensaje,
            siguiente
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    # Contenedor principal
    pantalla = ft.Container(
        content=contenido,
        bgcolor=ft.Colors.INDIGO_900,
        padding=40,
        border_radius=20,
        width=500
    )

    page.add(
        ft.Row(
            controls=[pantalla],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


ft.run(main)
