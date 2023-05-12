/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/*.{html,js}"],
  theme: {
    extend: {
      screens: {
        sm:  "576px",
        md:  "768px",
        lg:  "992px",
        xl:  "1200px",
        xxl: "1400px"
      },
      colors: {
        BGColor: '#191A1C',
        BGColorMid: '#3d3d3d',
        BGColorLow: 'hsl(0, 0%, 17%)',
        themeHigh: '#5800FF',
        themeMain: '#0096FF',
        themeMid: '#00D7FF',
        themeLow: '#72FFFF',
      }
    },
  },
  plugins: [],
}

