<template>
    <v-card align="left">
        <v-card-title>
            Chat
        </v-card-title>
        <v-card-text>
            This is the chat
        </v-card-text>
    </v-card>
    <v-card>
        <v-row align="center" justify="center">
            <v-col>
                <v-textarea label="Ask something here" hint="Hit Enter to send, Shift+Enter to change lines" variant="solo"
                    v-model="inputText" :rows="getNumRows" auto-grow max-rows="10" @keydown="handleKeydown"
                    append-inner-icon='mdi-send' focus></v-textarea>
            </v-col>
        </v-row>
    </v-card>
</template>

<script>
export default {
    props: [],
    components: {
    },
    data() {
        return {
            inputText: '',
            numRows: 1,
        };
    },
    mounted() {
    },
    methods: {
        handleKeydown(event) {
            if (event.key === 'Enter') {
                if (event.shiftKey) {
                    // Shift + Enter key combination to add lines
                    return;
                } else {
                    // Enter key: Submit the form
                    console.log(this.inputText);

                    event.preventDefault();
                    this.inputText = ''
                }
            }
        },
    },
    computed: {
        getNumRows() {
            return this.inputText.split('\n').length;
        },
    }
}
</script>