import flet as ft

def main(page: ft.Page):
     # Configuración de la ventana
    page.title = "BRAIN RUSH"
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.padding = 25

# Texto que cambiará cuando presionemos el botón
    mensaje = ft.Text(
        "Are you ready for the challenge?",
        size=16,
        color=ft.Colors.WHITE
    )
    # Función que se ejecuta al presionar el botón
    def iniciar_juego(e):
        mensaje.value = "Welcome to BRAIN RUSH! 🧠"
        page.update()

    # Título del juego
    titulo = ft.Text(
        "🧠 BRAIN RUSH",
        size=35,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.CYAN
    )

    # Descripción
    descripcion = ft.Text(
        "Test your knowledge and challenge your mind!",
        size=16,
        color=ft.Colors.WHITE
    )

    # Botón para comenzar
    boton = ft.Button(
        "START GAME",
        on_click=iniciar_juego
    )

    # Organización de los elementos
    contenido = ft.Column(
        controls=[
            titulo,
            descripcion,
            boton,
            mensaje
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=25
    )

    # Contenedor principal
    pantalla = ft.Container(
        content=contenido,
        bgcolor=ft.Colors.INDIGO_900,
        padding=40,
        border_radius=20,
        width=500
    )

    # Centrar la pantalla
    page.add(
        ft.Row(
            controls=[pantalla],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.run(main)