import gradio as gr
from gradio.blocks import BlockContext

from ui.document import DocumentComponent
from ui.chat import ChatComponent
from ui.setting import SettingComponent


class GradioApp():
    document: BlockContext
    chat: BlockContext
    setting: BlockContext

    def launch(self, *args, **kwargs):
        self.document = DocumentComponent()
        self.chat = ChatComponent()
        self.setting = SettingComponent()

        with gr.Blocks() as demo:
            with gr.Tab('Chat'):
                with gr.Accordion('Documents'):
                    self.document.render()
                with gr.Accordion('Chat'):
                    self.chat.render()

            with gr.Tab('Settings'):
                self.setting.render()

            self.chat.run()

            self.document.run()

            demo.launch(*args, **kwargs)


