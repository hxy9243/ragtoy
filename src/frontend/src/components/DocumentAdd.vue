<template>
    <v-row>
        <v-col cols="6" md="4">
            <v-dialog v-model="dialog" activator="parent">
                <v-card>
                    <v-card-text>
                        <v-row>
                            Create a new Document
                        </v-row>
                    </v-card-text>
                    <v-card-item>
                        <v-row>
                            <v-file-input label="File input" variant="solo-filled"></v-file-input>
                        </v-row>
                    </v-card-item>
                    <v-card-actions>
                        <v-row>
                            <v-col>
                                <v-btn color="red" block @click="dialog = false">Close
                                    Dialog</v-btn>
                            </v-col>
                            <v-col>
                                <v-btn color="green" block @click="addDocument">Add</v-btn>
                            </v-col>
                        </v-row>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-col>
    </v-row>
</template>

<script>
export default {
    props: ['url'],
    name: 'AddDocument',
    data() {
        return {
            documents: [],
            documentMap: {},
            documentBody: '',
            selectedDocument: null,
            dialog: null,
        };
    },
    methods: {
        addDocument() {
            this.$emit('addDocument', {
                'id': '1234',
                'name': 'yeah',
                'body': 'WOWWOWO',
            })
            this.dialog = false;
        },
    },
};
</script>
