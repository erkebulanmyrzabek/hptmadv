<template>
  <div class="profile-page">
    <div v-if="user" class="profile-card">
      <img
        :src="user.avatar || 'https://via.placeholder.com/150'"
        alt="Avatar"
        class="avatar"
      />
      <div class="profile-info">
        <h1>{{ user.first_name || user.username }} {{ user.last_name }}</h1>
        <p><strong>Telegram ID:</strong> {{ user.telegram_id }}</p>
        <p><strong>Email:</strong> {{ user.email || 'Не указано' }}</p>
        <p><strong>Телефон:</strong> {{ user.phone_number || 'Не указан' }}</p>
        <p><strong>XP:</strong> {{ user.xp }}</p>
        <p><strong>Уровень:</strong> {{ user.level }}</p>
        <p><strong>Баланс:</strong> {{ user.balance }}₸</p>
        <p><strong>Город:</strong> {{ user.city || 'Не указан' }}</p>
        <p><strong>Дата рождения:</strong> {{ formatDate(user.birth_date) }}</p>
        <router-link to="/profile/settings" class="edit-btn">Настройки</router-link>
      </div>
    </div>
    <p v-else>Загрузка...</p>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth';

export default {
  computed: {
    user() {
      const authStore = useAuthStore();
      return authStore.user;
    },
  },
  methods: {
    formatDate(date) {
      if (!date) return 'Не указано';
      return new Date(date).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
      });
    },
  },
  async created() {
    const authStore = useAuthStore();
    if (!authStore.user && authStore.token) {
      await authStore.fetchUser();
    }
    if (!authStore.token) {
      this.$router.push('/');
    }
  },
};
</script>

<style scoped>
.profile-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.profile-card {
  background-color: #2A3435;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-info {
  flex: 1;
}

h1 {
  font-size: 24px;
  color: #00BFFF;
  margin-bottom: 10px;
}

p {
  font-size: 16px;
  color: #ccc;
  margin: 5px 0;
}

.edit-btn {
  display: inline-block;
  padding: 10px 20px;
  background-color: #00BFFF;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
  margin-top: 15px;
}

.edit-btn:hover {
  background-color: #009ACD;
}
</style>