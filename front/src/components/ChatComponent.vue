<template>
    <div class="chat-container">
        <div class="chat-header" @click="toggleChat">
            Chat
        </div>
        <div class="chat-content" v-if="isChatOpen">
            <div v-for="message in messages" :key="message.id">
                {{ message.text }}
            </div>
            <input v-model="newMessage" @keyup.enter="sendMessage">
        </div>
    </div>
</template>

<script>
import io from 'socket.io-client';

export default {
    data() {
        return {
            isChatOpen: false,
            newMessage: '',
            messages: [],
            socket: null,
        };
    },
    created() {
        this.socket = io('http://localhost:5000');
        this.socket.on('message', (message) => {
            this.messages.push({ id: this.messages.length, text: message });
            console.log(this.messages);
        });
    },
    methods: {
        toggleChat() {
            this.isChatOpen = !this.isChatOpen;
        },
        sendMessage() {
            this.socket.emit('message', this.newMessage);
            this.newMessage = '';
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