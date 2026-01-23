import { Alert, Button, Spin } from "antd";
import { ReloadOutlined } from "@ant-design/icons";
import GlobalKPIOverview from "./components/GlobalKPIOverview";
import TrafficPerformance from "./components/TrafficPerformance";
import CongestionDensityAnalysis from "./components/CongestionDensityAnalysis";
import { useAnalytics } from "./hooks/useAnalytics";

export default function Analytics() {
    const { analytics, isLoading, error, refreshAnalytics } = useAnalytics();

    return (
        <div className="bg-white p-6 min-h-screen">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900 mb-1">
                        Analytics Dashboard
                    </h1>
                    <p className="text-sm text-gray-500">
                        Real-time traffic analytics and performance metrics
                    </p>
                </div>
                <Button
                    icon={<ReloadOutlined />}
                    onClick={refreshAnalytics}
                    loading={isLoading}
                    type="default"
                >
                    Refresh
                </Button>
            </div>

            {/* Error Alert */}
            {error && (
                <Alert
                    message="Error"
                    description={error}
                    type="error"
                    closable
                    className="mb-6"
                />
            )}

            {/* Loading State for Initial Load */}
            {isLoading && !analytics ? (
                <div className="flex items-center justify-center min-h-[400px]">
                    <Spin size="large" />
                </div>
            ) : (
                <>
                    {/* Global KPI Overview */}
                    <GlobalKPIOverview
                        data={analytics.globalKPI}
                        loading={isLoading}
                    />

                    {/* Traffic Performance */}
                    <TrafficPerformance />

                    {/* Congestion & Density Analysis */}
                    <CongestionDensityAnalysis loading={isLoading} />

                    {/* Placeholder for other sections */}
                    {/* <div className="grid grid-cols-1 gap-6 mt-6">
                        <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                            <p className="text-gray-500">Junction-Level Analysis - Coming Soon</p>
                        </div>
                        <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                            <p className="text-gray-500">Temporal & AI Control Analysis - Coming Soon</p>
                        </div>
                    </div> */}
                </>
            )}
        </div>
    );
}