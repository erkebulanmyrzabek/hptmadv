import { defineStore } from 'pinia';
import axios from 'axios';
import { useAuthStore } from './auth'; // Импортируем authStore для получения токена

export const useHackathonStore = defineStore('hackathon', {
  state: () => ({
    hackathons: [],
    currentHackathon: null,
  }),
  actions: {
    // Получение списка всех хакатонов
    async fetchHackathons() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_API_URL}/events/hackathons/`);
        this.hackathons = response.data;
        console.log('Хакатоны:', this.hackathons);
      } catch (error) {
        console.error('Ошибка получения хакатонов:', error.response?.data || error);
      }
    },

    // Получение деталей конкретного хакатона
    async fetchHackathonDetail(id) {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_API_URL}/events/hackathons/${id}/`);
        this.currentHackathon = response.data;
        console.log('Детали хакатона:', this.currentHackathon);
      } catch (error) {
        console.error('Ошибка получения деталей хакатона:', error.response?.data || error);
      }
    },

    // Регистрация на хакатон
    async registerForHackathon(id) {
      try {
        const authStore = useAuthStore();
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND_API_URL}/events/hackathons/${id}/register/`,
          {},
          { headers: { Authorization: `Bearer ${authStore.token}` } }
        );
        await this.fetchHackathonDetail(id); // Обновляем данные хакатона, включая is_participant
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },

    // Создание команды для хакатона
    async createTeam(id, teamName) {
      try {
        const authStore = useAuthStore();
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND_API_URL}/events/hackathons/${id}/create_team/`,
          { team_name: teamName },
          { headers: { Authorization: `Bearer ${authStore.token}` } }
        );
        await this.fetchHackathonDetail(id); // Обновляем данные после создания команды
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },

    // Присоединение к команде по коду
    async joinTeam(id, joinCode) {
      try {
        const authStore = useAuthStore();
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND_API_URL}/events/hackathons/${id}/join_team/`,
          { join_code: joinCode },
          { headers: { Authorization: `Bearer ${authStore.token}` } }
        );
        await this.fetchHackathonDetail(id); // Обновляем данные после присоединения
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },
  },
});