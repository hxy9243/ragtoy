from dataclasses import dataclass
import gradio as gr
from gradio.blocks import BlockContext

from ui.document import DocumentComponent
from ui.chat import ChatComponent
from ui.setting import SettingComponent


@dataclass
class App():
    document: BlockContext
    chat: BlockContext
    setting: BlockContext

    def render(self):
        with gr.Blocks() as demo:

            with gr.Tab('Chat'):
                with gr.Accordion('Documents'):
                    self.document.render()
                with gr.Accordion('Chat'):
                    self.chat.render()

            with gr.Tab('Settings'):
                self.setting.render()

            self.chat.run()

            return demo


app = App(
    document=DocumentComponent(),
    chat=ChatComponent(),
    setting=SettingComponent(),
)
demo = app.render()

demo.launch(server_name='0.0.0.0')
