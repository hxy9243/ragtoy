<template>
    <div class="document-list">
        <h1>Document List</h1>
    </div>

    <v-row align="center" justify="center">
        <v-col cols=8 md=6>
            <v-expansion-panels>
                <v-expansion-panel title="Documents" variant="accordion">
                    <v-expansion-panel-text>

                        <DocumentManage :url=this.url />

                    </v-expansion-panel-text>
                </v-expansion-panel>
            </v-expansion-panels>
        </v-col>
    </v-row>
</template>

<script>
import DocumentManage from './DocumentManage.vue'

export default {
    props: ['url'],
    components: {
        DocumentManage,
    },
    data() {
        return {
            // documents: [],
            // documentMap: {},
            // documentBody: '',
            // selectedDocument: null,
            // dialog: null,
        };
    },
    mounted() {
        // this.fetchDocuments();
    },
    methods: {
        //     fetchDocuments() {
        //         // Make an API request to fetch the documents from your backend
        //         // Replace the URL with your actual API endpoint
        //         fetch(this.url + '/api/documents')
        //             .then((response) => response.json())
        //             .then((data) => {
        //                 this.documents = data;
        //                 this.documentMap = data.reduce((map, object) => {
        //                     map[object.id] = object;
        //                     return map;
        //                 }, {});
        //             })
        //             .catch((error) => {
        //                 console.error('Error fetching documents:', error);
        //             });
        //     },
        //     handleSelectDocument(value) {
        //         console.log(this.documentMap[value].body);

        //         this.documentBody = this.documentMap[value].body;
        //     },
        // },
    },
}
</script>