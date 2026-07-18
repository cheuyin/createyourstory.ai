import { useContext } from "react";
import { Link, Outlet, useNavigate } from "react-router";
import { AuthContext } from "../auth";
import {
  Button,
  DarkThemeToggle,
  Navbar,
  NavbarBrand,
  NavbarCollapse,
  NavbarLink,
  NavbarToggle,
} from "flowbite-react";

export default function HomeLayout() {
  const { currentUser, setCurrentUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    setCurrentUser(null);
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar fluid className="border-b border-gray-200 dark:border-gray-700">
        <NavbarBrand as={Link} href="/">
          <span className="self-center text-xl font-semibold whitespace-nowrap dark:text-white">
            CreateYourStory.ai
          </span>
        </NavbarBrand>
        <div className="flex items-center gap-2 md:order-2">
          <DarkThemeToggle />
          {currentUser ? (
            <Button size="sm" color="gray" onClick={handleLogout}>
              Log out
            </Button>
          ) : (
            <>
              <Button size="sm" color="gray" onClick={() => navigate("/login")}>
                Sign in
              </Button>
              <Button size="sm" onClick={() => navigate("/signup")}>
                Sign up
              </Button>
            </>
          )}
          <NavbarToggle />
        </div>
        <NavbarCollapse>
          <NavbarLink as={Link} href="/" active>
            Home
          </NavbarLink>
        </NavbarCollapse>
      </Navbar>

      <main className="mx-auto max-w-4xl px-4 py-8">
        {currentUser && (
          <p className="mb-6 text-gray-600 dark:text-gray-400">
            Welcome back, {currentUser.fullName}!
          </p>
        )}
        <Outlet />
      </main>
    </div>
  );
}
