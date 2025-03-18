<template>
  <div class="profile-settings">
    <h1>Настройки профиля</h1>
    <form @submit.prevent="saveSettings">
      <div class="form-group">
        <label>Имя</label>
        <input v-model="form.first_name" placeholder="Введите имя" />
      </div>
      <div class="form-group">
        <label>Фамилия</label>
        <input v-model="form.last_name" placeholder="Введите фамилию" />
      </div>
      <div class="form-group">
        <label>Номер телефона</label>
        <input v-model="form.phone_number" placeholder="Введите номер телефона" />
      </div>
      <div class="form-group">
        <label>Email</label>
        <input v-model="form.email" type="email" placeholder="Введите email" />
      </div>
      <div class="form-group">
        <label>Пол</label>
        <select v-model="form.gender">
          <option value="male">Мужской</option>
          <option value="female">Женский</option>
        </select>
      </div>
      <div class="form-group">
        <label>Дата рождения</label>
        <input v-model="form.birth_date" type="date" />
      </div>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <button type="submit" class="action-btn primary">Сохранить</button>
    </form>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth';

export default {
  data() {
    return {
      form: {
        first_name: '',
        last_name: '',
        phone_number: '',
        email: '',
        gender: '',
        birth_date: '',
      },
      errorMessage: '',
    };
  },
  methods: {
    async saveSettings() {
      const authStore = useAuthStore();
      this.errorMessage = '';

      // Добавляем "+" к номеру телефона, если его нет

      // Преобразуем birth_date в формат ISO (YYYY-MM-DD), если заполнено
      if (this.form.birth_date) {
        this.form.birth_date = new Date(this.form.birth_date).toISOString().split('T')[0];
      }

      console.log('Отправляемые данные:', this.form);
      console.log('URL запроса:', `${import.meta.env.VITE_BACKEND_API_URL}/api/users/profile/update/`);

      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_API_URL}/api/users/profile/update/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authStore.token}`,
          },
          body: JSON.stringify(this.form),
        });

        if (!response.ok) {
          const text = await response.text(); // Получаем текст ответа
          try {
            const error = JSON.parse(text); // Пробуем разобрать как JSON
            throw error;
          } catch (e) {
            throw new Error(text || 'Неизвестная ошибка сервера');
          }
        }

        const result = await response.json();
        await authStore.fetchUser(); // Обновляем данные пользователя в сторе
        this.$router.push('/profile');
      } catch (error) {
        console.error('Ошибка обновления профиля:', error);
        this.errorMessage = error.detail || error.message || 'Не удалось обновить профиль';
      }
    },
  },
  async created() {
    const authStore = useAuthStore();
    if (authStore.user) {
      this.form = {
        first_name: authStore.user.first_name || '',
        last_name: authStore.user.last_name || '',
        phone_number: authStore.user.phone_number || '',
        email: authStore.user.email || '',
        gender: authStore.user.gender || '',
        birth_date: authStore.user.birth_date ? authStore.user.birth_date.split('T')[0] : '',
      };
    }
  },
};
</script>

<style scoped>
.profile-settings {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background: rgba(42, 52, 53, 0.7);
  border-radius: 20px;
  color: #fff;
}

h1 {
  font-size: 24px;
  color: #00BFFF;
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #ccc;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid rgba(0, 191, 255, 0.2);
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #00BFFF;
  box-shadow: 0 0 5px rgba(0, 191, 255, 0.5);
}

.action-btn {
  padding: 12px 24px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
}

.action-btn.primary {
  background: linear-gradient(45deg, #00BFFF, #0099cc);
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 191, 255, 0.2);
}

.error {
  color: #ff5555;
  background: rgba(255, 85, 85, 0.1);
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
  text-align: center;
}

@media (max-width: 768px) {
  .profile-settings {
    padding: 15px;
  }

  h1 {
    font-size: 20px;
  }

  .form-group input,
  .form-group select {
    font-size: 14px;
  }
}
</style>