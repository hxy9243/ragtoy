<template>
    <div class="container">
        <div class="page-container parent-card scroller" align="left">
            <div class="card-wrapper">
                <v-card v-for="message in messages" class="child-card" :key="message" :label="message">
                    <v-card-text class="card-text">
                        {{ message }}
                    </v-card-text>
                </v-card>
            </div>
        </div>
        <div>
            <v-row class="card-wrapper" align="center" justify="center">
                <v-col>
                    <v-textarea label="Ask something here" hint="Hit Enter to send, Shift+Enter to change lines"
                        variant="solo" v-model="inputText" :rows="getNumRows" auto-grow max-rows="10"
                        @keydown="handleKeydown" append-inner-icon='mdi-send' focus></v-textarea>
                </v-col>
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
    background-color: #dffffc;
}

.parent-card .child-card:nth-child(odd) {
    background-color: #93e7f6;
}

.child-card {
    margin-bottom: 5px;
}

.scroller {
    overflow-y: scroll;
    max-height: 100%;
}

.page-container {
    display: flex;
    flex-direction: column;
    height: 60vh;
}

.card-wrapper {
    flex: 1;
}

.card-text {
    white-space: pre-line;
}
</style>