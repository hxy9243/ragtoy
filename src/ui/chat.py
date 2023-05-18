import gradio as gr
from gradio.blocks import BlockContext


class ChatComponent:
    textinput: BlockContext
    chatbot: BlockContext

    def render(self):
        with gr.Accordion('Chat'):
            with gr.Row():
                with gr.Column(scale=2):
                    with gr.Row():
                        gr.Number()
                    with gr.Row():
                        gr.Slider()
                    with gr.Row():
                        gr.Number()
                with gr.Column(scale=4):
                    self.chatbot = gr.Chatbot()

                    self.chatbot.style(height=600)
                    self.textinput = gr.Textbox(lines=5, interactive=True)

    def submit_text(self, msg, history):
        if history is None:
            return '', msg

        history.append([
            'You:' + msg,
            '**Bot:** Hello! Roger roger. See [google](https://google.com)'])

        return '', history

    def run(self):
        self.textinput.submit(
            self.submit_text,
            [self.textinput, self.chatbot],
            [self.textinput, self.chatbot],
        )

