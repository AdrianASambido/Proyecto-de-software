/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
       colors: {
        'portal-red': 'rgb(169, 17, 20)', 
        'gris-claro': 'rgb(240, 240, 240)', 
        'gris-oscuro': 'rgb(100, 100, 100)', 
        'cherry-rose': '#B1004A', 
      },
      fontFamily: {
        // Fuentes personalizadas
        'roboto': ['Roboto', 'sans-serif'],
        'headings': ['Playfair Display', 'serif'],
      },
    },
  },
  plugins: [],
}
