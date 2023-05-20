import logging

import gradio as gr
from gradio.blocks import BlockContext

from models.documents import Document, DocumentsApi


class DocumentComponent:
    docapi = DocumentsApi()

    documents: BlockContext
    delete_button: BlockContext
    url: BlockContext
    text: BlockContext
    docname: BlockContext
    add_button: BlockContext
    output: BlockContext

    def get_docs(self):
        return self.docapi.get()

    @property
    def docnames(self):
        return [doc['name'] for doc in self.get_docs()]

    def render(self):
        with gr.Accordion('Files'):
            with gr.Row():
                with gr.Column(scale=2):
                    with gr.Row():
                        # self.documents = gr.Radio(
                        #     label='Documents',
                        #     choices=self.docnames,
                        #     type='index',
                        #     interactive=True,
                        # )
                        self.documents = gr.DataFrame(
                            headers=['documents'],
                            datatype=['str'],
                            col_count=(1, "fixed"),
                            value=[[doc] for doc in self.docnames],
                        )
                    with gr.Row():
                        self.delete_button = gr.Button('Delete', variant='stop')
                    with gr.Row():
                        self.docname = gr.Textbox(placeholder='Document Name')
                    with gr.Row():
                        self.url = gr.Textbox(label='URL', placeholder='URL')
                    with gr.Row():
                        self.text = gr.Textbox(label='Paste Text',
                                               lines=5,
                                               placeholder='Input text here')
                    with gr.Row():
                        self.add_button = gr.Button(value='Add',
                                                    variant='main')

                with gr.Column(scale=4):
                    with gr.Row():
                        self.output = gr.TextArea(
                            placeholder='Choose the document to display text',
                        )
                        self.output.style(show_copy_button=True)

    def add_doc(self, docname, url, text):
        """ callback for clicking on adding documents
        inputs: docname, url, text
        outputs: doclist
        """

        logging.info(f'Adding new document {docname}')

        self.docapi.post(docname, text)

        docs = self.get_docs()
        return '', '', '', gr.update(value=[[doc['name'] for doc in docs]]), text

    def delete_doc(self, docidx):
        """ callback for deleting
        inputs: event
        output: documents
        """
        logging.debug(f'Deleting document {docidx}')

        docs = self.get_docs()
        doc = docs[docidx.index[0]]

        self.docapi.delete(doc['id'])
        docs = self.get_docs()

        logging.info(f'Getting updated document list: {[doc["name"] for doc in docs]}')

        # gr.update(choices=[doc['name'] for doc in docs], value=None)

        return gr.update(value=[[doc['name']] for doc in docs])

    def select_doc(self, evt: gr.SelectData):
        """ select document to examine the contents
        inputs: doclist
        output: output
        """
        docs = self.get_docs()

        logging.debug(f'Selecting document {evt.index}')

        return docs[evt.index[0]]['body']

    def run(self):
        self.add_button.click(self.add_doc,
                              [self.docname, self.url, self.text],
                              [self.docname, self.url, self.text,
                               self.documents, self.output])
        self.delete_button.click(self.delete_doc,
                                 [self.documents],
                                 self.documents)
        self.documents.select(self.select_doc,
                              None,
                              self.output)
