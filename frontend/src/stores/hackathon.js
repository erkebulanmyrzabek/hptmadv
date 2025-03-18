import { defineStore } from 'pinia';
import axios from 'axios';
import { useAuthStore } from './auth';

export const useHackathonStore = defineStore('hackathon', {
  state: () => ({
    hackathons: [],
    currentHackathon: null,
  }),
  actions: {
    async fetchHackathons() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_API_URL}/events/hackathons/`);
        this.hackathons = response.data;
      } catch (error) {
        console.error('Ошибка получения хакатонов:', error.response?.data || error);
      }
    },

    async fetchHackathonDetail(id) {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_API_URL}/events/hackathons/${id}/`);
        this.currentHackathon = response.data;
        console.log('Fetched hackathon detail:', this.currentHackathon);
      } catch (error) {
        console.error('Ошибка получения деталей хакатона:', error.response?.data || error);
      }
    },

    async registerForHackathon(id) {
      const authStore = useAuthStore();
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND_API_URL}/events/hackathons/${id}/register/`,
          { type: 'solo' },
          { headers: { Authorization: `Bearer ${authStore.token}` } }
        );
        await this.fetchHackathonDetail(id);
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },

    async createTeam(id, teamName, joinCode) {
      const authStore = useAuthStore();
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND_API_URL}/events/hackathons/${id}/register/`,
          { type: 'create_team', team_name: teamName, join_code: joinCode }, // Передаём join_code
          { headers: { Authorization: `Bearer ${authStore.token}` } }
        );
        await this.fetchHackathonDetail(id);
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },

    async joinTeam(id, joinCode) {
      const authStore = useAuthStore();
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND_API_URL}/events/hackathons/${id}/register/`,
          { type: 'join_team', join_code: joinCode },
          { headers: { Authorization: `Bearer ${authStore.token}` } }
        );
        await this.fetchHackathonDetail(id);
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },
  },
});