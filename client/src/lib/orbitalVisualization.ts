export type OrbitalVisualizationRecord = {
  meanMotion: number;
  orbitalPeriodMinutes: number;
  retrievedAt: string;
};

export function buildOrbitalVisualizationModel(record?: OrbitalVisualizationRecord, now = Date.now()) {
  if (!record) {
    return { available: false, periodLabel: "cycle unavailable", meanMotionLabel: "—", freshnessLabel: "Awaiting source", freshnessMinutes: null };
  }

  const freshnessMinutes = Math.max(0, Math.round((now - new Date(record.retrievedAt).getTime()) / 60000));
  return {
    available: true,
    periodLabel: `${record.orbitalPeriodMinutes.toFixed(2)} min cycle`,
    meanMotionLabel: `${record.meanMotion.toFixed(2)} rev/day`,
    freshnessLabel: freshnessMinutes < 1 ? "Retrieved just now" : `${freshnessMinutes} min old`,
    freshnessMinutes,
  };
}
