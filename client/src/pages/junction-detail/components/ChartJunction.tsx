import { Button } from 'antd';
import { useState, useMemo } from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Brush,
} from 'recharts';

// Mock data: 24 hours of traffic data
const generateMockData = () => {
    const data = [];
    const now = new Date();
    
    for (let i = 23; i >= 0; i--) {
        const time = new Date(now.getTime() - i * 60 * 60 * 1000);
        const hour = time.getHours();
        
        // Simulate traffic patterns (higher during rush hours)
        let traffic;
        if (hour >= 7 && hour <= 9) {
            traffic = Math.floor(Math.random() * 30 + 60); // Morning rush: 60-90%
        } else if (hour >= 17 && hour <= 19) {
            traffic = Math.floor(Math.random() * 30 + 70); // Evening rush: 70-100%
        } else if (hour >= 22 || hour <= 5) {
            traffic = Math.floor(Math.random() * 20); // Night: 0-20%
        } else {
            traffic = Math.floor(Math.random() * 40 + 30); // Normal: 30-70%
        }
        
        data.push({
            time: `${hour.toString().padStart(2, '0')}:00`,
            traffic,
            fullTime: time.toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit',
                hour12: false 
            }),
        });
    }
    
    return data;
};

export default function ChartJunction() {
    const mockData = useMemo(() => generateMockData(), []);
    const [brushRange, setBrushRange] = useState<{ startIndex: number; endIndex: number }>({
        startIndex: 12,
        endIndex: 23,
    });
    
    // Get visible data based on brush range
    const visibleData = mockData.slice(brushRange.startIndex, brushRange.endIndex + 1);
    
    // Calculate stats for visible data
    const stats = useMemo(() => {
        const values = visibleData.map(d => d.traffic);
        const avg = Math.round(values.reduce((a, b) => a + b, 0) / values.length);
        const min = Math.min(...values);
        const max = Math.max(...values);
        const current = values[values.length - 1];
        const peakItem = visibleData.reduce((prev, curr) => 
            prev.traffic > curr.traffic ? prev : curr
        );
        
        return { avg, min, max, current, peak: peakItem };
    }, [visibleData]);

    const handlePrevious = () => {
        const windowSize = brushRange.endIndex - brushRange.startIndex;
        const newStartIndex = Math.max(0, brushRange.startIndex - 1);
        setBrushRange({
            startIndex: newStartIndex,
            endIndex: Math.min(mockData.length - 1, newStartIndex + windowSize),
        });
    };

    const handleNext = () => {
        const windowSize = brushRange.endIndex - brushRange.startIndex;
        const newEndIndex = Math.min(mockData.length - 1, brushRange.endIndex + 1);
        setBrushRange({
            startIndex: Math.max(0, newEndIndex - windowSize),
            endIndex: newEndIndex,
        });
    };

    const handleBrushChange = (range: { startIndex?: number; endIndex?: number }) => {
        if (range.startIndex !== undefined && range.endIndex !== undefined) {
            setBrushRange({
                startIndex: range.startIndex,
                endIndex: range.endIndex,
            });
        }
    };

    return (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">
                Daily Traffic Pattern
            </h2>

            {/* Chart header */}
            <div className="flex items-center justify-between mb-4">
                <span className="text-sm text-gray-600">
                    Traffic Volume (12 Hours Window)
                </span>
                <span className="text-sm text-gray-500">
                    Peak: {stats.peak.traffic}% at {stats.peak.time}
                </span>
            </div>

            {/* Navigation buttons */}
            <div className="flex items-center justify-center gap-2 mb-4">
                <Button
                    onClick={handlePrevious}
                    type="primary"
                    disabled={brushRange.startIndex === 0}
                    className="px-3 py-1 text-sm !bg-purple-400 text-white rounded disabled:bg-gray-300 disabled:cursor-not-allowed hover:!bg-purple-500 !border-purple-400 transition-colors"
                >
                    ← Previous
                </Button>
                <span className="text-sm text-gray-600">
                    Showing: {visibleData[0]?.time} - {visibleData[visibleData.length - 1]?.time}
                </span>
                <Button
                    onClick={handleNext}
                    disabled={brushRange.endIndex >= mockData.length - 1}
                    className="px-3 py-1 text-sm !bg-purple-400 text-white rounded disabled:bg-gray-300 disabled:cursor-not-allowed hover:!bg-purple-500 !border-purple-400 transition-colors"
                >
                    Next →
                </Button>
            </div>

            {/* Chart */}
            <div className="h-80 mb-4">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart
                        data={mockData}
                        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                        <XAxis 
                            dataKey="time" 
                            tick={{ fontSize: 12 }}
                            stroke="#6b7280"
                        />
                        <YAxis 
                            tick={{ fontSize: 12 }}
                            stroke="#6b7280"
                            label={{ value: 'Traffic %', angle: -90, position: 'insideLeft' }}
                            domain={[0, 100]}
                        />
                        <Tooltip 
                            contentStyle={{ 
                                backgroundColor: '#fff',
                                border: '1px solid #e5e7eb',
                                borderRadius: '8px',
                                padding: '8px'
                            }}
                            formatter={(value: number | undefined) => value !== undefined ? [`${value}%`, 'Traffic'] : ['N/A', 'Traffic']}
                        />
                        <Line 
                            type="monotone" 
                            dataKey="traffic" 
                            stroke="#c084fc" 
                            strokeWidth={2}
                            dot={{ fill: '#c084fc', r: 4 }}
                            activeDot={{ r: 6 }}
                        />
                        <Brush 
                            dataKey="time"
                            height={30}
                            stroke="#c084fc"
                            fill="#c084fc"
                            startIndex={brushRange.startIndex}
                            endIndex={brushRange.endIndex}
                            onChange={handleBrushChange}
                            travellerWidth={10}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                    <span className="text-gray-600">
                        Avg (12h):
                    </span>
                    <span className="font-semibold text-gray-800 ml-2">
                        {stats.avg}%
                    </span>
                </div>
                <div>
                    <span className="text-gray-600">
                        Min:
                    </span>
                    <span className="font-semibold text-gray-800 ml-2">
                        {stats.min}%
                    </span>
                </div>
                <div>
                    <span className="text-gray-600">
                        Max:
                    </span>
                    <span className="font-semibold text-gray-800 ml-2">
                        {stats.max}%
                    </span>
                </div>
                <div>
                    <span className="text-gray-600">
                        Current:
                    </span>
                    <span className="font-semibold text-purple-600 ml-2">
                        {stats.current}%
                    </span>
                </div>
            </div>
        </div>
    );
}
