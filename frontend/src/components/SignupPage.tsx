import { useContext } from "react";
import { BASE_URL } from "../api";
import { AuthContext } from "../auth";
import { useNavigate } from "react-router";

export default function SignupPage() {
  const { setCurrentUser } = useContext(AuthContext);
  const navigate = useNavigate();

  async function handleSubmit(event: React.SubmitEvent) {
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
    }
    const { access_token } = data;
    localStorage.setItem("accessToken", access_token);
    const user_response = await fetch(`${BASE_URL}/api/auth/users/me`, {
      headers: new Headers({
        Accept: "application/json",
        Authorization: "Bearer " + access_token,
      }),
    });
    const user_data = await user_response.json();
    if (!user_response) {
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
      <label htmlFor="fullname-input">Full Name</label>
      <input
        id="fullname-input"
        name="full_name"
        required
        type="text"
        autoComplete="off"
      />
      <label htmlFor="Username-input">Username</label>
      <input
        id="Username-input"
        name="username"
        required
        type="Username"
        autoComplete="off"
      />
      <label htmlFor="password-input">Password</label>
      <input
        aria-describedby="password-hint"
        id="password-input"
        name="userPassword"
        required
        type="password"
        autoComplete="off"
      />
      <button type="submit">Create Account</button>
    </form>
  );
}
