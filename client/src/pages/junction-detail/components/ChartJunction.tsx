import { useMemo } from 'react';
import LineChartWithBrush from '@src/components/charts/LineChartWithBrush';

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
        });
    }
    
    return data;
};

export default function ChartJunction() {
    const mockData = useMemo(() => generateMockData(), []);

    return (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">
                Daily Traffic Pattern
            </h2>

            <LineChartWithBrush
                data={mockData}
                dataKeyX="time"
                dataKeyY="traffic"
                yLabel="Traffic %"
                yDomain={[0, 100]}
                unit="%"
                height={320}
                showNavigation={true}
                initialWindowSize={12}
                lineColor="#c084fc"
                fillColor="#c084fc"
                formatTooltip={(value) => `${value}%`}
            />
        </div>
    );
}
