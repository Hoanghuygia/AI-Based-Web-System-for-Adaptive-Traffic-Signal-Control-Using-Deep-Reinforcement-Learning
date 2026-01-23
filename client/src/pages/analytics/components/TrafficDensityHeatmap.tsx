import { Card } from "antd";
import { memo, useMemo } from "react";
import SingleLegend from "./SIngleLegend";

interface Props {
    loading?: boolean;
}

// Generate mock data for traffic density heatmap
const generateTrafficDensityHeatmapData = () => {
    const junctions = ["J1", "J2", "J3", "J4", "J5", "J6", "J7", "J8"];
    const timeSlots = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"];
    const data: Array<{
        junction: string;
        time: string;
        density: number;
    }> = [];

    junctions.forEach((junction, jIndex) => {
        timeSlots.forEach((time) => {
            let density;
            const hour = parseInt(time.split(":")[0]);

            // Simulate different patterns for different junctions
            const junctionFactor = 0.7 + jIndex * 0.05;

            if (hour >= 7 && hour <= 9) {
                // Morning rush
                density = Math.floor(
                    (Math.random() * 20 + 70) * junctionFactor,
                );
            } else if (hour >= 16 && hour <= 20) {
                // Evening rush
                density = Math.floor(
                    (Math.random() * 25 + 75) * junctionFactor,
                );
            } else if (hour >= 0 && hour <= 4) {
                // Night
                density = Math.floor(
                    (Math.random() * 15 + 10) * junctionFactor,
                );
            } else {
                // Normal
                density = Math.floor(
                    (Math.random() * 30 + 40) * junctionFactor,
                );
            }

            data.push({
                junction,
                time,
                density: Math.min(100, density),
            });
        });
    });

    return data;
};

// Get color based on density value
const getDensityColor = (density: number): string => {
    if (density >= 80) return "#7c3aed"; // purple-600 - Very High
    if (density >= 60) return "#a78bfa"; // purple-400 - High
    if (density >= 40) return "#c4b5fd"; // purple-300 - Medium
    if (density >= 20) return "#ddd6fe"; // purple-200 - Low
    return "#ede9fe"; // purple-100 - Very Low
};

function TrafficDensityHeatmap({ loading = false }: Props) {
    const heatmapData = useMemo(() => generateTrafficDensityHeatmapData(), []);

    return (
        <Card
            title="Traffic Density Heatmap"
            loading={loading}
            className="shadow-sm"
        >
            <div className="overflow-x-auto">
                <div className="min-w-[600px]">
                    {/* Legend */}
                    <div className="flex items-center justify-end gap-4 mb-4 text-sm">
                        <span className="text-gray-600">Density:</span>
                        <SingleLegend color="#ede9fe" label="Low" />
                        <SingleLegend color="#ddd6fe" label="Moderate" />
                        <SingleLegend color="#c4b5fd" label="Medium" />
                        <SingleLegend color="#a78bfa" label="High" />
                        <SingleLegend color="#7c3aed" label="Very High" />
                    </div>

                    {/* Heatmap Grid */}
                    <div className="border border-gray-200 rounded-lg overflow-hidden">
                        {/* Header Row */}

                        <div className="grid grid-cols-[100px_repeat(6,1fr)] bg-gray-50 border-b border-gray-200">
                            <div className="p-3 font-semibold text-gray-700 border-r border-gray-200">
                                Junction
                            </div>
                            {["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"].map(
                                (time) => (
                                    <div
                                        key={time}
                                        className="p-3 text-center font-semibold text-gray-700 border-r border-gray-200 last:border-r-0"
                                    >
                                        {time}
                                    </div>
                                ),
                            )}
                        </div>

                        {/* Data Rows */}
                        {["J1", "J2", "J3", "J4", "J5", "J6", "J7", "J8"].map(
                            (junction) => (
                                <div
                                    key={junction}
                                    className="grid grid-cols-[100px_repeat(6,1fr)] border-b border-gray-200 last:border-b-0"
                                >
                                    <div className="p-3 font-medium text-gray-700 bg-gray-50 border-r border-gray-200 flex items-center">
                                        {junction}
                                    </div>
                                    {[
                                        "00:00",
                                        "04:00",
                                        "08:00",
                                        "12:00",
                                        "16:00",
                                        "20:00",
                                    ].map((time) => {
                                        const cell = heatmapData.find(
                                            (d) =>
                                                d.junction === junction &&
                                                d.time === time,
                                        );
                                        const density = cell?.density || 0;
                                        const color = getDensityColor(density);

                                        return (
                                            <div
                                                key={`${junction}-${time}`}
                                                className="p-3 text-center border-r border-gray-200 last:border-r-0 transition-all hover:opacity-80 cursor-pointer"
                                                style={{
                                                    backgroundColor: color,
                                                }}
                                                title={`${junction} at ${time}: ${density}% density`}
                                            >
                                                <span className="text-sm font-medium text-gray-800">
                                                    {density}%
                                                </span>
                                            </div>
                                        );
                                    })}
                                </div>
                            ),
                        )}
                    </div>
                </div>
            </div>
        </Card>
    );
}

export default memo(TrafficDensityHeatmap);
