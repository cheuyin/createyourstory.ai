import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import App from "./App";
import { BrowserRouter } from "react-router";
import { ThemeInit } from "../.flowbite-react/init";

const queryClient = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <ThemeInit />
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>,
);
