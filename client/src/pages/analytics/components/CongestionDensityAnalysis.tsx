import { memo } from "react";
import CongestionStatusPieChart from "./CongestionStatusPieChart";
import CongestionRatioAreaChart from "./CongestionRatioAreaChart";
import TrafficDensityHeatmap from "./TrafficDensityHeatmap";

interface Props {
    loading?: boolean;
}

function CongestionDensityAnalysis({ loading = false }: Props) {
    return (
        <div className="mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Congestion & Density Analysis
            </h2>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <CongestionStatusPieChart loading={loading} />
                <CongestionRatioAreaChart loading={loading} />
            </div>

            <div className="mt-4">
                <TrafficDensityHeatmap loading={loading} />
            </div>
        </div>
    );
}

export default memo(CongestionDensityAnalysis);
