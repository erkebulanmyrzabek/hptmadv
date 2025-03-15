<template>
  <div class="home">
    <h1>Добро пожаловать в HackPlatform!</h1>
    <p class="welcome-text">
      Присоединяйтесь к лучшим хакатонам, соревнуйтесь с другими участниками и выигрывайте призы!
    </p>
    <login v-if="!isAuthenticated" />
    <div v-else class="action-buttons">
      <router-link to="/hackathons" class="action-btn">Посмотреть хакатоны</router-link>
      <router-link to="/profile" class="action-btn">Мой профиль</router-link>
    </div>
  </div>
</template>

<script>
import Login from '../components/Login.vue';
import { useAuthStore } from '../stores/auth';

export default {
  components: { Login },
  computed: {
    isAuthenticated() {
      const authStore = useAuthStore();
      return !!authStore.token;
    },
  },
};
</script>

<style scoped>
.home {
  text-align: center;
  padding: 40px 20px;
}

h1 {
  font-size: 28px;
  margin-bottom: 20px;
  color: #00BFFF;
}

.welcome-text {
  font-size: 16px;
  margin-bottom: 30px;
  color: #ccc;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.action-btn {
  display: inline-block;
  padding: 12px 24px;
  background-color: #00BFFF;
  color: #fff;
  text-decoration: none;
  border-radius: 8px;
  font-size: 16px;
  transition: background-color 0.3s;
}

.action-btn:hover {
  background-color: #009ACD;
}
</style>