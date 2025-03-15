<template>
  <div class="hackathon-card" :class="{ 'registration': hackathon.status === 'registration' }">
    <div class="card-header">
      <img :src="hackathon.details.preview_image" alt="Hackathon Preview" class="preview-image">
      <div class="status-badge" :class="hackathon.status">
        {{ getStatusText(hackathon.status) }} 
        <span class="status-icon">{{ getStatusIcon(hackathon.status) }}</span>
      </div>
    </div>

    <div class="card-content">
      <h2 class="title">{{ hackathon.title }}</h2>
      <p class="description">{{ hackathon.details.short_description }}</p>

      <div class="info-grid">
        <div class="info-item">
          <span class="icon">📅</span>
          <span class="label">Начало:</span>
          <span class="value">{{ formatDate(hackathon.schedule.start_date) }}</span>
        </div>
        <div class="info-item">
          <span class="icon">⏳</span>
          <span class="label">Длительность:</span>
          <span class="value">{{ getDuration(hackathon.schedule.start_date, hackathon.schedule.end_date) }}</span>
        </div>
        <div class="info-item">
          <span class="icon">🎯</span>
          <span class="label">Формат:</span>
          <span class="value">{{ getFormatText(hackathon.type) }}</span>
        </div>
        <div class="info-item">
          <span class="icon">👥</span>
          <span class="label">Участники:</span>
          <span class="value">{{ hackathon.participants?.length || 0 }}/{{ hackathon.participants_info.max_participants || '∞' }}</span> 
        </div>
      </div>

      <div class="tags">
        <span v-for="tag in hackathon.tags" :key="tag.id" class="tag">
          #{{ tag.name }}
        </span>
      </div>

      <div class="prize-pool" v-if="hackathon.hackathon_prizes.length > 0">
        <span class="prize-icon">🏆</span>
        <span class="prize-amount">{{ hackathon.hackathon_prizes.reduce((acc, prize) => acc + prize.prize_amount, 0) }}₸</span>
      </div>

      <div class="card-actions">
        <router-link :to="'/hackathons/' + hackathon.id" class="details-btn">
          Подробнее
          <span class="arrow">→</span>
        </router-link>
        <button 
          v-if="hackathon.status === 'registration'" 
          class="register-btn"
          @click="$emit('register', hackathon.id)"
        >
          Участвовать 🚀
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    hackathon: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return 'Не указано';
      return new Date(date).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      });
    },
    getDuration(start, end) {
      if (!start || !end) return 'Не указано';
      const days = Math.ceil((new Date(end) - new Date(start)) / (1000 * 60 * 60 * 24));
      return `${days} ${this.getDaysWord(days)}`;
    },
    getDaysWord(days) {
      const cases = [2, 0, 1, 1, 1, 2];
      const titles = ['день', 'дня', 'дней'];
      return titles[(days % 100 > 4 && days % 100 < 20) ? 2 : cases[(days % 10 < 5) ? days % 10 : 5]];
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
    }
  }
};
</script>

<style scoped>
.hackathon-card {
  background: linear-gradient(145deg, #2A3435, #1a2223);
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  margin-bottom: 30px;
}

.hackathon-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
}

.card-header {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.hackathon-card:hover .preview-image {
  transform: scale(1.05);
}

.status-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  padding: 8px 15px;
  border-radius: 20px;
  color: white;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  backdrop-filter: blur(5px);
}

.status-badge.registration {
  background: rgba(46, 213, 115, 0.8);
}

.status-badge.in_progress {
  background: rgba(255, 71, 87, 0.8);
}

.status-badge.archived {
  background: rgba(128, 128, 128, 0.8);
}

.status-badge.anounce {
  background: rgba(54, 174, 255, 0.8);
}

.status-badge.finished {
  background: rgba(116, 185, 255, 0.8);
}

.card-content {
  padding: 25px;
}

.title {
  font-size: 24px;
  color: #00BFFF;
  margin-bottom: 15px;
  text-shadow: 0 0 10px rgba(0, 191, 255, 0.3);
}

.description {
  color: #ccc;
  margin-bottom: 20px;
  line-height: 1.5;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.icon {
  font-size: 20px;
}

.label {
  color: #888;
  font-size: 14px;
}

.value {
  color: #fff;
  font-weight: 500;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.tag {
  background: rgba(0, 191, 255, 0.1);
  color: #00BFFF;
  padding: 5px 12px;
  border-radius: 15px;
  font-size: 14px;
}

.prize-pool {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  background: linear-gradient(45deg, #FFD700, #FFA500);
  padding: 10px 20px;
  border-radius: 15px;
  display: inline-flex;
}

.prize-icon {
  font-size: 24px;
}

.prize-amount {
  color: #fff;
  font-weight: bold;
  font-size: 20px;
}

.card-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
}

.details-btn, .register-btn {
  padding: 12px 25px;
  border-radius: 25px;
  font-weight: 500;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.details-btn {
  background: rgba(0, 191, 255, 0.1);
  color: #00BFFF;
}

.details-btn:hover {
  background: rgba(0, 191, 255, 0.2);
  transform: translateX(5px);
}

.register-btn {
  background: linear-gradient(45deg, #00BFFF, #0099cc);
  color: white;
  border: none;
  cursor: pointer;
}

.register-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 191, 255, 0.3);
}

.arrow {
  transition: transform 0.3s ease;
}

.details-btn:hover .arrow {
  transform: translateX(5px);
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .card-actions {
    flex-direction: column;
  }

  .details-btn, .register-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>