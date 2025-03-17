<script>
import { useAuthStore } from '../stores/auth'; // Импорт Pinia store
import { useMiniApp } from 'vue-tg';

const miniApp = useMiniApp();

export default {
  data() {
    return {
      loading: false, // Состояние загрузки
    };
  },
  methods: {
    async login(initData) {
      this.loading = true;
      const authStore = useAuthStore();
      try {
        // Парсим initData в объект
        const initDataObj = Object.fromEntries(new URLSearchParams(initData));
        console.log('initDataObj:', initDataObj);

        // Извлекаем поле user и парсим его из JSON
        if (!initDataObj.user) {
          throw new Error('Поле user отсутствует в initData');
        }

        const userData = JSON.parse(initDataObj.user);
        console.log('userData:', userData);

        // Проверяем наличие id в userData
        if (!userData.id) {
          throw new Error('Telegram ID отсутствует в userData');
        }

        // Формируем данные для отправки на сервер
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
        alert('Не удалось авторизоваться: ' + error.message);
      } finally {
        this.loading = false;
      }
    },

    async loginWithTestUser() {
      // Тестовый пользователь, имитирующий структуру Telegram initData
      const testUserInitData = new URLSearchParams({
        user: JSON.stringify({
          id: 1234567890, // Тестовый Telegram ID
          first_name: 'Test',
          last_name: 'User',
          username: 'testuser',
          language_code: 'en',
          allows_write_to_pm: true,
          photo_url: 'https://t.me/i/userpic/320/testuser.jpg',
        }),
        chat_instance: '-1234567890123456789',
        chat_type: 'sender',
        auth_date: Math.floor(Date.now() / 1000).toString(), // Текущая дата в формате Unix timestamp
        hash: 'mock_hash_1234567890', // Моковый hash для теста
      }).toString();

      console.log('testUserInitData:', testUserInitData);
      await this.login(testUserInitData);
    },

    async loginWithRealUser() {
      // Проверка Telegram WebApp
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
div {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #0056b3;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

p {
  color: #666;
}
</style>