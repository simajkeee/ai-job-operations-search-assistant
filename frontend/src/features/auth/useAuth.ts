import { AuthContext, type AuthContextValue } from "./authContext.ts";
import { useContext } from "react";

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (context === null) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}
