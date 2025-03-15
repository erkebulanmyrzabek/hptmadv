<template>
    <div class="settings-page">
      <h1>Настройки профиля</h1>
      <form @submit.prevent="saveSettings" class="settings-form">
        <div class="form-group">
          <label>Имя:</label>
          <input v-model="form.first_name" type="text" placeholder="Введите имя" />
        </div>
        <div class="form-group">
          <label>Фамилия:</label>
          <input v-model="form.last_name" type="text" placeholder="Введите фамилию" />
        </div>
        <div class="form-group">
          <label>Телефон:</label>
          <input v-model="form.phone_number" type="tel" placeholder="Введите номер телефона" />
        </div>
        <div class="form-group">
          <label>Email:</label>
          <input v-model="form.email" type="email" placeholder="Введите email" />
        </div>
        <div class="form-group">
          <label>Пол:</label>
          <select v-model="form.gender">
            <option value="">Не указано</option>
            <option value="male">Мужской</option>
            <option value="female">Женский</option>
          </select>
        </div>
        <div class="form-group">
          <label>Дата рождения:</label>
          <input v-model="form.birth_date" type="date" />
        </div>
        <div class="form-group">
          <label>Город:</label>
          <select v-model="form.city">
            <option value="">Не указано</option>
            <option value="Almaty">Алматы</option>
            <option value="Nur-Sultan">Нур-Султан</option>
            <option value="Shymkent">Шымкент</option>
            <option value="Taraz">Тараз</option>
            <option value="Aktobe">Актобе</option>
            <option value="Kyzylorda">Кызылорда</option>
            <option value="Kostanay">Костанай</option>
            <option value="Pavlodar">Павлодар</option>
            <option value="Oral">Орал</option>
            <option value="Atyrau">Атырау</option>
            <option value="Zhambyl">Жамбыл</option>
            <option value="Karagandy">Караганда</option>
            <option value="Kokshetau">Кокшетау</option>
            <option value="Mangystau">Мангистау</option>
            <option value="Petropavl">Петропавловск</option>
            <option value="Taldykorgan">Талдыкорган</option>
            <option value="Turkistan">Туркестан</option>
            <option value="Ust-Kamenogorsk">Усть-Каменогорск</option>
          </select>
        </div>
        <div class="form-group">
          <label>Страна:</label>
          <input v-model="form.country" type="text" placeholder="Введите страну" />
        </div>
        <div class="form-group">
          <label>Адрес:</label>
          <input v-model="form.address" type="text" placeholder="Введите адрес" />
        </div>
        <div class="form-group">
          <label>О себе:</label>
          <textarea v-model="form.bio" placeholder="Краткое описание"></textarea>
        </div>
        <button type="submit" class="save-btn">Сохранить</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
      </form>
    </div>
  </template>
  
  <script>
  import { useAuthStore } from '../stores/auth';
  import axios from 'axios';

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
          city: '',
          country: '',
          address: '',
          bio: '',
        },
        errorMessage: '',
        successMessage: '',
      };
    },
    computed: {
      user() {
        const authStore = useAuthStore();
        return authStore.user;
      },
    },
    created() {
      this.form = {
        first_name: this.user.first_name || '',
        last_name: this.user.last_name || '',
        phone_number: this.user.phone_number || '',
        email: this.user.email || '',
        gender: this.user.gender || '',
        birth_date: this.user.birth_date ? this.formatDateToInput(this.user.birth_date) : '',
        city: this.user.city || '',
        country: this.user.country || '',
        address: this.user.address || '',
        bio: this.user.bio || '',
      };
    },
    methods: {
      formatDateToInput(date) {
        if (!date) return '';
        return new Date(date).toISOString().split('T')[0]; // Гарантирует формат YYYY-MM-DD
      },
      async saveSettings() {
        try {
          const authStore = useAuthStore();
          // Преобразуем birth_date в правильный формат, если он есть
          const payload = { ...this.form };
          if (payload.birth_date) {
            payload.birth_date = this.formatDateToInput(payload.birth_date); // Убедимся, что дата в формате YYYY-MM-DD
          }
          console.log("Отправляемые данные:", payload); // Отладка
          const response = await axios.put(
            'http://localhost:8000/api/users/profile/update/',
            payload,
            { headers: { Authorization: `Bearer ${authStore.token}` } }
          );
          await authStore.fetchUser(); // Синхронизация данных
          this.successMessage = response.data.detail;
          this.errorMessage = '';
          setTimeout(() => this.$router.push('/profile'), 2000);
        } catch (error) {
          this.errorMessage = error.response?.data.detail || 'Ошибка при сохранении';
          this.successMessage = '';
        }
      },
    },
  };


  </script>
  
  <style scoped>
  .settings-page {
    padding: 20px;
    max-width: 600px;
    margin: 0 auto;
  }
  
  h1 {
    font-size: 24px;
    color: #00BFFF;
    margin-bottom: 20px;
  }
  
  .settings-form {
    background-color: #2A3435;
    padding: 20px;
    border-radius: 10px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    font-size: 14px;
    color: #ccc;
    margin-bottom: 5px;
  }
  
  input,
  select,
  textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #444;
    border-radius: 5px;
    background-color: #333;
    color: #fff;
  }
  
  textarea {
    height: 100px;
    resize: vertical;
  }
  
  .save-btn {
    display: block;
    width: 100%;
    padding: 12px;
    background-color: #00BFFF;
    color: #fff;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .save-btn:hover {
    background-color: #009ACD;
  }
  
  .error {
    color: #FF5555;
    margin-top: 10px;
  }
  
  .success {
    color: #00FF00;
    margin-top: 10px;
  }

 
  </style>