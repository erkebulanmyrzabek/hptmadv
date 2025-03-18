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
      const authStore = useAuthStore();
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_API_URL}/api/events/hackathons/`, {
          headers: { Authorization: `Bearer ${authStore.token}` },
        });
        this.hackathons = response.data;
      } catch (error) {
        console.error('Ошибка получения хакатонов:', error.response?.data || error);
      }
    },

    async fetchHackathonDetail(id) {
      const authStore = useAuthStore();
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_API_URL}/api/events/hackathons/${id}/`, {
          headers: { Authorization: `Bearer ${authStore.token}` },
        });
        this.currentHackathon = response.data;
        this.currentHackathon.is_participant = await this.checkParticipant(id);
        console.log('Fetched hackathon detail:', this.currentHackathon);
      } catch (error) {
        console.error('Ошибка получения деталей хакатона:', error.response?.data || error);
        throw error;
      }
    },

    async checkParticipant(hackathonId) {
      const authStore = useAuthStore();
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_API_URL}/api/teams/`, {
          headers: { Authorization: `Bearer ${authStore.token}` },
          params: { hackathon_id: hackathonId },
        });
        const teams = response.data;
        return teams.some(team => team.members.some(member => member.id === authStore.user.id));
      } catch (error) {
        console.error('Ошибка проверки регистрации:', error);
        return false;
      }
    },

    async createTeam(hackathonId, teamName) {
      const authStore = useAuthStore();
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND_API_URL}/api/teams/`,
          { hackathon: hackathonId, name: teamName, max_members: 4 },
          { headers: { Authorization: `Bearer ${authStore.token}` } }
        );
        await this.fetchHackathonDetail(hackathonId);
        return response.data;
      } catch (error) {
        console.error('Ошибка при создании команды:', error.response?.data || error);
        throw error.response?.data || { detail: 'Не удалось создать команду' };
      }
    },

    async joinTeam(hackathonId, joinCode) {
      const authStore = useAuthStore();
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND_API_URL}/api/teams/join/`,
          { join_code: joinCode },
          { headers: { Authorization: `Bearer ${authStore.token}` } }
        );
        await this.fetchHackathonDetail(hackathonId);
        return response.data;
      } catch (error) {
        console.error('Ошибка при присоединении к команде:', error.response?.data || error);
        throw error.response?.data || { detail: 'Не удалось присоединиться к команде' };
      }
    },
  },
});