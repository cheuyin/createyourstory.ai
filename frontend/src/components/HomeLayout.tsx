import { useContext } from "react";
import { Outlet, useNavigate } from "react-router";
import { AuthContext } from "../auth";
import { Button, DarkThemeToggle, Navbar, NavbarBrand } from "flowbite-react";

export default function HomeLayout() {
  const { currentUser, setCurrentUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    setCurrentUser(null);
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-amber-50/60 to-white dark:from-gray-900 dark:to-gray-950">
      <Navbar
        fluid
        className="border-b border-amber-200/50 bg-transparent dark:border-gray-700/50"
      >
        <NavbarBrand
          href="/"
          onClick={(e) => {
            e.preventDefault();
            navigate("/");
          }}
        >
          <span className="mr-2 text-2xl">📖</span>
          <span className="self-center text-xl font-bold tracking-tight whitespace-nowrap text-gray-900 dark:text-white">
            CreateYourStory
            <span className="text-amber-500">.ai</span>
          </span>
        </NavbarBrand>
        <div className="flex items-center gap-2 md:order-2">
          <DarkThemeToggle />
          {currentUser ? (
            <>
              <span className="hidden text-sm text-gray-600 sm:inline dark:text-gray-400">
                Hi, {currentUser.fullName.split(" ")[0]}
              </span>
              <Button size="sm" color="gray" onClick={handleLogout}>
                Log out
              </Button>
            </>
          ) : (
            <>
              <Button size="sm" color="gray" onClick={() => navigate("/login")}>
                Sign in
              </Button>
              <Button
                size="sm"
                color="primary"
                onClick={() => navigate("/signup")}
              >
                Sign up
              </Button>
            </>
          )}
        </div>
      </Navbar>

      <main className="mx-auto w-full px-4 py-8">
        <Outlet />
      </main>
    </div>
  );
}
