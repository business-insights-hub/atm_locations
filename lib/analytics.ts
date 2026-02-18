import { haversineDistanceKm } from "@/lib/geo";
import { isAtm, isRetail } from "@/lib/data";
import { CoverageGap, DashboardMetrics, LocationRecord, RetailOpportunity } from "@/lib/types";

export function computeDashboardMetrics(data: LocationRecord[]): DashboardMetrics {
  const atms = data.filter(isAtm);
  const bobAtms = atms.filter((row) => row.source === "Bank of Baku");

  const countsByBank = new Map<string, number>();
  for (const row of atms) {
    countsByBank.set(row.source, (countsByBank.get(row.source) ?? 0) + 1);
  }

  const [leaderName, leaderCount] = [...countsByBank.entries()].sort((a, b) => b[1] - a[1])[0] ?? ["N/A", 0];

  const totalAtmCount = atms.length;
  const bobAtmCount = bobAtms.length;
  const marketSharePct = totalAtmCount > 0 ? (bobAtmCount / totalAtmCount) * 100 : 0;

  return {
    bobAtmCount,
    totalAtmCount,
    marketSharePct,
    leaderName,
    leaderCount,
    gapToLeader: Math.max(0, leaderCount - bobAtmCount)
  };
}

export function calculateCoverageGaps(data: LocationRecord[], radiusKm = 2): CoverageGap[] {
  const atms = data.filter(isAtm);
  const bobAtms = atms.filter((row) => row.source === "Bank of Baku");
  const competitors = atms.filter((row) => row.source !== "Bank of Baku");

  if (!bobAtms.length) {
    return [];
  }

  const gaps: CoverageGap[] = [];

  for (const comp of competitors) {
    let minDistance = Infinity;

    for (const bob of bobAtms) {
      const d = haversineDistanceKm(comp.latitude, comp.longitude, bob.latitude, bob.longitude);
      if (d < minDistance) {
        minDistance = d;
      }
    }

    if (minDistance > radiusKm) {
      // Exclude self-comparison so density reflects true nearby competitor count.
      let density = 0;
      for (const other of competitors) {
        if (other === comp) {
          continue;
        }

        const d = haversineDistanceKm(comp.latitude, comp.longitude, other.latitude, other.longitude);
        if (d <= 1) {
          density += 1;
        }
      }

      gaps.push({
        latitude: comp.latitude,
        longitude: comp.longitude,
        source: comp.source,
        address: comp.address,
        distance_to_bob: minDistance,
        competitor_density: density
      });
    }
  }

  return gaps;
}

export function calculateRetailOpportunities(data: LocationRecord[]): RetailOpportunity[] {
  const atms = data.filter(isAtm);
  const bobAtms = atms.filter((row) => row.source === "Bank of Baku");
  const competitors = atms.filter((row) => row.source !== "Bank of Baku");
  const retailLocations = data.filter(isRetail);

  if (!bobAtms.length || !retailLocations.length) {
    return [];
  }

  const opportunities: RetailOpportunity[] = [];

  for (const retail of retailLocations) {
    let minDistanceToBob = Infinity;

    for (const bob of bobAtms) {
      const d = haversineDistanceKm(retail.latitude, retail.longitude, bob.latitude, bob.longitude);
      if (d < minDistanceToBob) {
        minDistanceToBob = d;
      }
    }

    if (minDistanceToBob <= 1) {
      continue;
    }

    let competitorDensity = 0;
    for (const comp of competitors) {
      const d = haversineDistanceKm(retail.latitude, retail.longitude, comp.latitude, comp.longitude);
      if (d <= 0.5) {
        competitorDensity += 1;
      }
    }

    const opportunityScore = (Math.min(minDistanceToBob, 10) / 10) * 50 + (Math.min(competitorDensity, 10) / 10) * 50;

    opportunities.push({
      source: retail.source,
      address: retail.address,
      latitude: retail.latitude,
      longitude: retail.longitude,
      distance_to_bob: minDistanceToBob,
      competitor_density: competitorDensity,
      opportunity_score: opportunityScore
    });
  }

  return opportunities.sort((a, b) => b.opportunity_score - a.opportunity_score);
}

export function calculateRoiScores(gaps: CoverageGap[], data: LocationRecord[]): CoverageGap[] {
  const retail = data.filter(isRetail);

  return gaps
    .map((gap) => {
      const gapScore = Math.min(gap.distance_to_bob / 10, 1) * 30;
      const demandScore = Math.min(gap.competitor_density / 10, 1) * 40;

      let nearestRetail = Infinity;
      for (const r of retail) {
        const d = haversineDistanceKm(gap.latitude, gap.longitude, r.latitude, r.longitude);
        if (d < nearestRetail) {
          nearestRetail = d;
        }
      }

      const retailScore = Number.isFinite(nearestRetail) ? Math.max(0, (2 - nearestRetail) / 2) * 30 : 0;
      const roiScore = gapScore + demandScore + retailScore;

      return {
        ...gap,
        roi_score: roiScore
      };
    })
    .sort((a, b) => (b.roi_score ?? 0) - (a.roi_score ?? 0));
}
