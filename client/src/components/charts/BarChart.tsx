import { Button, Select } from 'antd';
import { useState, useMemo } from 'react';
import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Brush,
} from 'recharts';

export interface BarChartDataPoint {
  [key: string]: string | number;
}

export interface BarChartProps {
  data: BarChartDataPoint[];
  dataKeyX: string;
  dataKeyY: string;
  yDomain?: [number | string, number | string];
  unit?: string;
  height?: number;
  barColor?: string;
  showStats?: boolean;
  showNavigation?: boolean;
  initialWindowSize?: number;
  formatTooltip?: (value: number) => string;
  availableJunctions?: number[];
  selectedJunctions?: number[];
  onJunctionChange?: (junctions: number[]) => void;
}

export default function BarChart({
  data,
  dataKeyX,
  dataKeyY,
  yDomain = [0, 'auto'],
  unit = '',
  height = 320,
  barColor = '#c084fc',
  showStats = true,
  showNavigation = true,
  initialWindowSize = 5,
  formatTooltip,
  availableJunctions = [],
  selectedJunctions = [],
  onJunctionChange,
}: BarChartProps) {
  const [brushRange, setBrushRange] = useState({
    startIndex: 0,
    endIndex: Math.min(initialWindowSize - 1, data.length - 1),
  });

  const visibleData = data.slice(brushRange.startIndex, brushRange.endIndex + 1);

  // Calculate stats for visible data
  const stats = useMemo(() => {
    const values = visibleData.map((d) => Number(d[dataKeyY]));
    const avg = Math.round(values.reduce((a, b) => a + b, 0) / values.length);
    const max = Math.max(...values);
    const maxItem = visibleData.find((d) => Number(d[dataKeyY]) === max);

    return { avg, max, maxItem };
  }, [visibleData, dataKeyY]);

  const handlePrevious = () => {
    const windowSize = brushRange.endIndex - brushRange.startIndex;
    const newStartIndex = Math.max(0, brushRange.startIndex - 1);
    setBrushRange({
      startIndex: newStartIndex,
      endIndex: Math.min(data.length - 1, newStartIndex + windowSize),
    });
  };

  const handleNext = () => {
    const windowSize = brushRange.endIndex - brushRange.startIndex;
    const newEndIndex = Math.min(data.length - 1, brushRange.endIndex + 1);
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

  const tooltipFormatter = (value: number) => {
    if (formatTooltip) {
      return formatTooltip(value);
    }
    return `${value}${unit}`;
  };

  return (
    <div>
      {/* Junction selector dropdown */}
      {onJunctionChange && availableJunctions.length > 0 && (
        <div className="mb-3">
          <Select
            mode="multiple"
            placeholder="Select junctions to display"
            value={selectedJunctions}
            onChange={onJunctionChange}
            style={{ width: '100%' }}
            options={availableJunctions.map((id) => ({
              label: `Junction ${id}`,
              value: id,
            }))}
            maxTagCount="responsive"
          />
        </div>
      )}

      {/* Chart header with stats */}
      {showStats && showNavigation && (
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs text-gray-600">
            Window: {visibleData.length} of {data.length} data points
          </span>
          <span className="text-xs text-gray-500">
            Highest: {stats.maxItem?.[dataKeyX]} ({stats.max}{unit})
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
            disabled={brushRange.endIndex >= data.length - 1}
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
          <RechartsBarChart 
            data={data} 
            margin={{ top: 5, right: 20, left: 0, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey={dataKeyX} tick={{ fontSize: 11 }} stroke="#6b7280" />
            <YAxis
              tick={{ fontSize: 11 }}
              stroke="#6b7280"
              domain={yDomain}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#fff',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                padding: '8px',
              }}
              formatter={(value: number | string | undefined) =>
                value !== undefined ? [tooltipFormatter(Number(value)), dataKeyY] : ['N/A', dataKeyY]
              }
            />
            <Bar dataKey={dataKeyY} fill={barColor} radius={[4, 4, 0, 0]} />
            {showNavigation && (
              <Brush
                dataKey={dataKeyX}
                height={30}
                stroke={barColor}
                fill="#f3e8ff"
                startIndex={brushRange.startIndex}
                endIndex={brushRange.endIndex}
                onChange={handleBrushChange}
                travellerWidth={10}
              />
            )}
          </RechartsBarChart>
        </ResponsiveContainer>
      </div>

      {/* Stats */}
      {showStats && (
        <div className="grid grid-cols-2 gap-3 mt-3 text-xs">
          <div>
            <span className="text-gray-600">Average: </span>
            <span className="font-semibold text-gray-800">
              {stats.avg}{unit}
            </span>
          </div>
          <div>
            <span className="text-gray-600">Highest: </span>
            <span className="font-semibold text-purple-600">
              {stats.max}{unit}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
