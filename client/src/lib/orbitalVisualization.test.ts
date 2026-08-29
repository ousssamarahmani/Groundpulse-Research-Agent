import { describe, expect, it } from "vitest";
import { buildOrbitalVisualizationModel } from "./orbitalVisualization";

describe("buildOrbitalVisualizationModel", () => {
  it("shows derived orbital values and retrieval freshness", () => {
    const model = buildOrbitalVisualizationModel({ meanMotion: 15.5, orbitalPeriodMinutes: 92.9, retrievedAt: "2026-08-29T00:00:00.000Z" }, Date.parse("2026-08-29T00:04:00.000Z"));
    expect(model.available).toBe(true);
    expect(model.periodLabel).toBe("92.90 min cycle");
    expect(model.meanMotionLabel).toBe("15.50 rev/day");
    expect(model.freshnessLabel).toBe("4 min old");
  });

  it("does not invent values before a source arrives", () => {
    const model = buildOrbitalVisualizationModel();
    expect(model.available).toBe(false);
    expect(model.periodLabel).toBe("cycle unavailable");
    expect(model.freshnessLabel).toBe("Awaiting source");
  });
});
