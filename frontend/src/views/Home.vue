<template>
  <div class="home">
    <h1>Добро пожаловать в HackPlatform!</h1>
    <p class="welcome-text">
      Присоединяйтесь к лучшим хакатонам, соревнуйтесь с другими участниками и выигрывайте призы!
    </p>
    <div v-if="!isAuthenticated" class="login-section">
      <button @click="loginWithTestUser" :disabled="loading" class="action-btn login-btn">
        Войти как тестовый пользователь
      </button>
      <button @click="loginWithRealUser" :disabled="loading" class="action-btn login-btn">
        Войти через Telegram
      </button>
      <p v-if="loading">Авторизация...</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
    <div v-else class="action-buttons">
      <router-link to="/hackathons" class="action-btn">Посмотреть хакатоны</router-link>
      <router-link to="/profile" class="action-btn">Мой профиль</router-link>
    </div>
  </div>
</template>
<script>
import { useAuthStore } from '../stores/auth';
import { useMiniApp } from 'vue-tg';

const miniApp = useMiniApp();

export default {
  computed: {
    isAuthenticated() {
      const authStore = useAuthStore();
      return !!authStore.token;
    },
  },
  data() {
    return {
      loading: false,
      errorMessage: '',
    };
  },
  methods: {
    async login(initData) {
      this.loading = true;
      this.errorMessage = '';
      const authStore = useAuthStore();
      try {
        const initDataObj = Object.fromEntries(new URLSearchParams(initData));
        console.log('initDataObj:', initDataObj);

        if (!initDataObj.user) {
          throw new Error('Поле user отсутствует в initData');
        }

        const userData = JSON.parse(initDataObj.user);
        console.log('userData:', userData);

        if (!userData.id) {
          throw new Error('Telegram ID отсутствует в userData');
        }

        const dataToSend = {
          id: userData.id,
          first_name: userData.first_name,
          last_name: userData.last_name,
          username: userData.username,
          hash: initDataObj.hash,
          auth_date: initDataObj.auth_date,
        };
        console.log('dataToSend:', dataToSend);

        await authStore.login(dataToSend);
        this.$router.push('/profile');
      } catch (error) {
        console.error('Ошибка авторизации:', error);
        this.errorMessage = 'Не удалось авторизоваться: ' + error.message;
      } finally {
        this.loading = false;
      }
    },

    async loginWithTestUser() {
      const testUserInitData = new URLSearchParams({
        user: JSON.stringify({
          id: 1234567890,
          first_name: 'Test',
          last_name: 'User',
          username: 'testuser',
          language_code: 'en',
          allows_write_to_pm: true,
          photo_url: 'https://t.me/i/userpic/320/testuser.jpg',
        }),
        chat_instance: '-1234567890123456789',
        chat_type: 'sender',
        auth_date: Math.floor(Date.now() / 1000).toString(),
        hash: 'mock_hash_1234567890',
      }).toString();

      console.log('testUserInitData:', testUserInitData);
      await this.login(testUserInitData);
    },

    async loginWithRealUser() {
      if (!window.Telegram || !window.Telegram.WebApp) {
        throw new Error('Telegram WebApp не инициализирован');
      }

      const initData = miniApp.initData || window.Telegram.WebApp.initData;
      console.log('initData:', initData);

      if (!initData) {
        throw new Error('Telegram initData не доступен');
      }

      await this.login(initData);
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

.login-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: center;
  margin-bottom: 20px;
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
  transition: background-color 0.3s, transform 0.2s;
  border: none;
  cursor: pointer;
}

.action-btn:hover {
  background-color: #009ACD;
  transform: translateY(-2px);
}

.action-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
  transform: none;
}

.login-btn {
  width: 250px;
}

.error-message {
  color: #ff5555;
  background: rgba(255, 85, 85, 0.1);
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
  max-width: 300px;
}

p {
  color: #666;
}

@media (max-width: 768px) {
  h1 {
    font-size: 24px;
  }

  .welcome-text {
    font-size: 14px;
  }

  .action-buttons {
    flex-direction: column;
    gap: 15px;
  }

  .action-btn {
    width: 100%;
    max-width: 250px;
  }
}
</style>