import { useContext, useState } from "react";
import { BASE_URL } from "../api";
import { AuthContext } from "../auth";
import { Link, useNavigate } from "react-router";
import { Button, Card, Label, TextInput } from "flowbite-react";
import ErrorAlert from "./ErrorAlert";

export default function SignupPage() {
  const { setCurrentUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.SubmitEvent) {
    event.preventDefault();
    setError(null);

    try {
      const formData = new FormData(event.target);
      const response = await fetch(`${BASE_URL}/api/auth/signup`, {
        method: "POST",
        body: JSON.stringify({
          full_name: formData.get("full_name"),
          username: formData.get("username"),
          password: formData.get("userPassword"),
        }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await response.json();
      if (!response.ok) {
        setError(data.error || "Sign up failed. Please check your details.");
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
          Create an account
        </h1>
        {error && <ErrorAlert message={error} />}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <div className="mb-2 block">
              <Label htmlFor="fullname-input">Full name</Label>
            </div>
            <TextInput
              id="fullname-input"
              name="full_name"
              required
              type="text"
              autoComplete="off"
            />
          </div>
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
              name="userPassword"
              required
              type="password"
              autoComplete="off"
            />
          </div>
          <Button type="submit">Create account</Button>
        </form>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Already have an account?{" "}
          <Link
            to="/login"
            className="text-primary-600 hover:underline dark:text-primary-500"
          >
            Sign in
          </Link>
        </p>
      </Card>
    </div>
  );
}
