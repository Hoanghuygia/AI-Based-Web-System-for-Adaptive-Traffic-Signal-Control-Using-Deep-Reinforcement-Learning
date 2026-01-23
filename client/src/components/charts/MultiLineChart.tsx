import { Button } from 'antd';
import { useState, useMemo } from 'react';
import { PlusOutlined, CloseOutlined } from '@ant-design/icons';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Brush,
  Legend,
} from 'recharts';

export interface JunctionData {
  junctionId: number;
  data: Array<{ [key: string]: string | number }>;
}

export interface MultiLineChartProps {
  junctionData: JunctionData[];
  dataKeyX: string;
  dataKeyY: string;
  height?: number;
  showNavigation?: boolean;
  initialWindowSize?: number;
  selectedJunctions: number[];
  onAddJunction: () => void;
  onRemoveJunction: (junctionId: number) => void;
}

const JUNCTION_COLORS = [
  '#8b5cf6', // purple
  '#ec4899', // pink
  '#f59e0b', // orange
  '#10b981', // green
  '#3b82f6', // blue
  '#ef4444', // red
  '#06b6d4', // cyan
  '#84cc16', // lime
  '#f97316', // orange-red
  '#6366f1', // indigo
];

export default function MultiLineChart({
  junctionData,
  dataKeyX,
  dataKeyY,
  height = 320,
  showNavigation = true,
  initialWindowSize = 12,
  selectedJunctions,
  onAddJunction,
  onRemoveJunction,
}: MultiLineChartProps) {
  const [brushRange, setBrushRange] = useState({
    startIndex: Math.max(0, (junctionData[0]?.data.length || 0) - initialWindowSize),
    endIndex: (junctionData[0]?.data.length || 0) - 1,
  });

  // Merge all junction data into one dataset
  const mergedData = useMemo(() => {
    if (junctionData.length === 0) return [];

    const timePoints = junctionData[0].data.map((d) => d[dataKeyX]);
    
    return timePoints.map((time, index) => {
      const dataPoint: any = { [dataKeyX]: time };
      
      junctionData.forEach(({ junctionId, data }) => {
        dataPoint[`junction${junctionId}`] = data[index]?.[dataKeyY] || 0;
      });
      
      return dataPoint;
    });
  }, [junctionData, dataKeyX, dataKeyY]);

  const visibleData = mergedData.slice(brushRange.startIndex, brushRange.endIndex + 1);

  const handlePrevious = () => {
    const windowSize = brushRange.endIndex - brushRange.startIndex;
    const newStartIndex = Math.max(0, brushRange.startIndex - 1);
    setBrushRange({
      startIndex: newStartIndex,
      endIndex: Math.min(mergedData.length - 1, newStartIndex + windowSize),
    });
  };

  const handleNext = () => {
    const windowSize = brushRange.endIndex - brushRange.startIndex;
    const newEndIndex = Math.min(mergedData.length - 1, brushRange.endIndex + 1);
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
    <div>
      {/* Junction selector buttons */}
      <div className="flex items-center gap-2 mb-3 flex-wrap">
        {selectedJunctions.map((junctionId) => (
          <Button
            key={junctionId}
            size="small"
            style={{
              borderColor: JUNCTION_COLORS[(junctionId - 1) % JUNCTION_COLORS.length],
              color: JUNCTION_COLORS[(junctionId - 1) % JUNCTION_COLORS.length],
            }}
            className="flex items-center gap-1"
            icon={
              selectedJunctions.length > 1 ? (
                <CloseOutlined
                  onClick={(e) => {
                    e.stopPropagation();
                    onRemoveJunction(junctionId);
                  }}
                />
              ) : undefined
            }
          >
            Junction {junctionId}
          </Button>
        ))}
        {selectedJunctions.length < 4 && (
          <Button
            type="dashed"
            size="small"
            icon={<PlusOutlined />}
            onClick={onAddJunction}
            disabled={selectedJunctions.length >= 4}
            className="flex items-center gap-1"
          >
            Add Junction
          </Button>
        )}
      </div>

      {/* Chart header with stats */}
      {showNavigation && (
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs text-gray-600">
            Window: {visibleData.length} data points
          </span>
          <span className="text-xs text-gray-500">
            Showing {selectedJunctions.length} junction(s)
          </span>
        </div>
      )}

      {/* Navigation buttons */}
      {showNavigation && (
        <div className="flex items-center justify-center gap-2 mb-3">
          <Button
            onClick={handlePrevious}
            disabled={brushRange.startIndex === 0}
            size="small"
            className="!bg-purple-400 text-white rounded disabled:!bg-gray-300 disabled:cursor-not-allowed hover:!bg-purple-500 !border-purple-400"
          >
            ← Prev
          </Button>
          <span className="text-xs text-gray-600">
            {visibleData[0]?.[dataKeyX]} - {visibleData[visibleData.length - 1]?.[dataKeyX]}
          </span>
          <Button
            onClick={handleNext}
            disabled={brushRange.endIndex >= mergedData.length - 1}
            size="small"
            className="!bg-purple-400 text-white rounded disabled:!bg-gray-300 disabled:cursor-not-allowed hover:!bg-purple-500 !border-purple-400"
          >
            Next →
          </Button>
        </div>
      )}

      {/* Chart */}
      <div style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={mergedData}
            margin={{ top: 5, right: 20, left: 0, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey={dataKeyX} tick={{ fontSize: 11 }} stroke="#6b7280" />
            <YAxis tick={{ fontSize: 11 }} stroke="#6b7280" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#fff',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                padding: '8px',
              }}
              formatter={(value: number | string | undefined, name: string | undefined) => {
                if (!name) return ['N/A', ''];
                const junctionId = name.replace('junction', '');
                return [
                  value !== undefined ? `${value} vehicles` : 'N/A',
                  `Junction ${junctionId}`,
                ];
              }}
            />
            <Legend
              verticalAlign="bottom"
              height={36}
              formatter={(value) => `Junction ${value.replace('junction', '')}`}
            />
            {selectedJunctions.map((junctionId) => (
              <Line
                key={junctionId}
                type="monotone"
                dataKey={`junction${junctionId}`}
                stroke={JUNCTION_COLORS[(junctionId - 1) % JUNCTION_COLORS.length]}
                strokeWidth={2}
                dot={{ r: 3 }}
                activeDot={{ r: 5 }}
              />
            ))}
            <Brush
              dataKey={dataKeyX}
              height={30}
              stroke="#c084fc"
              fill="#f3e8ff"
              startIndex={brushRange.startIndex}
              endIndex={brushRange.endIndex}
              onChange={handleBrushChange}
              travellerWidth={10}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
