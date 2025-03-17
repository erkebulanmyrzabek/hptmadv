<script>
import { useHackathonStore } from '../stores/hackathon';
import { useAuthStore } from '../stores/auth';

export default {
  data() {
    return {
      showRegistrationModal: false,
      registrationStep: '',
      teamName: '',
      joinCode: '',
      teamCreated: false,
      teamJoinCode: '',
      errorMessage: '',
      currentTab: 'about',
      tabs: [
        { id: 'about', name: 'О хакатоне', icon: '📝' },
        { id: 'prizes', name: 'Призы', icon: '🏆' },
        { id: 'organizer', name: 'Организатор', icon: '🏢' },
        { id: 'rules', name: 'FAQ и Правила', icon: '📜' },
        { id: 'registration', name: 'Регистрация', icon: '✍️' }
      ]
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
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return 'Не указано';
      return new Date(date).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    getStatusText(status) {
      const statusMap = {
        'archived': 'Архив',
        'anounce': 'Анонс',
        'registration': 'Регистрация',
        'in_progress': 'В процессе',
        'finished': 'Завершен'
      };
      return statusMap[status] || status;
    },
    getStatusIcon(status) {
      const iconMap = {
        'archived': '📦',
        'anounce': '📢',
        'registration': '✍️',
        'in_progress': '🔥',
        'finished': '🏁'
      };
      return iconMap[status] || '❓';
    },
    getFormatText(type) {
      const formatMap = {
        'online': 'Онлайн 💻',
        'offline': 'Офлайн 🏢',
        'hybrid': 'Гибрид 🔄'
      };
      return formatMap[type] || type;
    },
    getPrizeMedal(place) {
      const medals = {
        1: '🥇',
        2: '🥈',
        3: '🥉'
      };
      return medals[place] || '🏅';
    },
    formatFAQ(faq) {
      return faq.split('\n').map(line => `<p>${line}</p>`).join('');
    },
    formatRules(rules) {
      return rules.split('\n').map(line => `<p>${line}</p>`).join('');
    },
    // Методы для управления модальным окном
    openRegistrationModal() {
      this.showRegistrationModal = true;
      this.registrationStep = '';
    },
    closeRegistrationModal() {
      this.showRegistrationModal = false;
      this.registrationStep = '';
      this.teamName = '';
      this.joinCode = '';
      this.teamCreated = false;
      this.teamJoinCode = '';
    },
    registerAsSolo() {
      this.registerSolo();
      this.closeRegistrationModal();
    },
    registerAsTeam() {
      this.registrationStep = 'create-team';
    },
    joinTeamModal() {
      this.registrationStep = 'join-team';
    },
    async registerSolo() {
      try {
        this.errorMessage = '';
        const hackathonStore = useHackathonStore();
        const response = await hackathonStore.registerForHackathon(this.$route.params.id);
        this.showSuccessMessage(response.detail);
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
        this.showSuccessMessage(response.detail);
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
        this.showSuccessMessage(response.detail);
        this.closeRegistrationModal();
      } catch (error) {
        this.errorMessage = error.detail || 'Ошибка при присоединении к команде';
      }
    },
    copyCode() {
      if (!this.teamCreated) return;
      navigator.clipboard.writeText(this.teamJoinCode);
      this.showSuccessMessage('Код скопирован!');
    },
    showSuccessMessage(message) {
      alert(message);
    }
  },
  async created() {
    const hackathonStore = useHackathonStore();
    await hackathonStore.fetchHackathonDetail(this.$route.params.id);
  }
};
</script>

<style scoped>
.hackathon-detail {
  min-height: 100vh;
  background: #1a1a1a;
}

.banner-container {
  position: relative;
  height: 400px;
  overflow: hidden;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.banner-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  color: white;
}

.banner-overlay h1 {
  font-size: 42px;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.header-info {
  display: flex;
  gap: 20px;
  align-items: center;
}

.status-badge, .type-badge, .participants-badge {
  padding: 8px 16px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  backdrop-filter: blur(5px);
}

.status-badge {
  background: rgba(0, 191, 255, 0.2);
}

.status-badge.registration {
  background: rgba(46, 213, 115, 0.8);
}

.status-badge.in_progress {
  background: rgba(255, 71, 87, 0.8);
}

.hackathon-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.tab-btn {
  padding: 12px 24px;
  border: none;
  background: rgba(0, 191, 255, 0.1);
  color: #ccc;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}

.tab-btn:hover {
  background: rgba(0, 191, 255, 0.2);
  color: #fff;
}

.tab-btn.active {
  background: #00BFFF;
  color: white;
}

.tab-icon {
  font-size: 20px;
}

.section {
  background: rgba(42, 52, 53, 0.7);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
}

.section h2 {
  font-size: 24px;
  color: #00BFFF;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Timeline стили */
.timeline {
  position: relative;
  padding: 20px 0;
}

.timeline-item {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.timeline-icon {
  width: 40px;
  height: 40px;
  background: rgba(0, 191, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.timeline-content h3 {
  color: #00BFFF;
  margin-bottom: 5px;
}

/* Призы стили */
.prizes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.prize-card {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 15px;
  padding: 20px;
  text-align: center;
  transition: transform 0.3s ease;
}

.prize-card:hover {
  transform: translateY(-5px);
}

.prize-medal {
  font-size: 40px;
  margin-bottom: 15px;
}

.prize-value {
  font-size: 24px;
  color: #00BFFF;
  margin: 10px 0;
}

.xp-value {
  color: #FFD700;
}

/* Организатор стили */
.organizer-card {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.org-logo {
  width: 100px;
  height: 100px;
  border-radius: 15px;
  object-fit: cover;
}

.org-links {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.org-link {
  padding: 8px 16px;
  background: rgba(0, 191, 255, 0.1);
  border-radius: 20px;
  color: #00BFFF;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.org-link:hover {
  background: rgba(0, 191, 255, 0.2);
  transform: translateY(-2px);
}

/* Стили для модального окна (взято из второго кода) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

.modal-content {
  background: rgba(42, 52, 53, 0.7); /* Адаптировано под стиль первого кода */
  border-radius: 15px;
  padding: 24px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.3s ease;
  color: #fff;
}

.modal-content h2 {
  margin: 0 0 24px;
  color: #00BFFF;
  font-size: 24px;
}

.registration-options {
  display: grid;
  gap: 16px;
}

.option-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(0, 191, 255, 0.1);
  border: none;
  border-radius: 10px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option-btn:hover {
  background: rgba(0, 191, 255, 0.2);
  transform: translateY(-2px);
}

.option-btn svg {
  width: 24px;
  height: 24px;
}

.team-code-input,
.create-team-form {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.team-code-input label,
.create-team-form label {
  color: #ccc;
  font-size: 14px;
}

.team-code-input input,
.create-team-form input {
  padding: 12px;
  border: 1px solid rgba(0, 191, 255, 0.2);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  font-size: 16px;
}

.team-code-input input:focus,
.create-team-form input:focus {
  outline: none;
  border-color: #00BFFF;
}

.team-code {
  margin-top: 10px;
}

.code-display {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: rgba(0, 191, 255, 0.1);
  border-radius: 10px;
  font-family: monospace;
  font-size: 16px;
  color: #00BFFF;
}

.copy-btn {
  padding: 4px;
  background: transparent;
  border: none;
  color: #ccc;
  cursor: pointer;
  transition: color 0.2s ease;
}

.copy-btn:hover {
  color: #00BFFF;
}

.copy-btn:disabled {
  color: #666;
  cursor: not-allowed;
}

.copy-btn svg {
  width: 20px;
  height: 20px;
}

.submit-btn {
  margin-top: 12px;
  padding: 12px 24px;
  background: linear-gradient(45deg, #00BFFF, #0099cc);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
}

.submit-btn:hover {
  background: linear-gradient(45deg, #0099cc, #007acc);
}

/* Стили для сообщений */
.message-card {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 15px;
  padding: 25px;
  text-align: center;
  margin-bottom: 20px;
}

.message-icon {
  font-size: 40px;
  margin-bottom: 15px;
  display: block;
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
}

.action-btn.primary {
  background: linear-gradient(45deg, #00BFFF, #0099cc);
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 191, 255, 0.2);
}

.full-width {
  width: 100%;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: #ccc;
}

.loader {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(0, 191, 255, 0.1);
  border-top-color: #00BFFF;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .banner-container {
    height: 300px;
  }
  
  .banner-overlay {
    padding: 20px;
  }
  
  .banner-overlay h1 {
    font-size: 28px;
  }
  
  .header-info {
    flex-direction: column;
    gap: 10px;
  }
  
  .tabs {
    flex-wrap: nowrap;
    overflow-x: auto;
  }
  
  .organizer-card {
    flex-direction: column;
    text-align: center;
  }
  
  .org-logo {
    margin: 0 auto;
  }
  
  .org-links {
    justify-content: center;
    flex-wrap: wrap;
  }
}
</style>