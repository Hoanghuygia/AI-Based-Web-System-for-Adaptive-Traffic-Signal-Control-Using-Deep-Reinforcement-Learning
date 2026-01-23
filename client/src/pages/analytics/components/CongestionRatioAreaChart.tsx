import { Card } from "antd";
import { memo, useMemo } from "react";
import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    ResponsiveContainer,
    Tooltip,
} from "recharts";

interface Props {
    loading?: boolean;
}

// Generate mock data for congestion ratio over time (24 hours)
const generateCongestionRatioData = () => {
    const data = [];

    for (let hour = 0; hour < 24; hour++) {
        let ratio;

        // Simulate traffic patterns throughout the day
        if (hour >= 7 && hour <= 9) {
            // Morning rush hour
            ratio = Math.floor(Math.random() * 15 + 40); // 40-55%
        } else if (hour >= 17 && hour <= 19) {
            // Evening rush hour
            ratio = Math.floor(Math.random() * 15 + 45); // 45-60%
        } else if (hour >= 22 || hour <= 5) {
            // Night time
            ratio = Math.floor(Math.random() * 10 + 2); // 2-12%
        } else {
            // Normal hours
            ratio = Math.floor(Math.random() * 20 + 20); // 20-40%
        }

        data.push({
            time: `${hour.toString().padStart(2, "0")}:00`,
            ratio,
        });
    }

    return data;
};

function CongestionRatioAreaChart({ loading = false }: Props) {
    const congestionRatioData = useMemo(
        () => generateCongestionRatioData(),
        [],
    );

    return (
        <Card
            title="Congestion Ratio Over Time"
            loading={loading}
            className="shadow-sm"
        >
            <ResponsiveContainer width="100%" height={300}>
                <AreaChart
                    data={congestionRatioData}
                    margin={{
                        top: 10,
                        right: 30,
                        left: 0,
                        bottom: 0,
                    }}
                >
                    <defs>
                        <linearGradient
                            id="colorRatio"
                            x1="0"
                            y1="0"
                            x2="0"
                            y2="1"
                        >
                            <stop
                                offset="5%"
                                stopColor="#8b5cf6"
                                stopOpacity={0.8}
                            />
                            <stop
                                offset="95%"
                                stopColor="#8b5cf6"
                                stopOpacity={0.1}
                            />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="time" tick={{ fontSize: 12 }} interval={2} />
                    <YAxis
                        tick={{ fontSize: 12 }}
                        label={{
                            value: "Congestion %",
                            angle: -90,
                            position: "insideLeft",
                        }}
                    />
                    <Tooltip
                        formatter={(value) => [`${value}%`, "Congestion Ratio"]}
                        labelFormatter={(label) => `Time: ${label}`}
                    />
                    <Area
                        type="monotone"
                        dataKey="ratio"
                        stroke="#8b5cf6"
                        strokeWidth={2}
                        fillOpacity={1}
                        fill="url(#colorRatio)"
                    />
                </AreaChart>
            </ResponsiveContainer>
        </Card>
    );
}

export default memo(CongestionRatioAreaChart);
