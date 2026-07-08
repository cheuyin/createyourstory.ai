import "./App.css";
import { Routes, Route, useNavigate } from "react-router";
import StoryLoader from "./components/StoryLoader";
import StoryGenerator from "./components/StoryGenerator";
import StoryList from "./components/StoryList";
import SignupPage from "./components/SignupPage";
import { AuthContext } from "./auth";
import { useState } from "react";
import type { User } from "./types";

function App() {
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  console.log("CURRENT USER", currentUser);

  return (
    <AuthContext value={{ currentUser, setCurrentUser }}>
      <div className="app-container">
        <header>
          <h1>CreateYourStory.ai</h1>
        </header>
        <main>
          <Routes>
            <Route
              path={"/"}
              element={
                <>
                  {currentUser ? (
                    <p>Signed in as: {currentUser.fullName}</p>
                  ) : (
                    <button onClick={() => navigate("/signup")}>Sign Up</button>
                  )}
                  <div className="story-generator">
                    <StoryGenerator />
                    <StoryList />
                  </div>
                </>
              }
            />
            <Route path={"/signup"} element={<SignupPage />} />
            <Route path={"/story/:id"} element={<StoryLoader />} />
          </Routes>
        </main>
      </div>
    </AuthContext>
  );
}

export default App;
