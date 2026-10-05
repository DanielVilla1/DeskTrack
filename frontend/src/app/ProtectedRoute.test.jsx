import { useAuth } from "@clerk/clerk-react";
import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import ProtectedRoute from "./ProtectedRoute";

vi.mock("@clerk/clerk-react", () => ({ useAuth: vi.fn() }));

function renderProtectedRoute() {
  render(
    <MemoryRouter initialEntries={["/"]}>
      <Routes>
        <Route path="/sign-in" element={<p>Sign-in page</p>} />
        <Route element={<ProtectedRoute />}>
          <Route index element={<p>Private page</p>} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

describe("ProtectedRoute", () => {
  it("shows the page to a signed-in user", () => {
    useAuth.mockReturnValue({ isLoaded: true, isSignedIn: true });

    renderProtectedRoute();

    expect(screen.getByText("Private page")).toBeTruthy();
  });

  it("redirects a signed-out user to the sign-in page", () => {
    useAuth.mockReturnValue({ isLoaded: true, isSignedIn: false });

    renderProtectedRoute();

    expect(screen.getByText("Sign-in page")).toBeTruthy();
    expect(screen.queryByText("Private page")).toBeNull();
  });

  it("shows nothing while Clerk is still loading", () => {
    useAuth.mockReturnValue({ isLoaded: false, isSignedIn: false });

    renderProtectedRoute();

    expect(screen.queryByText("Private page")).toBeNull();
    expect(screen.queryByText("Sign-in page")).toBeNull();
  });
});
