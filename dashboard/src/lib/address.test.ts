import { describe, expect, it } from "vitest";
import { displayAddress, isTronAddress, shortAddress } from "./address";

const USDT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t";

describe("addresses on the dashboard", () => {
  it("recognises TRON addresses", () => {
    expect(isTronAddress(USDT)).toBe(true);
    expect(isTronAddress("0x1234")).toBe(false);
    expect(isTronAddress(`${USDT}0`)).toBe(false);
  });

  it("shortens a wallet that has not been frozen", () => {
    expect(shortAddress(USDT)).toBe("T…Lj6t");
    expect(displayAddress(USDT, false)).toBe("T…Lj6t");
  });

  it("shows the full address only after a freeze", () => {
    expect(displayAddress(USDT, true)).toBe(USDT);
  });

  it("refuses anything that is not a TRON address", () => {
    expect(() => shortAddress("not-an-address")).toThrow();
  });
});
