<template>
    <nav class="navbar">
        <div class="nav-content">
            <RouterLink to="/" class="nav-item" active-class="active">
                <div class="nav-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                    </svg>
                </div>
                <span>Главная</span>
            </RouterLink>

            <RouterLink to="/hackathons" class="nav-item" active-class="active">
                <div class="nav-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="16 18 22 12 16 6"/>
                        <polyline points="8 6 2 12 8 18"/>
                    </svg>
                </div>
                <span>Хакатоны</span>
            </RouterLink>

            <RouterLink to="/rating" class="nav-item" active-class="active">
                <div class="nav-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="8" r="6"/>
                        <path d="M12 2v12"/>
                        <path d="M8 14l4 8 4-8"/>
                    </svg>
                </div>
                <span>Рейтинг</span>
            </RouterLink>

            <RouterLink to="/shop" class="nav-item" active-class="active">
                <div class="nav-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="8" cy="21" r="1"/>
                        <circle cx="19" cy="21" r="1"/>
                        <path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>
                    </svg>
                </div>
                <span>Магазин</span>
            </RouterLink>

            <RouterLink to="/profile" class="nav-item" active-class="active">
                <div class="nav-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="8" r="4"/>
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    </svg>
                </div>
                <span>Профиль</span>
            </RouterLink>
        </div>
    </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.navbar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--surface-color);
    box-shadow: var(--shadow-sm);
    padding: 10px 0;
    z-index: 1000;
    height: 70px;
    display: flex;
    align-items: center;
}

.nav-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-around;
    align-items: center;
    width: 100%;
    padding: 0 20px;
}

.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
    color: var(--text-secondary);
    font-size: 0.75rem;
    padding: 8px 12px;
    border-radius: var(--radius-md);
    transition: all 0.3s ease;
}

.nav-item:hover {
    color: var(--primary-color);
    transform: translateY(-2px);
}

.nav-item.active {
    color: var(--primary-color);
}

.nav-icon {
    width: 24px;
    height: 24px;
    margin-bottom: 4px;
}

.nav-icon svg {
    width: 100%;
    height: 100%;
}

@media (min-width: 768px) {
    .navbar {
        top: 0;
        bottom: auto;
        padding: 0;
        height: 70px;
    }

    .nav-content {
        padding: 0 40px;
    }

    .nav-item {
        flex-direction: row;
        font-size: 0.875rem;
        gap: 8px;
        height: 70px;
        padding: 0 16px;
        border-radius: 0;
    }

    .nav-icon {
        margin-bottom: 0;
    }

    .nav-item:hover {
        transform: none;
        background: var(--surface-variant);
    }

    .nav-item.active {
        box-shadow: inset 0 -2px 0 var(--primary-color);
    }
}
</style>