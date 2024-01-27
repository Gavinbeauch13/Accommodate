/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      'black': '#000000',
      'white': '#FFFFFF'
    },
  },
  plugins: [],
}

