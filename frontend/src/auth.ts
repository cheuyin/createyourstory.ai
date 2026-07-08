import { createContext, type Dispatch, type SetStateAction } from "react";
import type { User } from "./types";

interface AuthContextType {
  currentUser: User | null;
  setCurrentUser: Dispatch<SetStateAction<User | null>>;
}

export const AuthContext = createContext<AuthContextType>({
  currentUser: null,
  setCurrentUser: () => null,
});
