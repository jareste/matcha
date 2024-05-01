<template>
    <div class="chat-container">
        <div class="chat-header" @click="toggleChat">
            Chat
        </div>
        <div class="chat-content" v-if="isChatOpen">
            <!-- Chat content goes here -->
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            isChatOpen: false,
        };
    },
    methods: {
        toggleChat() {
            this.isChatOpen = !this.isChatOpen;
        },
    },
};
</script>

<style scoped>
.chat-container {
    position: fixed;
    bottom: 0;
    right: 0;
    width: 300px;
    border: 1px solid #ccc;
}

.chat-header {
    background-color: #f5f5f5;
    padding: 10px;
    cursor: pointer;
}

.chat-content {
    height: 300px;
    overflow-y: auto;
}
</style>