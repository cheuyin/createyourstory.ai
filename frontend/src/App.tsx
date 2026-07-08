import "./App.css";
import { Routes, Route } from "react-router";
import StoryLoader from "./components/StoryLoader";
import StoryGenerator from "./components/StoryGenerator";
import StoryList from "./components/StoryList";
import SignupPage from "./components/SignupPage";
import { AuthContext } from "./auth";
import { useEffect, useState } from "react";
import type { User } from "./types";
import { BASE_URL } from "./api";
import HomeLayout from "./components/HomeLayout";
import LoginPage from "./components/LoginPage";

function App() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      const accessToken = localStorage.getItem("accessToken");
      if (accessToken) {
        const user_response = await fetch(`${BASE_URL}/api/auth/users/me`, {
          headers: new Headers({
            Accept: "application/json",
            Authorization: "Bearer " + accessToken,
          }),
        });
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
      <div className="app-container">
        <header>
          <h1>CreateYourStory.ai</h1>
        </header>
        <main>
          <Routes>
            <Route element={<HomeLayout />}>
              <Route
                path={"/"}
                element={
                  <div className="story-generator">
                    <StoryGenerator />
                    <StoryList />
                  </div>
                }
              />
            </Route>
            <Route path={"/signup"} element={<SignupPage />} />
            <Route path={"/login"} element={<LoginPage />} />
            <Route path={"/story/:id"} element={<StoryLoader />} />
          </Routes>
        </main>
      </div>
    </AuthContext>
  );
}

export default App;
