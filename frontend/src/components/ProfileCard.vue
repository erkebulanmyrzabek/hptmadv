<template>
    <div class="profile-card">
      <p><strong>Username:</strong> @{{ user.username }}</p>
      <p><strong>Имя:</strong> {{ user.first_name }}</p>
      <p><strong>Фамилия:</strong> {{ user.last_name }}</p>
      <p><strong>Telegram ID:</strong> {{ user.telegram_id }}</p>
      <p><strong>Уровень:</strong> {{ user.level }}</p>
      <p><strong>Опыт (XP):</strong> {{ user.xp }}</p>
      <p><strong>Кристаллы:</strong> {{ user.balance }}</p>
    </div>
  </template>
  
  <script>

  export default {
    props: {
      user: {
        type: Object,
        required: true,
      },
    }
  };
  </script>
  
  <style scoped>
  .profile-card {
    border: 1px solid #ccc;
    padding: 20px;
    border-radius: 5px;
    max-width: 400px;
    margin: 20px auto;
  }
  </style>