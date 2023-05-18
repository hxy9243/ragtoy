import gradio as gr

class SettingComponent:

    def render(self):
        gr.Textbox(label='OpenAI Token',
                    placeholder='st-xxxx',
                    type='password')