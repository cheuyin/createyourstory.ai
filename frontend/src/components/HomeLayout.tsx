import { useContext } from "react";
import { Outlet, useNavigate } from "react-router";
import { AuthContext } from "../auth";

export default function HomeLayout() {
  const { currentUser, setCurrentUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    setCurrentUser(null);
    navigate("/");
  };

  return (
    <div>
      <div>
        <h1>CreateYourStory.ai</h1>
        {currentUser ? (
          <>
            <p>Hi {currentUser.fullName}!</p>
            <button onClick={handleLogout}>Log Out</button>
          </>
        ) : (
          <>
            <button onClick={() => navigate("/login")}>Sign In</button>
            <button onClick={() => navigate("/signup")}>Sign Up</button>
          </>
        )}
        <Outlet />
      </div>
    </div>
  );
}
