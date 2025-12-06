import { ref, computed } from 'vue'

const isDark = ref(false)

export function useTheme() {
  // Apply theme to document
  const applyTheme = () => {
    const html = document.documentElement
    
    if (isDark.value) {
      html.classList.add('dark')
    } else {
      html.classList.remove('dark')
    }
  }

  // Initialize theme from localStorage or system preference
  const initializeTheme = () => {
    const stored = localStorage.getItem('theme')
    if (stored) {
      isDark.value = stored === 'dark'
    } else {
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    applyTheme()
  }

  // Toggle theme
  const toggleTheme = () => {
    isDark.value = !isDark.value
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
    applyTheme()
  }

  // Watch for system theme changes
  const watchSystemTheme = () => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    const handler = (e) => {
      if (!localStorage.getItem('theme')) {
        isDark.value = e.matches
        applyTheme()
      }
    }
    mediaQuery.addEventListener('change', handler)
    
    // Return cleanup function
    return () => {
      mediaQuery.removeEventListener('change', handler)
    }
  }

  // Computed theme icon
  const themeIcon = computed(() => isDark.value ? '🌙' : '☀️')

  return {
    isDark,
    toggleTheme,
    initializeTheme,
    watchSystemTheme,
    applyTheme,
    themeIcon
  }
}