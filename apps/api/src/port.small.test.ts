import { describe, expect, it } from "vitest";
import { parsePort } from "./port";

describe("parsePort", () => {
  it("returns the default port when the value is undefined", () => {
    expect(parsePort(undefined)).toBe(8787);
  });

  it("returns the parsed integer for a valid port string", () => {
    expect(parsePort("3000")).toBe(3000);
  });

  it("throws an error naming PORT when the value is not a number", () => {
    expect(() => parsePort("not-a-number")).toThrow(/PORT/);
  });

  it("throws an error naming PORT when the value is above 65535", () => {
    expect(() => parsePort("70000")).toThrow(/PORT/);
  });

  it("throws an error naming PORT when the value is below 1", () => {
    expect(() => parsePort("0")).toThrow(/PORT/);
  });
});
