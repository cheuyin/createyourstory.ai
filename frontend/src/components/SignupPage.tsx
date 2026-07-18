import { useContext } from "react";
import { BASE_URL } from "../api";
import { AuthContext } from "../auth";
import { Link, useNavigate } from "react-router";
import { Button, Card, Label, TextInput } from "flowbite-react";

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
      headers: {
        "Content-Type": "application/json",
      },
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
          Create an account
        </h1>
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
            className="text-cyan-600 hover:underline dark:text-cyan-500"
          >
            Sign in
          </Link>
        </p>
      </Card>
    </div>
  );
}
