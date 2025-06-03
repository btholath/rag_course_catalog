# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.


npm create vite@latest frontend --template react
cd frontend
npm install
npm install axios react-router-dom


Step 2: Project Structure

frontend/
├── public/
├── src/
│   ├── components/
│   │   └── QueryForm.jsx
│   ├── pages/
│   │   └── Home.jsx
│   ├── api.js
│   ├── App.jsx
│   └── main.jsx
├── vite.config.js
└── index.html


Step 3: API Integration (src/api.js)
Component: QueryForm.jsx
Page: Home.jsx
App Entry: App.jsx
Main Entry: main.jsx
