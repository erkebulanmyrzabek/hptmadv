<template>
  <div class="profile-page">
    <div v-if="user" class="profile-card">
      <div class="profile-header">
        <img
          :src="user.avatar"
          alt="Avatar"
          class="avatar"
        />
        <div class="profile-title">
          <h1>{{ user.first_name || user.username }} {{ user.last_name }}</h1>
          <div class="level-badge">
            <span class="level-icon">👑</span>
            <span>Уровень {{ user.level }}</span>
          </div>
        </div>
      </div>

      <div class="profile-stats">
        <div class="stat-card">
          <span class="stat-icon">⭐️</span>
          <span class="stat-value">{{ user.xp }}</span>
          <span class="stat-label">XP</span>
        </div>
        <div class="stat-card">
          <span class="stat-icon">💎</span>
          <span class="stat-value">{{ user.balance }}</span>
          <span class="stat-label">Кристаллов</span>
        </div>
      </div>

      <div class="profile-info">
        <div class="info-section">
          <h2>📱 Контактная информация</h2>
          <p><span class="info-icon">🆔</span> <strong>Telegram:</strong> {{ user.telegram_id }}</p>
          <p><span class="info-icon">📧</span> <strong>Email:</strong> {{ user.email || 'Не указано' }}</p>
          <p><span class="info-icon">📞</span> <strong>Телефон:</strong> {{ user.phone_number || 'Не указан' }}</p>
        </div>

        <div class="info-section">
          <h2>👤 Личная информация</h2>
          <p><span class="info-icon">🌆</span> <strong>Город:</strong> {{ user.city || 'Не указан' }}</p>
          <p><span class="info-icon">🎂</span> <strong>Дата рождения:</strong> {{ formatDate(user.birth_date) }}</p>
        </div>

        <router-link to="/profile/settings" class="edit-btn">
          ⚙️ Настройки профиля
        </router-link>
      </div>
    </div>
    <div v-else class="loading">
      <p>🔄 Загрузка...</p>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const { user } = storeToRefs(authStore);

    if (!authStore.user && authStore.token) {
      authStore.fetchUser();
    }
    if (!authStore.token) {
      router.push('/');
    }

    const formatDate = (date) => {
      if (!date) return 'Не указано';
      return new Date(date).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
      });
    };

    return {
      user,
      formatDate
    };
  }
};
</script>

<style scoped>
.profile-page {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.profile-card {
  background: linear-gradient(145deg, #2A3435, #1a2223);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 30px;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid rgba(0, 191, 255, 0.2);
}

.avatar {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #00BFFF;
  box-shadow: 0 0 20px rgba(0, 191, 255, 0.3);
}

.profile-title {
  flex: 1;
}

h1 {
  font-size: 32px;
  color: #00BFFF;
  margin-bottom: 10px;
  text-shadow: 0 0 10px rgba(0, 191, 255, 0.3);
}

.level-badge {
  display: inline-flex;
  align-items: center;
  background: rgba(0, 191, 255, 0.1);
  padding: 8px 15px;
  border-radius: 20px;
  color: #00BFFF;
}

.level-icon {
  font-size: 24px;
  margin-right: 8px;
}

.profile-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  flex: 1;
  background: rgba(0, 191, 255, 0.1);
  padding: 20px;
  border-radius: 15px;
  text-align: center;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  font-size: 32px;
  display: block;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  color: #00BFFF;
  font-weight: bold;
  display: block;
}

.stat-label {
  color: #ccc;
  font-size: 14px;
}

.info-section {
  background: rgba(42, 52, 53, 0.7);
  padding: 20px;
  border-radius: 15px;
  margin-bottom: 20px;
}

.info-section h2 {
  color: #00BFFF;
  font-size: 20px;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.info-icon {
  margin-right: 10px;
  font-size: 18px;
}

p {
  font-size: 16px;
  color: #ccc;
  margin: 12px 0;
  display: flex;
  align-items: center;
}

.edit-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 25px;
  background: linear-gradient(45deg, #00BFFF, #0099cc);
  color: #fff;
  text-decoration: none;
  border-radius: 25px;
  font-weight: 500;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  margin-top: 20px;
}

.edit-btn:hover {
  background: linear-gradient(45deg, #0099cc, #00BFFF);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 191, 255, 0.3);
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 20px;
  color: #00BFFF;
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .profile-stats {
    flex-direction: column;
  }

  .avatar {
    width: 150px;
    height: 150px;
  }
}
</style>