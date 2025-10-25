import { useTheme } from '@/composables/useTheme.js'

export default {
  install(app) {
    // Initialize theme system
    const { initializeTheme, watchSystemTheme } = useTheme()
    
    // Initialize theme on app start
    initializeTheme()
    
    // Watch for system theme changes
    const cleanup = watchSystemTheme()
    
    // Provide theme to all components
    app.config.globalProperties.$theme = useTheme()
    
    // Cleanup on unmount
    app.config.globalProperties.$themeCleanup = cleanup
  }
}