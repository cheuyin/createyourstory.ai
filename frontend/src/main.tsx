import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import App from "./App";
import { BrowserRouter } from "react-router";
import { ThemeInit } from "../.flowbite-react/init";
import { initThemeMode, ThemeProvider } from "flowbite-react";
import { appTheme } from "./theme";

// Apply persisted/OS theme to <html> before React mounts so DarkThemeToggle's
// first click is never a no-op (useThemeMode only writes the DOM on toggle).
initThemeMode();

const queryClient = new QueryClient();

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
