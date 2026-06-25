import { render, screen } from "@testing-library/react";
import Home from "./home";

test("renders the heading", () => {
  render(<Home />);
  expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent(
    "Portfolio Trajectory",
  );
});
