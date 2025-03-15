import { defineStore } from 'pinia';
import axios from 'axios';

export const useHackathonStore = defineStore('hackathon', {
  state: () => ({
    hackathons: [],
    currentHackathon: null,
  }),
  actions: {
    async fetchHackathons() {
      try {
        const response = await axios.get('http://localhost:8000/api/events/hackathons/');
        this.hackathons = response.data;
        console.log('Хакатоны:', this.hackathons);
      } catch (error) {
        console.error('Ошибка получения хакатонов:', error.response?.data || error);
      }
    },
    async fetchHackathonDetail(id) {
      try {
        const response = await axios.get(`http://localhost:8000/api/events/hackathons/${id}/`);
        this.currentHackathon = response.data;
        console.log('Детали хакатона:', this.currentHackathon);
      } catch (error) {
        console.error('Ошибка получения деталей хакатона:', error.response?.data || error);
      }
    },
    async registerForHackathon(id) {
      try {
        const authStore = useAuthStore();
        const response = await axios.post(
          `http://localhost:8000/api/events/hackathons/${id}/register/`,
          {},
          { headers: { Authorization: `Bearer ${authStore.token}` } }
        );
        await this.fetchHackathonDetail(id); // Обновляем статус is_participant
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },
    async createTeam(id, teamName) {
      try {
        const authStore = useAuthStore();
        const response = await axios.post(
          `http://localhost:8000/api/events/hackathons/${id}/create_team/`,
          { team_name: teamName },
          { headers: { Authorization: `Bearer ${authStore.token}` } }
        );
        await this.fetchHackathonDetail(id);
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },
    async joinTeam(id, joinCode) {
      try {
        const authStore = useAuthStore();
        const response = await axios.post(
          `http://localhost:8000/api/events/hackathons/${id}/join_team/`,
          { join_code: joinCode },
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

import { useAuthStore } from './auth'; // Импортируем authStore для получения токена