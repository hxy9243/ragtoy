<template>
    <div class="container">
        <div class="page-container parent-card scroller messages" align="left">
            <v-card v-for="message in messages" class="child-card" :key="message" :label="message">
                <v-card-text class="card-text">
                    {{ message }}
                </v-card-text>
            </v-card>
        </div>
        <div>
            <v-row class="message-input" align="center" justify="center">
                <v-textarea label="Ask something here" hint="Hit Enter to send, Shift+Enter to change lines" variant="solo"
                    v-model="inputText" :rows="getNumRows" auto-grow max-rows="10" @keydown="handleKeydown"
                    append-inner-icon='mdi-send' focus></v-textarea>
            </v-row>
        </div>
    </div>
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
            messages: [
                "Hello world",
                "Hello, how may I help you?",
                "Ask some questions",
            ],
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

                    this.messages.push(this.inputText);

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

<style>
.parent-card .child-card:nth-child(even) {
    background-color: #efefef;
}

.parent-card .child-card:nth-child(odd) {
    background-color: #cacaca;
}

.child-card {
    margin-bottom: 5px;
}

.scroller {
    overflow-y: scroll;
}

.page-container {
    display: flex;
    width: 100%;
    height: 100vh;
    flex-direction: column;
}

.messages {
    top: 0;
    bottom: 60px;
    position: relative;
}

.message-input {
    padding: 10px;
    position: absolute;
    bottom: 0;
}

.card-text {
    white-space: pre-line;
}
</style>