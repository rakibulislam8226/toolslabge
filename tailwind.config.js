/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./frontend/**/*.{vue,js,ts,jsx,tsx}",
    "./templates/**/*.html",
  ],
  darkMode: 'class', // Enable class-based dark mode
  theme: {
    extend: {
      colors: {
        // Custom theme colors that work with CSS variables
        'theme': {
          'bg-primary': 'var(--bg-primary)',
          'bg-secondary': 'var(--bg-secondary)',
          'bg-tertiary': 'var(--bg-tertiary)',
          'text-primary': 'var(--text-primary)',
          'text-secondary': 'var(--text-secondary)',
          'text-tertiary': 'var(--text-tertiary)',
          'border-primary': 'var(--border-primary)',
          'border-secondary': 'var(--border-secondary)',
          'accent-primary': 'var(--accent-primary)',
          'accent-secondary': 'var(--accent-secondary)',
        }
      },
      boxShadow: {
        'theme-light': 'var(--shadow-light)',
        'theme-medium': 'var(--shadow-medium)',
        'theme-large': 'var(--shadow-large)',
      },
      transitionDuration: {
        'theme-fast': 'var(--transition-fast)',
        'theme-normal': 'var(--transition-normal)',
        'theme-slow': 'var(--transition-slow)',
      },
      animation: {
        'pulse-slow': 'pulse 3s ease-in-out infinite',
        'gradient-shift': 'gradient-shift 4s ease infinite',
      },
      keyframes: {
        'gradient-shift': {
          '0%': { 'background-position': '0% 50%' },
          '50%': { 'background-position': '100% 50%' },
          '100%': { 'background-position': '0% 50%' },
        },
      },
      backgroundSize: {
        'gradient-animated': '200% 200%',
      },
    },
  },
  plugins: [
    // Plugin to generate theme-aware utilities
    function({ addUtilities, theme }) {
      const themeUtilities = {
        '.theme-transition': {
          'transition-property': 'background-color, border-color, color, fill, stroke, box-shadow',
          'transition-duration': theme('transitionDuration.theme-normal'),
          'transition-timing-function': 'ease-in-out',
        },
        '.theme-gradient-primary': {
          'background': 'linear-gradient(to right, var(--accent-primary), var(--accent-secondary))',
        },
        '.theme-gradient-animated': {
          'background-size': '200% 200%',
          'animation': 'gradient-shift 4s ease infinite',
        },
        '.theme-glass': {
          'backdrop-filter': 'blur(20px)',
          'background': 'rgba(255, 255, 255, 0.1)',
          'border': '1px solid rgba(255, 255, 255, 0.2)',
        },
        '.dark .theme-glass': {
          'background': 'rgba(0, 0, 0, 0.2)',
          'border': '1px solid rgba(255, 255, 255, 0.1)',
        },
      }
      
      addUtilities(themeUtilities)
    }
  ],
}