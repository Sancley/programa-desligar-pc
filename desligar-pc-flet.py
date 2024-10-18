import os   # Módulo usado para enviar comandos ao sistema operacional, como o desligamento.
import time # Módulo utilizado para manipulação de horários e contagem de tempo.
import flet as ft  # Biblioteca Flet, usada para criar interfaces gráficas (UI) com Python.

# Função principal que será executada ao iniciar o programa
def main(page: ft.Page):
    # Configurações da janela principal
    page.title = "Agendar Desligamento"  # Título da janela
    page.vertical_alignment = ft.MainAxisAlignment.START  # Alinha os elementos na parte superior da janela

    # Função que será chamada quando o usuário clicar no botão "Confirmar"
    def agendar_desligamento(e):
        # Verifica qual opção o usuário selecionou no dropdown: "horário" ou "tempo"
        opcao = dropdown_opcao.value

        if opcao == "horario":  # Se a opção for "Por horário (HH:MM)"
            horario = input_horario.value  # Obtém o valor inserido pelo usuário (formato HH:MM)
            try:
                # Converte o horário inserido para um formato de tempo utilizável
                hora_definida = time.strptime(horario, '%H:%M')
                segundos_atual = time.mktime(time.localtime())  # Obtém o tempo atual em segundos
                segundos_definido = time.mktime((time.localtime()[:3] + hora_definida[3:6] + (-1, -1, -1)))
                # Calcula quantos segundos faltam até o horário definido pelo usuário
                segundos_para_desligar = int(segundos_definido - segundos_atual)

                # Se o tempo até o desligamento for maior que 0, agenda o desligamento
                if segundos_para_desligar > 0:
                    os.system(f"shutdown /s /t {segundos_para_desligar}")  # Comando para desligar o PC
                    label_feedback.value = f"Desligamento agendado para {horario}."  # Mostra mensagem de sucesso
                else:
                    # Se o horário definido já passou, avisa o usuário
                    label_feedback.value = "Horário inválido! Deve ser um horário futuro."
            except ValueError:
                # Se o usuário inserir um horário com formato errado, avisa sobre o erro
                label_feedback.value = "Formato de horário inválido! Use HH:MM."
        
        elif opcao == "tempo":  # Se a opção for "Por tempo (Horas/Minutos)"
            horas = input_horas.value or "0"  # Obtém o valor de horas (ou 0 se estiver vazio)
            minutos = input_minutos.value or "0"  # Obtém o valor de minutos (ou 0 se estiver vazio)

            try:
                horas = int(horas)  # Converte o valor de horas para inteiro
                minutos = int(minutos)  # Converte o valor de minutos para inteiro
                # Calcula quantos segundos faltam com base nas horas e minutos inseridos
                segundos_para_desligar = (horas * 3600) + (minutos * 60)

                # Se o tempo definido for maior que 0, agenda o desligamento
                if segundos_para_desligar > 0:
                    os.system(f"shutdown /s /t {segundos_para_desligar}")  # Comando para desligar o PC
                    label_feedback.value = f"Desligamento agendado para {horas} horas e {minutos} minutos."
                else:
                    # Se o tempo for zero ou negativo, avisa o usuário
                    label_feedback.value = "O tempo deve ser maior que zero!"
            except ValueError:
                # Se o usuário inserir valores inválidos (não numéricos), avisa sobre o erro
                label_feedback.value = "Insira valores válidos para horas e minutos."

        # Atualiza a interface para exibir o feedback (mensagem) ao usuário
        page.update()

    # Componente Dropdown para escolher a forma de agendamento (por horário ou tempo)
    dropdown_opcao = ft.Dropdown(
        width=200,  # Largura do dropdown
        options=[  # Opções dentro do dropdown
            ft.dropdown.Option("horario", "Por horário (HH:MM)"),  # Agendar por horário
            ft.dropdown.Option("tempo", "Por tempo (Horas/Minutos)")  # Agendar por tempo
        ],
        label="Escolha como deseja agendar o desligamento",  # Rótulo do dropdown
        value="horario",  # Valor padrão selecionado (horário)
    )

    # Campo de entrada para definir o horário (formato HH:MM)
    input_horario = ft.TextField(label="Defina o horário (HH:MM)", width=200)

    # Campos de entrada para definir o tempo (horas e minutos)
    input_horas = ft.TextField(label="Horas", width=100)  # Campo para horas
    input_minutos = ft.TextField(label="Minutos", width=100)  # Campo para minutos

    # Botão que o usuário clica para confirmar o agendamento
    button_confirmar = ft.ElevatedButton(text="Confirmar", on_click=agendar_desligamento)

    # Label para exibir feedback ao usuário (mensagens de sucesso ou erro)
    label_feedback = ft.Text(value="", color="blue")

    # Adiciona todos os componentes à interface na ordem que aparecerão
    page.add(
        dropdown_opcao,  # Dropdown para escolha de modo de agendamento
        input_horario,   # Campo para horário
        ft.Row([input_horas, input_minutos], alignment=ft.MainAxisAlignment.START),  # Campos para tempo
        button_confirmar,  # Botão de confirmação
        label_feedback  # Feedback para o usuário
    )

# Inicia o aplicativo Flet
ft.app(target=main)
