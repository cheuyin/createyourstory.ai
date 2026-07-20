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
import ErrorAlert from "./components/ErrorAlert";

function App() {
  const [currentUser, setCurrentUser] = useState<UserPublic | null>(null);
  const [authError, setAuthError] = useState<string | null>(null);

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
        try {
          const userResponse = await fetch(`${BASE_URL}/api/auth/users/me`);
          const userData = await userResponse.json();
          if (!userResponse.ok) {
            setAuthError(userData.error || "Your session has expired. Please sign in again.");
            localStorage.removeItem("accessToken");
            setCurrentUser(null);
            return;
          }
          setCurrentUser({
            fullName: userData.full_name,
            username: userData.username,
          });
        } catch {
          setAuthError("We couldn’t verify your session. Please try again.");
          localStorage.removeItem("accessToken");
          setCurrentUser(null);
        }
      }
    };
    fetchUser();
  }, []);

  return (
    <AuthContext value={{ currentUser, setCurrentUser }}>
      {authError && (
        <div className="mx-auto max-w-4xl px-4 pt-4">
          <ErrorAlert message={authError} />
        </div>
      )}
      <Routes>
        <Route element={<HomeLayout />}>
          <Route
            path={"/"}
            element={
              <div className="mx-auto max-w-4xl">
                <div className="mb-10 text-center">
                  <h1 className="mb-3 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl dark:text-white">
                    What story will you{" "}
                    <span className="bg-gradient-to-r from-amber-500 to-orange-500 bg-clip-text text-transparent">
                      tell today
                    </span>
                    ?
                  </h1>
                  <p className="mx-auto max-w-xl text-lg text-gray-500 dark:text-gray-400">
                    Turn any idea into an interactive adventure in seconds.
                    Choose a theme, pick a model, and let AI craft your story.
                  </p>
                </div>
                <StoryGenerator />
                {currentUser ? (
                  <StoryList />
                ) : (
                  <p className="mt-8 text-center text-gray-500 dark:text-gray-400">
                    Sign in to view saved stories
                  </p>
                )}
              </div>
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
