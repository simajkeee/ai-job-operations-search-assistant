import { useAuth } from "./useAuth.ts";
import { Navigate, Outlet } from "react-router-dom";

export function ProtectedRoute() {
  const { currentUser, initializationError, isInitializing } = useAuth();

  if (isInitializing) {
    return <p>Restoring session...</p>;
  }

  if (initializationError) {
    return <p>Could not restore the session. Please refresh the page.</p>;
  }

  if (currentUser === null) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
