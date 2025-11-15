/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./portal/index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",//rutas que le dicen a tailwind donde buscar clases
     
  ],
  theme: {
    extend: {
      colors: {
        'portal-red': 'rgb(169, 17, 20)', // Tu color rojo perdonalizado
        'gris-claro': 'rgb(240, 240, 240)', // Gris claro para fondos
        'gris-oscuro': 'rgb(100, 100, 100)', // Gris oscuro para textos
        'cherry-rose': '#B1004A', // O 'rgb(177, 0, 74)'
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