/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'Avenir', 'Helvetica', 'Arial', 'sans-serif'],
      },
      colors: {
        'deep-blue': '#0a192f',
        'ice-white': '#f8fafc',
        'neon-cyan': '#00f0ff',
      }
    },
  },
  plugins: [],
}
