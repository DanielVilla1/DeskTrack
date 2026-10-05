import { createBrowserRouter } from "react-router-dom";

import AppShell from "./AppShell";
import HomePage from "./HomePage";
import ProtectedRoute from "./ProtectedRoute";
import SignInPage from "./SignInPage";
import SignUpPage from "./SignUpPage";

// The trailing /* lets Clerk handle its own sub-steps, such as email verification.
export const router = createBrowserRouter([
  { path: "/sign-in/*", element: <SignInPage /> },
  { path: "/sign-up/*", element: <SignUpPage /> },
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppShell />,
        children: [{ index: true, element: <HomePage /> }],
      },
    ],
  },
]);
