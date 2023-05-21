<template>
    <div class="document-list">
        <h1>Chat Bot</h1>
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

    <v-row align="center" justify="center">
        <v-col cols=8 md=6>
            <ChatComponent />
        </v-col>
    </v-row>
</template>

<script>
import DocumentManage from './DocumentManage.vue'
import ChatComponent from './ChatComponent.vue'

export default {
    props: ['url'],
    components: {
        DocumentManage,
        ChatComponent,
    },
    data() {
        return {
        };
    },
    mounted() {
    },
    methods: {
    },
}
</script>