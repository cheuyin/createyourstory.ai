import { Routes, Route } from "react-router";
import StoryLoader from "./components/StoryLoader";
import StoryGenerator from "./components/StoryGenerator";
import StoryList from "./components/StoryList";
import SignupPage from "./components/SignupPage";
import { AuthContext } from "./auth";
import { useEffect, useLayoutEffect, useState } from "react";
import type { UserPublic } from "./types";
import { BASE_URL } from "./api";
import HomeLayout from "./components/HomeLayout";
import LoginPage from "./components/LoginPage";

function App() {
  const [currentUser, setCurrentUser] = useState<UserPublic | null>(null);

  useLayoutEffect(() => {
    const originalFetch = window.fetch;

    window.fetch = async (resource, config = {}) => {
      const token = localStorage.getItem("accessToken");

      const headers = new Headers(config.headers);

      if (token) {
        headers.set("Authorization", `Bearer ${token}`);
      }

      // Make sure this doesn't set FormData submissinos as JSON
      if (
        config.body &&
        typeof config.body === "string" &&
        !headers.has("Content-Type")
      ) {
        headers.set("Content-Type", "application/json");
      }

      const response = await originalFetch(resource, {
        ...config,
        headers,
      });

      if (response.status === 401) {
        localStorage.removeItem("accessToken");
        setCurrentUser(null);
      }
      return response;
    };
    return () => {
      window.fetch = originalFetch;
    };
  }, []);

  useEffect(() => {
    const fetchUser = async () => {
      const accessToken = localStorage.getItem("accessToken");
      if (accessToken) {
        const user_response = await fetch(`${BASE_URL}/api/auth/users/me`);
        const user_data = await user_response.json();
        if (!user_response.ok) {
          alert(user_data.error);
          localStorage.removeItem("accessToken");
          setCurrentUser(null);
          return;
        }
        setCurrentUser({
          fullName: user_data.full_name,
          username: user_data.username,
        });
      }
    };
    fetchUser();
  }, []);

  return (
    <AuthContext value={{ currentUser, setCurrentUser }}>
      <Routes>
        <Route element={<HomeLayout />}>
          <Route
            path={"/"}
            element={
              <>
                <StoryGenerator />
                {currentUser ? (
                  <StoryList />
                ) : (
                  <p className="mt-6 text-center text-gray-500 dark:text-gray-400">
                    Sign in to view saved stories
                  </p>
                )}
              </>
            }
          />
          <Route path={"/signup"} element={<SignupPage />} />
          <Route path={"/login"} element={<LoginPage />} />
          <Route path={"/story/:id"} element={<StoryLoader />} />
        </Route>
      </Routes>
    </AuthContext>
  );
}

export default App;
