<template>
    <div class="hackathon-detail">
      <div v-if="hackathon" class="hackathon-header">
        <img
          :src="hackathon.banner_image || hackathon.preview_image || 'https://via.placeholder.com/1200x400'"
          alt="Hackathon Banner"
          class="banner-image"
        />
        <h1>{{ hackathon.title }}</h1>
        <div class="info">
          <span class="status" :class="hackathon.status">{{ hackathon.status }}</span>
          <span class="type">{{ hackathon.type }}</span>
          <span>Участники: {{ hackathon.participants_count }}/{{ hackathon.max_participants || '∞' }}</span>
        </div>
      </div>
  
      <div v-if="hackathon" class="hackathon-content">
        <!-- Описание -->
        <section class="section">
          <h2>Описание</h2>
          <p>{{ hackathon.full_description || hackathon.short_description || 'Описание отсутствует' }}</p>
        </section>
  
        <!-- Организатор -->
        <section class="section">
          <h2>Организатор</h2>
          <div class="organization">
            <img
              :src="hackathon.organization.logo || 'https://via.placeholder.com/50'"
              alt="Organization Logo"
              class="org-logo"
            />
            <div>
              <p><strong>{{ hackathon.organization.name }}</strong></p>
              <p>{{ hackathon.organization.description }}</p>
              <div class="org-links">
                <a v-if="hackathon.organization.website" :href="hackathon.organization.website" target="_blank">Сайт</a>
                <a v-if="hackathon.organization.telegram" :href="hackathon.organization.telegram" target="_blank">Telegram</a>
                <a v-if="hackathon.organization.instagram" :href="hackathon.organization.instagram" target="_blank">Instagram</a>
              </div>
            </div>
          </div>
        </section>
  
        <!-- Даты -->
        <section class="section">
          <h2>Даты</h2>
          <p><strong>Регистрация:</strong> {{ formatDate(hackathon.registration_start_date) }} - {{ formatDate(hackathon.registration_end_date) }}</p>
          <p><strong>Хакатон:</strong> {{ formatDate(hackathon.start_date) }} - {{ formatDate(hackathon.end_date) }}</p>
        </section>
  
        <!-- Место -->
        <section v-if="hackathon.type !== 'online'" class="section">
          <h2>Место проведения</h2>
          <p>{{ hackathon.location || 'Не указано' }}</p>
          <p>{{ hackathon.address || 'Адрес не указан' }}</p>
        </section>
  
        <!-- Призы -->
        <section class="section">
          <h2>Призы</h2>
          <p><strong>Общий призовой фонд:</strong> {{ hackathon.total_prize_amount }}₸</p>
          <p><strong>Призовых мест:</strong> {{ hackathon.total_prize_places }}</p>
          <div class="prizes">
            <div v-for="prize in hackathon.hackathon_prizes" :key="prize.place" class="prize-item">
              <span>{{ prize.place }} место:</span>
              <span>{{ prize.prize_amount || 0 }}₸, {{ prize.xp_reward }} XP</span>
              <span>(для {{ prize.number_of_winners }} победителей)</span>
            </div>
          </div>
        </section>
  
        <!-- FAQ -->
        <section v-if="hackathon.faq" class="section">
          <h2>FAQ</h2>
          <p>{{ hackathon.faq }}</p>
        </section>
  
        <!-- Правила -->
        <section v-if="hackathon.rules" class="section">
          <h2>Правила</h2>
          <p>{{ hackathon.rules }}</p>
        </section>
  
        <!-- Регистрация -->
        <section class="section">
          <h2>Регистрация</h2>
          <div v-if="!isAuthenticated">
            <p>Пожалуйста, авторизуйтесь, чтобы зарегистрироваться.</p>
            <router-link to="/" class="action-btn">Войти</router-link>
          </div>
          <div v-else-if="hackathon.is_participant">
            <p class="success">Вы уже зарегистрированы на этот хакатон!</p>
          </div>
          <div v-else-if="hackathon.status !== 'registration'" class="error">
            <p>Регистрация на этот хакатон сейчас недоступна.</p>
          </div>
          <div v-else-if="missingRequiredFields" class="error">
            <p>Заполните недостающие данные профиля.</p>
            <router-link to="/profile/settings" class="action-btn">Перейти к настройкам</router-link>
          </div>
          <div v-else>
            <button @click="showRegistrationForm = true" class="action-btn">Регистрация</button>
            <div v-if="showRegistrationForm" class="registration-form">
              <div v-if="hackathon.type === 'team' || hackathon.type === 'hybrid'" class="team-section">
                <h3>Создать команду</h3>
                <input
                  v-model="teamName"
                  type="text"
                  placeholder="Название команды"
                  class="team-input"
                />
                <button @click="createTeam" class="action-btn">Создать команду</button>
                <p v-if="teamCreated" class="success">
                  Команда создана! Код для присоединения: {{ teamJoinCode }}
                </p>
                <h3>Присоединиться к команде</h3>
                <input
                  v-model="joinCode"
                  type="text"
                  placeholder="Введите код команды"
                  class="team-input"
                />
                <button @click="joinTeam" class="action-btn">Присоединиться</button>
              </div>
              <div v-if="hackathon.type === 'solo' || hackathon.type === 'hybrid'">
                <button @click="registerSolo" class="action-btn">Зарегистрироваться индивидуально</button>
              </div>
              <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
            </div>
          </div>
        </section>
      </div>
  
      <p v-else>Загрузка...</p>
    </div>
  </template>
  
  <script>
  import { useHackathonStore } from '../stores/hackathon';
  import { useAuthStore } from '../stores/auth';
  
  export default {
    data() {
      return {
        showRegistrationForm: false,
        teamName: '',
        joinCode: '',
        teamCreated: false,
        teamJoinCode: '',
        errorMessage: '',
      };
    },
    computed: {
      hackathon() {
        const hackathonStore = useHackathonStore();
        return hackathonStore.currentHackathon;
      },
      isAuthenticated() {
        const authStore = useAuthStore();
        return !!authStore.token;
      },
      user() {
        const authStore = useAuthStore();
        return authStore.user;
      },
      missingRequiredFields() {
        return !this.user.first_name || !this.user.phone_number || !this.user.birth_date;
      },
    },
    async created() {
      const hackathonStore = useHackathonStore();
      await hackathonStore.fetchHackathonDetail(this.$route.params.id);
    },
    methods: {
      formatDate(date) {
        if (!date) return 'Не указано';
        return new Date(date).toLocaleDateString('ru-RU', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
        });
      },
      async registerSolo() {
        try {
          this.errorMessage = '';
          const hackathonStore = useHackathonStore();
          const response = await hackathonStore.registerForHackathon(this.$route.params.id);
          alert(response.detail);
          this.showRegistrationForm = false;
        } catch (error) {
          this.errorMessage = error.detail || 'Ошибка при регистрации';
        }
      },
      async createTeam() {
        try {
          this.errorMessage = '';
          if (!this.teamName) {
            this.errorMessage = 'Укажите название команды';
            return;
          }
          const hackathonStore = useHackathonStore();
          const response = await hackathonStore.createTeam(this.$route.params.id, this.teamName);
          this.teamCreated = true;
          this.teamJoinCode = response.team.join_code;
          alert(response.detail);
        } catch (error) {
          this.errorMessage = error.detail || 'Ошибка при создании команды';
        }
      },
      async joinTeam() {
        try {
          this.errorMessage = '';
          if (!this.joinCode) {
            this.errorMessage = 'Укажите код команды';
            return;
          }
          const hackathonStore = useHackathonStore();
          const response = await hackathonStore.joinTeam(this.$route.params.id, this.joinCode);
          alert(response.detail);
          this.showRegistrationForm = false;
        } catch (error) {
          this.errorMessage = error.detail || 'Ошибка при присоединении к команде';
        }
      },
    },
  };
  </script>
  
  
  <style scoped>
  .hackathon-detail {
    padding: 20px;
  }
  
  .hackathon-header {
    text-align: center;
    margin-bottom: 30px;
  }
  
  .banner-image {
    width: 100%;
    max-height: 400px;
    object-fit: cover;
    border-radius: 10px;
  }
  
  h1 {
    font-size: 28px;
    margin: 20px 0;
    color: #00BFFF;
  }
  
  .info {
    display: flex;
    justify-content: center;
    gap: 15px;
    font-size: 14px;
    color: #ccc;
  }
  
  .status {
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 12px;
    text-transform: capitalize;
  }
  
  .status.anounce {
    background-color: #FFD700;
    color: #000;
  }
  
  .status.registration {
    background-color: #00FF00;
    color: #000;
  }
  
  .status.in_progress {
    background-color: #1E90FF;
    color: #fff;
  }
  
  .status.finished {
    background-color: #FF4500;
    color: #fff;
  }
  
  .status.archived {
    background-color: #808080;
    color: #fff;
  }
  
  .type {
    font-size: 14px;
  }
  
  .hackathon-content {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .section {
    margin-bottom: 30px;
  }
  
  h2 {
    font-size: 20px;
    color: #00BFFF;
    margin-bottom: 10px;
  }
  
  p {
    font-size: 16px;
    color: #ccc;
  }
  
  .organization {
    display: flex;
    align-items: center;
    gap: 15px;
  }
  
  .org-logo {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
  }
  
  .org-links {
    display: flex;
    gap: 10px;
  }
  
  .org-links a {
    color: #00BFFF;
    text-decoration: none;
  }
  
  .org-links a:hover {
    text-decoration: underline;
  }
  
  .prizes {
    margin-top: 10px;
  }
  
  .prize-item {
    display: flex;
    gap: 10px;
    font-size: 14px;
    color: #ccc;
    margin-bottom: 5px;
  }
  
  .team-section {
    margin-top: 20px;
  }
  
  .team-input {
    width: 100%;
    max-width: 300px;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #444;
    border-radius: 5px;
    background-color: #2A3435;
    color: #fff;
  }
  
  .action-btn {
    display: inline-block;
    padding: 12px 24px;
    background-color: #00BFFF;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .action-btn:hover {
    background-color: #009ACD;
  }
  
  .success {
    color: #00FF00;
    margin-top: 10px;
  }
  
  .error {
    color: #FF5555;
    margin-top: 10px;
  }
  </style>