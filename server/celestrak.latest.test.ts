import { afterEach, describe, expect, it, vi } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

const createContext = (): TrpcContext => ({
  user: null,
  req: {} as TrpcContext["req"],
  res: {} as TrpcContext["res"],
});

describe("celestrak.latest", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("normalizes a live GP/OMM record with retrieval metadata", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify([
      {
        OBJECT_NAME: "ISS (ZARYA)",
        OBJECT_ID: "1998-067A",
        EPOCH: "2026-08-27T12:44:14.404128",
        MEAN_MOTION: 15.49656235,
        NORAD_CAT_ID: 25544,
      },
    ]), { status: 200, headers: { "content-type": "application/json" } })));

    const result = await appRouter.createCaller(createContext()).celestrak.latest({ noradId: 25544 });

    expect(result.source).toBe("CelesTrak GP/OMM");
    expect(result.objectId).toBe("1998-067A");
    expect(result.noradId).toBe("25544");
    expect(result.epoch).toBe("2026-08-27T12:44:14.404128");
    expect(result.orbitalPeriodMinutes).toBeCloseTo(92.924, 2);
    expect(result.retrievedAt).toMatch(/^2026|^20/);
  });

  it("rejects malformed GP/OMM payloads", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify([{ OBJECT_NAME: "ISS" }]), { status: 200 })));

    await expect(appRouter.createCaller(createContext()).celestrak.latest({ noradId: 25544 })).rejects.toThrow("Invalid CelesTrak GP/OMM payload");
  });
});
