import os
import time
import flet as ft

def main(page: ft.Page):
    # Configurações da janela
    page.title = "Agendador de Desligamento"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#3A0CA3"  # Cor de fundo roxa
    page.padding = 50

    # Função para agendar o desligamento
    def agendar_desligamento(e):
        opcao = dropdown_opcao.value

        if opcao == "horario":
            horario = input_horario.value
            try:
                hora_definida = time.strptime(horario, '%H:%M')
                segundos_atual = time.mktime(time.localtime())
                segundos_definido = time.mktime((time.localtime()[:3] + hora_definida[3:6] + (-1, -1, -1)))
                segundos_para_desligar = int(segundos_definido - segundos_atual)

                if segundos_para_desligar > 0:
                    os.system(f"shutdown /s /t {segundos_para_desligar}")
                    label_feedback.value = f"💡 Desligamento agendado para {horario}."
                    label_feedback.color = "green"
                else:
                    label_feedback.value = "⚠️ Horário inválido! Deve ser um horário futuro."
                    label_feedback.color = "red"
            except ValueError:
                label_feedback.value = "❌ Formato de horário inválido! Use HH:MM."
                label_feedback.color = "red"
        
        elif opcao == "tempo":
            horas = input_horas.value or "0"
            minutos = input_minutos.value or "0"

            try:
                horas = int(horas)
                minutos = int(minutos)
                segundos_para_desligar = (horas * 3600) + (minutos * 60)

                if segundos_para_desligar > 0:
                    os.system(f"shutdown /s /t {segundos_para_desligar}")
                    label_feedback.value = f"💡 Desligamento agendado para {horas} horas e {minutos} minutos."
                    label_feedback.color = "green"
                else:
                    label_feedback.value = "⚠️ O tempo deve ser maior que zero!"
                    label_feedback.color = "red"
            except ValueError:
                label_feedback.value = "❌ Insira valores válidos para horas e minutos."
                label_feedback.color = "red"

        page.update()

    # Função para cancelar o desligamento
    def cancelar_desligamento(e):
        os.system("shutdown /a")
        label_feedback.value = "❌ Desligamento cancelado!"
        label_feedback.color = "blue"
        page.update()

    # Título principal
    titulo = ft.Text("Escolha como agendar o desligamento", size=20, color="blue", weight="bold")

    # Dropdown para selecionar como agendar o desligamento
    dropdown_opcao = ft.Dropdown(
        width=250,
        options=[
            ft.dropdown.Option("horario", "Por horário (HH:MM)"),
            ft.dropdown.Option("tempo", "Por tempo (Horas/Minutos)")
        ],
        label="Método de agendamento",
        value="horario",
        border_color="black",
        bgcolor="white"
    )

    # Inputs para o horário e tempo
    input_horario = ft.TextField(label="Horário (HH:MM)", width=300, border_color="gray", bgcolor="white")
    input_horas = ft.TextField(label="Horas", width=140, border_color="gray", bgcolor="white")
    input_minutos = ft.TextField(label="Minutos", width=140, border_color="gray", bgcolor="white")

    # Botão para confirmar o agendamento
    button_confirmar = ft.ElevatedButton(
        text="Agendar Desligamento",
        bgcolor="#f72585",  # Cor de fundo rosa
        color="white",
        width=200,
        on_click=agendar_desligamento
    )

    # Botão para cancelar o desligamento
    button_cancelar = ft.ElevatedButton(
        text="Cancelar Desligamento",
        bgcolor="#ff0000",  # Cor vermelha para cancelamento
        color="white",
        width=200,
        on_click=cancelar_desligamento
    )

    # Label para mostrar feedback de sucesso ou erro
    label_feedback = ft.Text(value="", color="blue", size=16)

    # Layout e organização dos elementos
    page.add(
        ft.Container(
            content=ft.Column([
                titulo,  # Título acima
                dropdown_opcao,
                input_horario,
                ft.Row([input_horas, input_minutos], spacing=10),
                button_confirmar,
                button_cancelar,  # Botões embaixo um do outro
                label_feedback
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=30,
            border_radius=15,
            bgcolor="white",
            width=400,
            shadow=ft.BoxShadow(blur_radius=20, spread_radius=5, color=ft.colors.GREY)
        )
    )

# Inicia o app
ft.app(target=main)
