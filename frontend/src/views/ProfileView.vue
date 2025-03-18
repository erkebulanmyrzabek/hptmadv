<template>
  <div class="profile-container">
    <transition name="slide">
      <div v-if="!authStore.isProfileComplete" class="alert">
        Заполните профиль для участия в хакатонах!
        <router-link to="/profile/settings">Перейти</router-link>
      </div>
    </transition>
    <h1>{{ authStore.user.first_name }} {{ authStore.user.last_name }}</h1>
    <img :src="authStore.user.avatar" alt="Avatar" class="avatar" />
    <p>Уровень: {{ authStore.user.level }} | XP: {{ authStore.user.xp }}</p>
    <p>Кристаллы: {{ authStore.user.balance }}</p>
    <h2>Мои команды</h2>
    <div v-for="team in authStore.user.teams" :key="team" class="team-card">
      <TeamCard :team-id="team" />
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth';
import TeamCard from '../components/TeamCard.vue';

export default {
  components: { TeamCard },
  setup() {
    const authStore = useAuthStore();
    if (!authStore.user) authStore.fetchUser();
    return { authStore };
  },
};
</script>

<style scoped>
.profile-container {
  padding: 20px;
  background: var(--tg-theme-bg-color, #ffffff);
  color: var(--tg-theme-text-color, #000000);
}
.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin: 10px 0;
}
.alert {
  background: #ffcccc;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 20px;
}
.team-card {
  margin: 10px 0;
}
.slide-enter-active, .slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter-from, .slide-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}
</style>