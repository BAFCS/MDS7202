from services import enviar_prediccion
import gradio as gr
from datetime import datetime



with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # ChaucherApp
        ## Clasificador de tickets
        """
    )
    with gr.Row(): #Generamos una fila
        with gr.Column():
            gr.Markdown("### Ingrese información del ticket")
            asunto_ticket = gr.Textbox(label = "Asunto del ticket", placeholder= "Ingrese el asunto del ticket")
            contenido = gr.TextArea(label="Contenido del ticket", placeholder = "Ingrese el contenido del ticket")
            canal = gr.Dropdown(label="Canal de entrada", choices= ["Whatsapp", "Correo", "Página Web"], value="Página Web", interactive=True)
            categoria_Problema = gr.Dropdown(label = "Categoría del ticket", choices=["Cuenta", "Fraude", "Técnica", "Pregunta general", "Cobros", "Otro"], value="Cuenta", interactive=True)

        #Separamos la información del ticket con la del usuario
        with gr.Column():
            gr.Markdown("### Ingrese información del usuario")
            Usuario_Tipo_de_Cuenta = gr.Dropdown(label = "Tipo de cuenta del usuario", choices=["Free", "Premium", "Business"], value="Free", interactive=True)
            Usuario_Antiguedad_Cuenta_Dias = gr.Number(label = "Días de antiguedad del usuario", precision=0) #precision es el número de decimales

    with gr.Row():
        boton_predecir = gr.Button("Envíar predicción", variant="primary")

    #Resultado
    with gr.Row():
        gr.Markdown("### Resultado de la predicción")
        id_salida = gr.Textbox(label="ID de Control asignado", interactive=False)
        resultado_prioridad = gr.Textbox(label="Prioridad Asignada por MLP", interactive=False)


    boton_predecir.click(
        fn=enviar_prediccion,
        inputs=[asunto_ticket, contenido, canal, categoria_Problema, Usuario_Tipo_de_Cuenta, Usuario_Antiguedad_Cuenta_Dias], outputs=[id_salida, resultado_prioridad]
    )



if __name__=="__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)

