import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";

// HTML 요소가 항상 존재함을 명시적으로 단언 (!)
const rootElement = document.getElementById("root") as HTMLElement;

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
