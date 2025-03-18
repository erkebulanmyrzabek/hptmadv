import { ref, watch } from 'vue'

const theme = ref(localStorage.getItem('theme') || 'light')

// Set initial theme
if (typeof document !== 'undefined') {
  document.documentElement.setAttribute('data-theme', theme.value)
}

export function useTheme() {
  // Watch for theme changes
  watch(theme, (newTheme) => {
    if (typeof document !== 'undefined') {
      document.documentElement.setAttribute('data-theme', newTheme)
    }
  })

  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    localStorage.setItem('theme', theme.value)
  }

  return {
    theme,
    toggleTheme
  }
}
