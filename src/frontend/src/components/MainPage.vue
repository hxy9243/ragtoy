<template>
    <div id="app">
        <div class="sidebar">
            <ControlPanel />
        </div>

        <div class="chat-interface">
            <div class="page-container">
                <v-row class="none" align="center" justify="center">
                    <v-col cols=12 md=6>
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
            </div>
        </div>
    </div>
</template>


<script>
import DocumentManage from './DocumentManage.vue'
import ChatComponent from './ChatComponent.vue'
import ControlPanel from './ControlPanel.vue'

export default {
    props: ['url'],
    components: {
        DocumentManage,
        ChatComponent,
        ControlPanel
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

<style>
#app {
    display: flex;
    height: 100vh;
}

.sidebar {
    width: 250px;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.chat-interface {
    width: 100%;
    display: flex;
    flex-direction: column;
    position: fixed;
}

.page-container {
    display: flex;
    width: 100%;
    min-height: 20vh;
}

.card-wrapper {
    margin-top: auto;
    flex: 1;
}

.chat-messages {
    justify-content: flex-end;
}

.none {
    display: none;
}
</style>