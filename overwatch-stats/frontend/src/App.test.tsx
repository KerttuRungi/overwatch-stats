import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import App from "./App";

beforeEach(() => {
  vi.stubGlobal(
    "fetch",
    vi.fn(() => Promise.resolve(new Response("[]", { status: 200 }))),
  );
});

afterEach(() => {
  vi.unstubAllGlobals();
});

// Rendering throws on runtime errors such as "Invalid hook call",
// which a type-check/bundle build cannot detect.
it.each(["/", "/compare"])("renders %s without crashing", (path) => {
  const { container } = render(
    <MemoryRouter initialEntries={[path]}>
      <App />
    </MemoryRouter>,
  );
  expect(container).toBeTruthy();
});
