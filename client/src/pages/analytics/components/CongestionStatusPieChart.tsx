import { Card } from "antd";
import { memo, useMemo } from "react";
import {
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    Legend,
    Tooltip,
} from "recharts";

interface Props {
    loading?: boolean;
}

// Generate mock data for congestion status distribution
const generateCongestionStatusData = () => {
    return [
        { name: "Normal", value: 45, color: "#10b981" }, // green-500
        { name: "Moderate", value: 30, color: "#f59e0b" }, // amber-500
        { name: "Congested", value: 25, color: "#ef4444" }, // red-500
    ];
};

function CongestionStatusPieChart({ loading = false }: Props) {
    const congestionStatusData = useMemo(
        () => generateCongestionStatusData(),
        [],
    );

    // Custom label for pie chart
    const renderCustomLabel = (entry: any) => {
        return `${entry.name}: ${entry.value}%`;
    };

    return (
        <Card
            title="Congestion Status Distribution"
            loading={loading}
            className="shadow-sm"
        >
            <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                    <Pie
                        data={congestionStatusData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={renderCustomLabel}
                        outerRadius={100}
                        fill="#8884d8"
                        dataKey="value"
                    >
                        {congestionStatusData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                    </Pie>
                    <Tooltip formatter={(value) => `${value}%`} />
                    <Legend
                        iconType="circle"
                        formatter={(value, entry: any) => (
                            <span style={{ color: entry.color }}>
                                {value}: {entry.payload.value}%
                            </span>
                        )}
                    />
                </PieChart>
            </ResponsiveContainer>
        </Card>
    );
}

export default memo(CongestionStatusPieChart);
