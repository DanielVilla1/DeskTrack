import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import AppShell from "./AppShell";

vi.mock("@clerk/clerk-react", () => ({
  UserButton: () => <button type="button">Account menu</button>,
}));

describe("AppShell", () => {
  it("shows the app name, the account menu, and the page content", () => {
    render(
      <MemoryRouter>
        <Routes>
          <Route element={<AppShell />}>
            <Route index element={<p>Page content</p>} />
          </Route>
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByRole("heading", { name: "DeskTrack" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Account menu" })).toBeTruthy();
    expect(screen.getByText("Page content")).toBeTruthy();
  });
});
