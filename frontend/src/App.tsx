import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router";
import StoryLoader from "./components/StoryLoader";
import StoryGenerator from "./components/StoryGenerator";

function App() {
  return (
    <Router>
      <div className="app-container">
        <header>
          <h1>CreateYourStory.ai</h1>
        </header>
        <main>
          <Routes>
            <Route
              path={"/"}
              element={
                <div className="story-generator">
                  <StoryGenerator />
                </div>
              }
            />
            <Route path={"/story/:id"} element={<StoryLoader />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
