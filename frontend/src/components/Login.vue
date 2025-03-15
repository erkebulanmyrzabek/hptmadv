<template>
  <div>
    <!-- Кнопка для входа как тестовый пользователь -->
    <button @click="loginWithTestUser" :disabled="loading">Войти как тестовый пользователь</button>
    <!-- Индикатор загрузки -->
    <p v-if="loading">Авторизация...</p>
  </div>
</template>

<script>
// Раскомментируйте следующую строку, когда будете использовать Telegram SDK
// import TelegramWebApp from '@twa-dev/sdk';
import { useAuthStore } from '../stores/auth'; // Импорт Pinia store

export default {
  data() {
    return {
      loading: false, // Состояние загрузки
    };
  },
  methods: {
    async loginWithTestUser() {
      this.loading = true;
      const authStore = useAuthStore();
      try {
        // Тестовые данные пользователя (имитация Telegram initData) TODO: Еркебулан потом удали
        const testUserData = {
          id: "123456789",
          first_name: "Test",
          last_name: "User",
          username: "testuser",
          hash: "mock_hash", // Моковый хэш для теста
        };

        //TODO: Еркебулан это включи
        // const initData = TelegramWebApp.initData;
        // if (!initData) {
        //   throw new Error('Telegram initData не доступен');
        // }
        // const initDataObj = Object.fromEntries(new URLSearchParams(initData));

        await authStore.login(testUserData); // Отправка тестовых данных в store
        this.$router.push('/profile'); // Перенаправление на страницу профиля
      } catch (error) {
        console.error('Ошибка авторизации:', error);
        alert('Не удалось авторизоваться');
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
}
button:disabled {
  background-color: #cccccc;
}
</style>