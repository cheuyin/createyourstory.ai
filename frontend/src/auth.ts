import { createContext, type Dispatch, type SetStateAction } from "react";
import type { UserPublic } from "./types";

interface AuthContextType {
  currentUser: UserPublic | null;
  setCurrentUser: Dispatch<SetStateAction<UserPublic | null>>;
}

export const AuthContext = createContext<AuthContextType>({
  currentUser: null,
  setCurrentUser: () => null,
});
