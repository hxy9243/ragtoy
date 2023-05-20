<template>
    <div class="document-list">
        <h1>Document List</h1>
        <ul>
            <li v-for="document in documents" :key="document.id">{{ document.name }}</li>
        </ul>
    </div>
</template>

<script>
export default {
    props: ['url'],
    data() {
        return {
            documents: [],
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
                })
                .catch((error) => {
                    console.error('Error fetching documents:', error);
                });
        },
    },
};
</script>