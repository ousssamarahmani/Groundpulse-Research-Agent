import { describe, expect, it } from "vitest";
import { profileScenarios, type Audience } from "./researchScenarios";

describe("role-specific research scenarios", () => {
  it.each<[Audience, string]>([
    ["CubeSat analyst", "Orbit readiness check"],
    ["Satellite engineer", "Subsystem evidence map"],
    ["Space researcher", "Source landscape"],
  ])("provides a useful default scenario for %s", (audience, expectedLabel) => {
    const scenario = profileScenarios[audience][0];
    expect(scenario.label).toBe(expectedLabel);
    expect(scenario.question.length).toBeGreaterThan(100);
    expect(scenario.output.length).toBeGreaterThan(30);
    expect(scenario.nextAction.length).toBeGreaterThan(15);
    expect(scenario.interpretation).toMatch(/evidence|source|orbit/i);
  });

  it("keeps scenario IDs distinct between roles", () => {
    const ids = Object.values(profileScenarios).flat().map((scenario) => scenario.id);
    expect(new Set(ids).size).toBe(ids.length);
  });
});
