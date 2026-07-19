import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import App from "./App";
import { BrowserRouter } from "react-router";
import { ThemeInit } from "../.flowbite-react/init";
import { ThemeProvider } from "flowbite-react";
import { appTheme } from "./theme";

const queryClient = new QueryClient();

// Workaround for flowbite-react 0.12.x: StoreInit applies the OS theme to the
// DOM but never persists it, leaving useThemeMode in an unresolved "auto"
// state where the first DarkThemeToggle click is a visual no-op. Seed the
// resolved mode once so the first toggle works.
if (!localStorage.getItem("flowbite-theme-mode")) {
  localStorage.setItem(
    "flowbite-theme-mode",
    window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light",
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <ThemeInit />
        <ThemeProvider theme={appTheme}>
          <App />
        </ThemeProvider>
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>,
);
