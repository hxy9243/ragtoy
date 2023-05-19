import logging

import gradio as gr
from gradio.blocks import BlockContext

from models.documents import Document, DocumentsApi


class DocumentComponent:

    documents: BlockContext
    delete_button: BlockContext
    url: BlockContext
    text: BlockContext
    docname: BlockContext
    add_button: BlockContext
    output: BlockContext

    def render(self):
        with gr.Accordion('Files'):
            with gr.Row():
                with gr.Column(scale=2):
                    with gr.Row():
                        self.documents = gr.Radio(
                            label='Documents',
                            choices=['Wikipedia', 'Website'],
                        )
                    with gr.Row():
                        self.delete_button = gr.Button('Delete')
                    with gr.Row():
                        self.url = gr.Textbox(label='URL', placeholder='URL')
                        self.text = gr.Textbox(label='Paste Text',
                                               lines=5,
                                               placeholder='Input text here')
                    with gr.Row():
                        self.docname = gr.Textbox(placeholder='Document Name')
                        self.add_button = gr.Button(value='Add')

                with gr.Column(scale=4):
                    with gr.Row():
                        self.output = gr.TextArea(
                            'Alan Turning is a British computer scientist',
                        )

    def run(self):
        self.add_button.click(self.add_doc,
                              [self.docname, self.url,
                               self.text],
                              [self.documents])

    def add_doc(self, docname, url, text):
        """
        Input: docname, url, text, doclist
        Output: doclist
        """

        logging.info(f'Adding new document {docname}')

        doc = DocumentsApi()
        doc.post(docname, text)

        choices = self.documents.choices
        choices.append(docname)

        return gr.update(choices=choices)
