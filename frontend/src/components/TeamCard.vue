<template>
    <div class="team-card">
      <h3>{{ team.name }}</h3>
      <p>Код: {{ team.join_code }} <button @click="copyCode">Скопировать</button></p>
      <p>Участники: {{ team.members.length }} / {{ team.max_members }}</p>
      <div v-if="isLeader">
        <button v-for="member in team.members" :key="member.id" @click="kickMember(member.id)" v-if="member.id !== authStore.user.id">
          Выгнать {{ member.first_name }}
        </button>
        <input v-model="newMaxMembers" type="number" min="1" max="4" />
        <button @click="setMaxMembers">Изменить лимит</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { useAuthStore } from '../stores/auth';
  
  export default {
    props: ['team-id'],
    data() {
      return {
        team: {},
        newMaxMembers: null,
      };
    },
    setup() {
      return { authStore: useAuthStore() };
    },
    computed: {
      isLeader() {
        return this.team.created_by === this.authStore.user.id;
      },
    },
    async created() {
      const response = await axios.get(`${import.meta.env.VITE_BACKEND_API_URL}/api/teams/${this.teamId}/`, {
        headers: { Authorization: `Bearer ${this.authStore.token}` },
      });
      this.team = response.data;
      this.newMaxMembers = this.team.max_members;
    },
    methods: {
      async copyCode() {
        await navigator.clipboard.writeText(this.team.join_code);
        alert('Код скопирован!');
      },
      async kickMember(memberId) {
        await axios.post(
          `${import.meta.env.VITE_BACKEND_API_URL}/api/teams/${this.teamId}/kick/`,
          { member_id: memberId },
          { headers: { Authorization: `Bearer ${this.authStore.token}` } }
        );
        this.team.members = this.team.members.filter(m => m.id !== memberId);
      },
      async setMaxMembers() {
        await axios.patch(
          `${import.meta.env.VITE_BACKEND_API_URL}/api/teams/${this.teamId}/`,
          { max_members: this.newMaxMembers },
          { headers: { Authorization: `Bearer ${this.authStore.token}` } }
        );
        this.team.max_members = this.newMaxMembers;
      },
    },
  };
  </script>
  
  <style scoped>
  .team-card {
    padding: 15px;
    background: var(--tg-theme-secondary-bg-color, #f0f0f0);
    border-radius: 10px;
    margin: 10px 0;
    transition: transform 0.2s;
  }
  .team-card:hover {
    transform: scale(1.02);
  }
  button {
    margin: 5px;
    padding: 5px 10px;
    background: var(--tg-theme-button-color, #007bff);
    color: var(--tg-theme-button-text-color, #ffffff);
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  button:hover {
    background: var(--tg-theme-button-color-hover, #0056b3);
  }
  </style>