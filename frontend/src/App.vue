<template>
  <div id="app" :class="{ 'dark-theme': isDarkTheme }">
    <!-- Навигационная панель -->
    <nav class="navbar">
      <router-link to="/" class="nav-link">Главная</router-link>
      <router-link to="/hackathons" class="nav-link">Хакатоны</router-link>
      <router-link to="/profile" class="nav-link">Профиль</router-link>
      <button v-if="isAuthenticated" @click="logout" class="logout-btn">Выйти</button>
    </nav>
    <!-- Основной контент -->
    <main class="content">
      <router-view />
    </main>
  </div>

</template>

<script>
import { useAuthStore } from './stores/auth';

export default {
  computed: {
    isAuthenticated() {
      const authStore = useAuthStore();
      return !!authStore.token;
    },
    isDarkTheme() {
      return true; // Пока фиксированно темная тема (можно сделать переключение позже)
    },
  },
  methods: {
    logout() {
      const authStore = useAuthStore();
      authStore.logout();
      this.$router.push('/');
    },
  },
};
</script>

<style>
/* Базовые стили для Telegram Mini App */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: #000;
  color: #fff;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.dark-theme {
  background-color: #1C2526;
  color: #fff;
}

/* Навигация */
.navbar {
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  background-color: #212b2c;
  border-bottom: 1px solid #333;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  font-size: 16px;
  padding: 10px;
  transition: color 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #00BFFF;
}

.logout-btn {
  background-color: #ff5555;
  border: none;
  color: #fff;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #ff3333;
}

/* Основной контент */
.content {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}
</style>