import gradio as gr


class DocumentComponent:

    def render(self):
        with gr.Accordion('Files'):
            with gr.Row():
                with gr.Column(scale=2):
                    with gr.Row():
                        gr.Radio(
                            label='Documents',
                            choices=['Wikipedia', 'Website'],
                        )
                    with gr.Row():
                        gr.Button('Delete')
                    with gr.Row():
                        gr.Textbox(label='URL', placeholder='URL')
                    with gr.Row():
                        gr.Textbox(label='Paste Text',
                                   lines=5,
                                   placeholder='Input text here')
                    with gr.Row():
                        gr.Textbox(placeholder='Document Name')
                        gr.Button(value='Add')

                with gr.Column(scale=4):
                    with gr.Row():
                        gr.TextArea('Alan Turning is a British computer '
                                    'scientist')


