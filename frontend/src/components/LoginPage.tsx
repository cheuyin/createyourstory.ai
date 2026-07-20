import { useContext, useState } from "react";
import { BASE_URL } from "../api";
import { Link, useNavigate } from "react-router";
import { AuthContext } from "../auth";
import { Button, Card, Label, TextInput } from "flowbite-react";
import ErrorAlert from "./ErrorAlert";

export default function LoginPage() {
  const { setCurrentUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.SubmitEvent) {
    event.preventDefault();
    setError(null);

    try {
      const formData = new FormData(event.target);
      const response = await fetch(`${BASE_URL}/api/auth/login`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        setError(data.error || "Sign in failed. Please check your credentials.");
        return;
      }

      localStorage.setItem("accessToken", data.access_token);
      const userResponse = await fetch(`${BASE_URL}/api/auth/users/me`);
      const userData = await userResponse.json();
      if (!userResponse.ok) {
        localStorage.removeItem("accessToken");
        setError(userData.error || "We couldn’t load your account.");
        return;
      }
      setCurrentUser({
        fullName: userData.full_name,
        username: userData.username,
      });
      navigate("/");
    } catch {
      setError("We couldn’t reach the server. Please try again.");
    }
  }

  return (
    <div className="flex justify-center">
      <Card className="w-full max-w-sm">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Sign in
        </h1>
        {error && <ErrorAlert message={error} />}
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
            className="text-primary-600 hover:underline dark:text-primary-500"
          >
            Sign up
          </Link>
        </p>
      </Card>
    </div>
  );
}
