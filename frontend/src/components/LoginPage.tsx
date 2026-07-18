import { useContext } from "react";
import { BASE_URL } from "../api";
import { Link, useNavigate } from "react-router";
import { AuthContext } from "../auth";
import { Button, Card, Label, TextInput } from "flowbite-react";

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
    <div className="flex justify-center">
      <Card className="w-full max-w-sm">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Sign in
        </h1>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <div className="mb-2 block">
              <Label htmlFor="username-input">Username</Label>
            </div>
            <TextInput
              id="username-input"
              name="username"
              required
              type="text"
              autoComplete="off"
            />
          </div>
          <div>
            <div className="mb-2 block">
              <Label htmlFor="password-input">Password</Label>
            </div>
            <TextInput
              id="password-input"
              name="password"
              required
              type="password"
              autoComplete="off"
            />
          </div>
          <Button type="submit">Sign in</Button>
        </form>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Don&rsquo;t have an account?{" "}
          <Link
            to="/signup"
            className="text-cyan-600 hover:underline dark:text-cyan-500"
          >
            Sign up
          </Link>
        </p>
      </Card>
    </div>
  );
}
