import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { Toaster } from "sonner";

import App from "./App";
import "./index.css";

import { AuthProvider } from "./context/AuthContext";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>

        <Toaster
          richColors
          position="top-right"
          expand={true}
        />

        <App />

      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);