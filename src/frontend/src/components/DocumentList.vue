<template>
    <div class="document-list">
        <h1>Document List</h1>
    </div>

    <v-row align="center" justify="center">
        <v-col cols=8 md=6>
            <v-expansion-panels>
                <v-expansion-panel title="Documents" variant="accordion">
                    <v-expansion-panel-text>
                        <v-container>
                            <v-row>
                                <v-col cols=4>
                                    <v-card>
                                        <v-card-item>
                                            <v-row>
                                                <v-select v-model=selectedDocument label="Documents" :items=this.documents
                                                    item-title="name" item-value="id"
                                                    @update:modelValue="handleSelectDocument"></v-select>
                                            </v-row>
                                        </v-card-item>

                                        <v-card-actions>
                                            <v-row>
                                                <v-btn color="red">Delete</v-btn>

                                                <v-btn color="green">Add
                                                    <v-dialog v-model="dialog" activator="parent">
                                                        <v-card>
                                                            <v-card-text>
                                                                <v-row>
                                                                    Create a new Document
                                                                </v-row>
                                                            </v-card-text>
                                                            <v-card-item>
                                                                <v-row>
                                                                    <v-file-input label="File input"
                                                                        variant="solo-filled"></v-file-input>
                                                                </v-row>
                                                            </v-card-item>
                                                            <v-card-actions>
                                                                <v-row>
                                                                    <v-col>
                                                                        <v-btn color="red" block
                                                                            @click="dialog = false">Close
                                                                            Dialog</v-btn>
                                                                    </v-col>
                                                                    <v-col>
                                                                        <v-btn color="green" block
                                                                            @click="dialog = false">Add</v-btn>
                                                                    </v-col>
                                                                </v-row>
                                                            </v-card-actions>
                                                        </v-card>

                                                    </v-dialog>
                                                </v-btn>
                                            </v-row>
                                        </v-card-actions>
                                    </v-card>
                                </v-col>
                                <v-col cols=8>
                                    <div>
                                        <v-textarea v-model="documentBody" readonly=false>
                                        </v-textarea>
                                    </div>
                                </v-col>

                            </v-row>
                        </v-container>
                    </v-expansion-panel-text>
                </v-expansion-panel>
            </v-expansion-panels>
        </v-col>
    </v-row>
</template>

<script>
export default {
    props: ['url'],
    data() {
        return {
            documents: [],
            documentMap: {},
            documentBody: '',
            selectedDocument: null,
            dialog: null,
        };
    },
    mounted() {
        this.fetchDocuments();
    },
    methods: {
        fetchDocuments() {
            // Make an API request to fetch the documents from your backend
            // Replace the URL with your actual API endpoint
            fetch(this.url + '/api/documents')
                .then((response) => response.json())
                .then((data) => {
                    this.documents = data;
                    this.documentMap = data.reduce((map, object) => {
                        map[object.id] = object;
                        return map;
                    }, {});
                })
                .catch((error) => {
                    console.error('Error fetching documents:', error);
                });
        },
        handleSelectDocument(value) {
            console.log(this.documentMap[value].body);

            this.documentBody = this.documentMap[value].body;
        },
    },
};
</script>