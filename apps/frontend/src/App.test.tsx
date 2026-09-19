import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { App } from "./App";

describe("App", () => {
  it("renders the Kotogumo heading on the top page", () => {
    render(<App />);

    expect(
      screen.getByRole("heading", { name: "Kotogumo" }),
    ).toBeInTheDocument();
  });
});
