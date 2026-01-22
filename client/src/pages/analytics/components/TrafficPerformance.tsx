import { Card } from 'antd';
import { memo, useMemo } from 'react';
import LineChartWithBrush from '@src/components/charts/LineChartWithBrush';
import BarChartSimple from '@src/components/charts/BarChartSimple';

// Generate mock data for traffic flow over 24 hours
const generateTrafficFlowData = () => {
  const data = [];
  const now = new Date();

  for (let i = 23; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 60 * 60 * 1000);
    const hour = time.getHours();

    // Simulate traffic patterns
    let vehicles;
    if (hour >= 7 && hour <= 9) {
      vehicles = Math.floor(Math.random() * 200 + 600); // Morning rush: 600-800
    } else if (hour >= 17 && hour <= 19) {
      vehicles = Math.floor(Math.random() * 200 + 650); // Evening rush: 650-850
    } else if (hour >= 22 || hour <= 5) {
      vehicles = Math.floor(Math.random() * 100 + 50); // Night: 50-150
    } else {
      vehicles = Math.floor(Math.random() * 200 + 350); // Normal: 350-550
    }

    data.push({
      time: `${hour.toString().padStart(2, '0')}:00`,
      vehicles,
    });
  }

  return data;
};

// Generate mock data for waiting time by junction
const generateWaitingTimeData = () => {
  return [
    { name: 'Junction 1', waitTime: Math.floor(Math.random() * 20 + 35) },
    { name: 'Junction 2', waitTime: Math.floor(Math.random() * 15 + 25) },
    { name: 'Junction 3', waitTime: Math.floor(Math.random() * 15 + 20) },
    { name: 'Junction 4', waitTime: Math.floor(Math.random() * 25 + 50) },
    { name: 'Junction 5', waitTime: Math.floor(Math.random() * 20 + 30) },
  ];
};

function TrafficPerformance() {
  const trafficFlowData = useMemo(() => generateTrafficFlowData(), []);
  const waitingTimeData = useMemo(() => generateWaitingTimeData(), []);

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Traffic Performance
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Traffic Flow Over Time Chart */}
        <Card className="shadow-sm">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Traffic Flow Over Time (Last 24h)
          </h3>

          <LineChartWithBrush
            data={trafficFlowData}
            dataKeyX="time"
            dataKeyY="vehicles"
            height={256}
            showNavigation={true}
            initialWindowSize={12}
            lineColor="#c084fc"
            fillColor="#f3e8ff"
            formatTooltip={(value) => `${value} vehicles`}
          />
        </Card>

        {/* Average Waiting Time by Junction Chart */}
        <Card className="shadow-sm">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Average Waiting Time by Junction
          </h3>

          <BarChartSimple
            data={waitingTimeData}
            dataKeyX="name"
            dataKeyY="waitTime"
            yDomain={[0, 80]}
            unit="s"
            height={256}
            barColor="#c084fc"
            showStats={true}
            formatTooltip={(value) => `${value}s`}
          />
        </Card>
      </div>
    </div>
  );
}

export default memo(TrafficPerformance);
