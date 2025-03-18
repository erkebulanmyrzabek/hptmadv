import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
  }),
  actions: {
    async login(initData) {
      try {
        const response = await axios.post(`${import.meta.env.VITE_BACKEND_API_URL}/api/users/telegram-auth/`, initData);
        const { access } = response.data;
        this.token = access;
        localStorage.setItem('token', access);
        await this.fetchUser();
      } catch (error) {
        console.error('Ошибка авторизации:', error.response?.data || error);
        throw error.response?.data || { detail: 'Ошибка авторизации' };
      }
    },
    async fetchUser() {
      if (!this.token) {
        throw new Error('Токен отсутствует');
      }
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_API_URL}/api/users/profile/`, {
          headers: { Authorization: `Bearer ${this.token}` },
        });
        this.user = response.data;
        console.log('Данные пользователя в Pinia:', this.user);
      } catch (error) {
        console.error('Ошибка получения данных:', error.response?.data || error);
        this.logout();
        throw error.response?.data || { detail: 'Не удалось загрузить данные пользователя' };
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
    },
  },
});
