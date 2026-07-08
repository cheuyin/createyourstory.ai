import { useContext } from "react";
import { Outlet, useNavigate } from "react-router";
import { AuthContext } from "../auth";

export default function HomeLayout() {
  const { currentUser } = useContext(AuthContext);
  const navigate = useNavigate();
  return (
    <div>
      <div>
        <h1>CreateYourStory.ai</h1>
        {currentUser ? (
          <>
            <p>Hi {currentUser.fullName}!</p>
            <button>Log Out</button>
          </>
        ) : (
          <>
            <button>Sign In</button>
            <button onClick={() => navigate("/signup")}>Sign Up</button>
          </>
        )}
        <Outlet />
      </div>
    </div>
  );
}
