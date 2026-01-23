import { Card, Button } from 'antd';
import { memo, useMemo, useState } from 'react';
import { SplitCellsOutlined } from '@ant-design/icons';
import LineChartWithBrush from '@src/components/charts/LineChartWithBrush';
import BarChart from '@src/components/charts/BarChart';
import MultiLineChart from '@src/components/charts/MultiLineChart';

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
    { name: 'Junction 1', waitTime: Math.floor(Math.random() * 20 + 35), junctionId: 1 },
    { name: 'Junction 2', waitTime: Math.floor(Math.random() * 15 + 25), junctionId: 2 },
    { name: 'Junction 3', waitTime: Math.floor(Math.random() * 15 + 20), junctionId: 3 },
    { name: 'Junction 4', waitTime: Math.floor(Math.random() * 25 + 50), junctionId: 4 },
    { name: 'Junction 5', waitTime: Math.floor(Math.random() * 20 + 30), junctionId: 5 },
    { name: 'Junction 6', waitTime: Math.floor(Math.random() * 18 + 28), junctionId: 6 },
    { name: 'Junction 7', waitTime: Math.floor(Math.random() * 22 + 32), junctionId: 7 },
    { name: 'Junction 8', waitTime: Math.floor(Math.random() * 25 + 40), junctionId: 8 },
  ];
};

// Generate mock data for junction traffic flow over 24 hours
const generateJunctionTrafficFlowData = (junctionId: number) => {
  const data = [];
  const now = new Date();

  for (let i = 23; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 60 * 60 * 1000);
    const hour = time.getHours();

    // Simulate traffic patterns with variation per junction
    let vehicles;
    const junctionMultiplier = 0.8 + (junctionId * 0.1); // Different traffic levels per junction
    
    if (hour >= 7 && hour <= 9) {
      vehicles = Math.floor((Math.random() * 100 + 200) * junctionMultiplier); // Morning rush
    } else if (hour >= 17 && hour <= 19) {
      vehicles = Math.floor((Math.random() * 100 + 220) * junctionMultiplier); // Evening rush
    } else if (hour >= 22 || hour <= 5) {
      vehicles = Math.floor((Math.random() * 30 + 20) * junctionMultiplier); // Night
    } else {
      vehicles = Math.floor((Math.random() * 80 + 120) * junctionMultiplier); // Normal
    }

    data.push({
      time: `${hour.toString().padStart(2, '0')}:00`,
      vehicles,
    });
  }

  return data;
};

function TrafficPerformance() {
  const [showByJunction, setShowByJunction] = useState(false);
  const [selectedJunctions, setSelectedJunctions] = useState<number[]>([1, 2, 4]);
  const [barChartJunctions, setBarChartJunctions] = useState<number[]>([]);
  
  const trafficFlowData = useMemo(() => generateTrafficFlowData(), []);
  const allWaitingTimeData = useMemo(() => generateWaitingTimeData(), []);
  const availableJunctions = useMemo(
    () => allWaitingTimeData.map((d) => d.junctionId),
    [allWaitingTimeData]
  );
  
  const filteredWaitingTimeData = useMemo(() => {
    if (barChartJunctions.length === 0) return allWaitingTimeData;
    return allWaitingTimeData.filter((d) => barChartJunctions.includes(d.junctionId));
  }, [allWaitingTimeData, barChartJunctions]);
  
  const junctionTrafficData = useMemo(() => {
    return selectedJunctions.map((junctionId) => ({
      junctionId,
      data: generateJunctionTrafficFlowData(junctionId),
    }));
  }, [selectedJunctions]);

  const handleToggleView = () => {
    setShowByJunction(!showByJunction);
  };

  const handleAddJunction = () => {
    if (selectedJunctions.length >= 4) return;
    
    const availableJunctions = [1, 2, 3, 4];
    const unusedJunctions = availableJunctions.filter(
      (id) => !selectedJunctions.includes(id)
    );
    if (unusedJunctions.length > 0) {
      setSelectedJunctions([...selectedJunctions, unusedJunctions[0]]);
    }
  };

  const handleRemoveJunction = (junctionId: number) => {
    if (selectedJunctions.length > 1) {
      setSelectedJunctions(selectedJunctions.filter((id) => id !== junctionId));
    }
  };

  const handleBarChartJunctionChange = (junctions: number[]) => {
    setBarChartJunctions(junctions);
  };

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Traffic Performance
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Traffic Flow Over Time Chart */}
        <Card className="shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">
              Junction Traffic Flow (Last 24h)
            </h3>
            <Button
              type="default"
              icon={<SplitCellsOutlined />}
              onClick={handleToggleView}
              className="flex items-center gap-1"
            >
              {showByJunction ? 'Show Total' : 'Show by Junction'}
            </Button>
          </div>

          {!showByJunction ? (
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
          ) : (
            <MultiLineChart
              junctionData={junctionTrafficData}
              dataKeyX="time"
              dataKeyY="vehicles"
              height={256}
              showNavigation={true}
              initialWindowSize={12}
              selectedJunctions={selectedJunctions}
              onAddJunction={handleAddJunction}
              onRemoveJunction={handleRemoveJunction}
            />
          )}
        </Card>

        {/* Average Waiting Time by Junction Chart */}
        <Card className="shadow-sm">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Average Waiting Time by Junction
          </h3>

          <BarChart
            data={filteredWaitingTimeData}
            dataKeyX="name"
            dataKeyY="waitTime"
            yDomain={[0, 80]}
            unit="s"
            height={256}
            barColor="#c084fc"
            showStats={true}
            showNavigation={true}
            initialWindowSize={5}
            formatTooltip={(value) => `${value}s`}
            availableJunctions={availableJunctions}
            selectedJunctions={barChartJunctions}
            onJunctionChange={handleBarChartJunctionChange}
          />
        </Card>
      </div>
    </div>
  );
}

export default memo(TrafficPerformance);
