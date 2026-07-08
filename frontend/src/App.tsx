import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router";
import StoryLoader from "./components/StoryLoader";
import StoryGenerator from "./components/StoryGenerator";
import StoryList from "./components/StoryList";
import { BASE_URL } from "./api";

function App() {
  async function handleSubmit(event: React.SubmitEvent) {
    // Prevent default behavior, which is a navigation
    event.preventDefault();

    const formElement = event.target;
    const formData = new FormData(formElement);

    const response = await fetch(`${BASE_URL}/api/auth/signup`, {
      method: "POST",
      body: JSON.stringify({
        full_name: formData.get("full_name"),
        username: formData.get("username"),
        password: formData.get("userPassword"),
      }),
      headers: { "Content-Type": "application/json" },
    });

    const data = await response.json();
    if (!response.ok) {
      alert(data.error);
      return;
    } else {
      console.log("SUCCESS: ", data);
    }
  }
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
                  <form onSubmit={handleSubmit}>
                    <label htmlFor="fullname-input">Full Name</label>
                    <input
                      id="fullname-input"
                      name="full_name"
                      required
                      type="text"
                    />
                    <label htmlFor="Username-input">Username</label>
                    <input
                      id="Username-input"
                      name="username"
                      required
                      type="Username"
                    />
                    <label htmlFor="password-input">Password</label>
                    <input
                      aria-describedby="password-hint"
                      id="password-input"
                      min={8}
                      name="userPassword"
                      required
                      type="password"
                    />
                    <div id="password-hint">
                      Your password must be at least 8 characters long.
                    </div>
                    <button>Sign up</button>
                  </form>
                  <StoryGenerator />
                  <StoryList />
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
