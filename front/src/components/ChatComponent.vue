<template>
    <div class="chat-container">
        <div class="chat-header" @click="toggleChat">
            Chat
        </div>
        <div class="chat-content" v-if="isChatOpen">
            <div class="friends-list" v-if="!selectedFriend">
                <div v-for="friend in friends" :key="friend.id" @click="selectFriend(friend)">
                    {{ friend.username }}
                </div>
                <div v-if="!friends || friends.length === 0">
                    Add some friends to start chatting
                </div>
            </div>
            <div v-else>
                <button @click="selectedFriend = null">Back to friends list</button>
                <div v-for="message in messages" :key="message.id">
                    {{ message.text }}
                </div>
                <input v-model="newMessage" @keyup.enter="sendMessage">
            </div>
        </div>
    </div>
</template>

<script>
import io from 'socket.io-client';
import axios from 'axios';

export default {
    data() {
        return {
            isChatOpen: false,
            newMessage: '',
            messages: [],
            socket: null,
            friends: [],
            selectedFriend: null,
            userId: 1, //update according to user id
        };
    },
    created() {
        this.socket = io('http://localhost:5000');
        this.socket.on('message', (message) => {
            this.messages.push({ id: this.messages.length, text: message.message });
        });
        this.socket.on('error', (error) => {
            console.error(error);
        });
        this.fetchFriends();
    },
    methods: {
        toggleChat() {
            this.isChatOpen = !this.isChatOpen;
        },
        sendMessage() {
            if (this.selectedFriend && this.newMessage.trim() !== '') {
                this.socket.emit('message', {
                    sender_id: this.userId,
                    receiver_id: this.selectedFriend.id,
                    message: this.newMessage,
                });
                this.messages.push({ id: this.messages.length, text: this.newMessage });
                this.newMessage = '';
            }
        },
        fetchFriends() {
            axios.get('http://localhost:5000/matches_chat', { user_id: this.userId })
                .then(response => {
                    this.friends = response.data.friends;
                });
        },
        selectFriend(friend) {
            this.selectedFriend = friend;
            this.messages = [];
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
    background-color: #f500f5;
    padding: 10px;
    cursor: pointer;
}

.chat-content {
    background-color: #00f5f5;
    height: 300px;
    overflow-y: auto;
}

.friends-list {
    background-color: #00f5f5;
    padding: 10px;
}
</style>
