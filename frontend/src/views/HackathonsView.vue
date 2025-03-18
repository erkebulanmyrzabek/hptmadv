<template>
  <div class="hackathon-container">
    <div class="filters">
      <select v-model="hackathonStore.filters.status">
        <option value="">Все статусы</option>
        <option value="registration">Регистрация</option>
        <option value="in_progress">В процессе</option>
        <option value="finished">Завершён</option>
      </select>
      <button @click="hackathonStore.fetchHackathons">Применить</button>
    </div>
    <transition-group name="list" tag="div" class="hackathon-list">
      <HackathonCard v-for="hackathon in hackathonStore.hackathons" :key="hackathon.id" :hackathon="hackathon" />
    </transition-group>
  </div>
</template>

<script>
import { useHackathonStore } from '../stores/hackathon';
import HackathonCard from '../components/HackathonCard.vue';

export default {
  components: { HackathonCard },
  setup() {
    const hackathonStore = useHackathonStore();
    hackathonStore.fetchHackathons();
    return { hackathonStore };
  },
};
</script>

<style scoped>
.hackathon-container {
  padding: 20px;
  background: var(--tg-theme-bg-color, #ffffff);
}
.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
select, button {
  padding: 8px;
  border-radius: 5px;
}
.hackathon-list {
  display: grid;
  gap: 15px;
}
.list-enter-active, .list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from, .list-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>