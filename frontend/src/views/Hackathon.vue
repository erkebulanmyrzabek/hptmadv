<template>
  <div class="hackathons-page">
    <div class="page-header">
      <h1>🚀 Хакатоны</h1>
      <div class="filters">
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Поиск хакатонов..."
            class="search-input"
          >
          <span class="search-icon">🔍</span>
        </div>
        <div class="filter-buttons">
          <button 
            v-for="status in ['all', 'registration', 'in_progress', 'anounce', 'finished', 'archived']"
            :key="status"
            :class="['filter-btn', { active: currentFilter === status }]"
            @click="currentFilter = status"
          >
            {{ getStatusText(status) }}
            <span class="status-icon">{{ getStatusIcon(status) }}</span>
          </button>
        </div>
      </div>
    </div>

    <div class="hackathons-grid">
      <template v-if="filteredHackathons.length">
        <hackathon-card
          v-for="hackathon in filteredHackathons"
          :key="hackathon.id"
          :hackathon="hackathon"
          @register="handleRegister"
        />
      </template>
      <div v-else-if="loading" class="loading-state">
        <div class="loader"></div>
        <p>Загрузка хакатонов... 🔄</p>
      </div>
      <div v-else class="empty-state">
        <p>🏜️ Хакатоны не найдены</p>
        <p class="empty-subtitle">Попробуйте изменить параметры поиска</p>
      </div>
    </div>
  </div>
</template>

<script>
import HackathonCard from '../components/HackathonCard.vue';
import axios from 'axios';
import { ref, computed, onMounted } from 'vue';

export default {
  components: {
    HackathonCard
  },
  setup() {
    const hackathons = ref([]);
    const loading = ref(true);
    const searchQuery = ref('');
    const currentFilter = ref('all');

    onMounted(async () => {
      await fetchHackathons();
    });

    const fetchHackathons = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/events/hackathons/');
            hackathons.value = response.data;
        } catch (error) {
            console.error('Error fetching hackathons:', error);
        } finally {
            loading.value = false;
        }
    };

    const filteredHackathons = computed(() => {
      let filtered = [...hackathons.value];

      // Фильтрация по поиску
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        filtered = filtered.filter(h => 
          h.title.toLowerCase().includes(query) ||
          h.short_description.toLowerCase().includes(query) ||
          h.tags.some(tag => tag.name.toLowerCase().includes(query))
        );
      }

      // Фильтрация по статусу
      if (currentFilter.value !== 'all') {
        filtered = filtered.filter(h => h.status === currentFilter.value);
      }

      return filtered;
    });

    const getStatusText = (status) => {
      const statusMap = {
        'all': 'Все',
        'archived': 'Архив',
        'anounce': 'Анонс',
        'registration': 'Регистрация',
        'in_progress': 'В процессе',
        'finished': 'Завершен'
      };
      return statusMap[status] || status;
    };

    const getStatusIcon = (status) => {
      const iconMap = {
        'all': '📋',
        'archived': '📦',
        'anounce': '📢',
        'registration': '✍️',
        'in_progress': '🔥',
        'finished': '🏁'
      };
      return iconMap[status] || '❓';
    };

    const handleRegister = (hackathonId) => {
      // Здесь будет ваш код для регистрации на хакатон
      console.log('Регистрация на хакатон:', hackathonId);
    };

    return {
      hackathons,
      loading,
      searchQuery,
      currentFilter,
      filteredHackathons,
      getStatusText,
      getStatusIcon,
      handleRegister
    };
  }
};
</script>

<style scoped>
.hackathons-page {
  padding: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 40px;
}

h1 {
  font-size: 36px;
  color: #00BFFF;
  margin-bottom: 30px;
  text-shadow: 0 0 10px rgba(0, 191, 255, 0.3);
  display: flex;
  align-items: center;
  gap: 15px;
}

.filters {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.search-box {
  position: relative;
  max-width: 500px;
}

.search-input {
  width: 100%;
  padding: 15px 20px;
  padding-left: 50px;
  background: rgba(42, 52, 53, 0.7);
  border: 2px solid rgba(0, 191, 255, 0.2);
  border-radius: 25px;
  color: #fff;
  font-size: 16px;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #00BFFF;
  box-shadow: 0 0 15px rgba(0, 191, 255, 0.2);
}

.search-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 20px;
}

.filter-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 20px;
  border-radius: 20px;
  background: rgba(42, 52, 53, 0.7);
  border: none;
  color: #ccc;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-btn:hover {
  background: rgba(0, 191, 255, 0.1);
  color: #00BFFF;
}

.filter-btn.active {
  background: #00BFFF;
  color: white;
}

.status-icon {
  font-size: 18px;
}

.hackathons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 30px;
}

.loading-state, .empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 50px;
  color: #ccc;
}

.loader {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(0, 191, 255, 0.1);
  border-top-color: #00BFFF;
  border-radius: 50%;
  margin: 0 auto 20px;
  animation: spin 1s linear infinite;
}

.empty-subtitle {
  color: #888;
  margin-top: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .hackathons-page {
    padding: 20px;
  }

  .filter-buttons {
    flex-wrap: nowrap;
    overflow-x: auto;
    padding-bottom: 10px;
    -webkit-overflow-scrolling: touch;
  }

  .filter-btn {
    white-space: nowrap;
  }

  .hackathons-grid {
    grid-template-columns: 1fr;
  }
}
</style>