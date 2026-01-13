/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          'Inter',
          'Noto Sans SC',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'PingFang SC',
          'Hiragino Sans GB',
          'Microsoft YaHei',
          'Helvetica Neue',
          'Arial',
          'sans-serif',
        ],
        mono: [
          'SF Mono',
          'Monaco',
          'Menlo',
          'Consolas',
          'Liberation Mono',
          'Courier New',
          'monospace',
        ],
      },
      letterSpacing: {
        tighter: '-0.02em',
        tight: '-0.01em',
        normal: '0',
        wide: '0.01em',
        wider: '0.02em',
        widest: '0.05em',
      },
      colors: {
        'bg-primary': '#ffffff',
        'bg-secondary': '#f7f7f8',
        'text-primary': '#353740',
        'text-secondary': '#6e6e80',
        'border': '#e5e5e6',
        'user-message-bg': '#f7f7f8',
        'ai-message-bg': '#ffffff',
        'button-primary': '#10a37f',
        'button-hover': '#0d8f6e',
      },
    },
  },
  plugins: [],
}
