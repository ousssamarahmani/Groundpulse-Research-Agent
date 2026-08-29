import { describe, expect, it } from "vitest";
import { buildResearchPackageHtml } from "./researchPackage";

describe("buildResearchPackageHtml", () => {
  it("includes live orbital evidence and engineering review sections", () => {
    const html = buildResearchPackageHtml({
      runId: "LIVE-CELESTRAK-25544",
      generatedAt: "2026-08-29T00:00:00.000Z",
      audience: "CubeSat analyst",
      scenario: "Orbit readiness check",
      record: { objectName: "ISS (ZARYA)", epoch: "2026-08-28T12:00:00.000Z", orbitalPeriodMinutes: 92.93 },
    });

    expect(html).toContain("LIVE-CELESTRAK-25544");
    expect(html).toContain("CubeSat analyst");
    expect(html).toContain("Orbit readiness check");
    expect(html).toContain("ADCS / GNC");
    expect(html).toContain("Communications");
    expect(html).toContain("CelesTrak GP data formats");
    expect(html).toContain("92.93 minutes");
  });

  it("does not present missing source fields as live evidence", () => {
    const html = buildResearchPackageHtml({ runId: "RUN-DEMO", generatedAt: "2026-08-29T00:00:00.000Z" });

    expect(html).toContain("Evidence-first review");
    expect(html).toContain("Selected satellite (awaiting source)");
    expect(html).toContain("Not available until CelesTrak responds");
    expect(html).toContain("Visible gap:");
  });
});
