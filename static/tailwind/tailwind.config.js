/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['../../templates/*.html',
            '../../templates/svg/*.svg'],
  theme: {
    fontFamily:{
      'sans':['Inter', 'ui-sans-serif', 'system-ui'],
	},
    extend: {},
  },
  plugins: [],
}

