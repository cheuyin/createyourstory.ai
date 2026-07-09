import { useContext } from "react";
import { BASE_URL } from "../api";
import { useNavigate } from "react-router";
import { AuthContext } from "../auth";

export default function LoginPage() {
  const { setCurrentUser } = useContext(AuthContext);
  const navigate = useNavigate();

  async function handleSubmit(event: React.SubmitEvent) {
    event.preventDefault();

    const formElement = event.target;
    const formData = new FormData(formElement);

    const response = await fetch(`${BASE_URL}/api/auth/login`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      alert(data.error);
      return;
    }

    const { access_token } = data;
    localStorage.setItem("accessToken", access_token);
    const user_response = await fetch(`${BASE_URL}/api/auth/users/me`);
    const user_data = await user_response.json();
    if (!user_response.ok) {
      alert(user_data.error);
      return;
    }
    setCurrentUser({
      fullName: user_data.full_name,
      username: user_data.username,
    });
    navigate("/");
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="username-input">Username</label>
      <input
        id="username-input"
        name="username"
        required
        type="text"
        autoComplete="off"
      />
      <label htmlFor="password-input">Password</label>
      <input
        id="password-input"
        name="password"
        required
        type="password"
        autoComplete="off"
      />
      <button type="submit">Sign In</button>
    </form>
  );
}
