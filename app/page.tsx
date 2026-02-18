import Dashboard from "@/components/Dashboard";
import {
  calculateCoverageGaps,
  calculateRetailOpportunities,
  calculateRoiScores,
  computeDashboardMetrics
} from "@/lib/analytics";
import { loadCombinedDataset } from "@/lib/data";

export const dynamic = "force-static";

export default async function HomePage() {
  const data = await loadCombinedDataset();
  const metrics = computeDashboardMetrics(data);
  const coverageGaps = calculateCoverageGaps(data, 2);
  const retail = calculateRetailOpportunities(data);
  const roi = calculateRoiScores(coverageGaps, data);

  return (
    <Dashboard
      data={data}
      metrics={metrics}
      coverageGaps={coverageGaps}
      retailOpportunities={retail}
      roiTop={roi}
    />
  );
}
