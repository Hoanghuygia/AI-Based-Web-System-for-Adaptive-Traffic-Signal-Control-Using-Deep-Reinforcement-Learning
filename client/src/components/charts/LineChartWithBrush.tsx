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

export interface LineChartDataPoint {
  [key: string]: string | number;
}

export interface LineChartWithBrushProps {
  data: LineChartDataPoint[];
  dataKeyX: string;
  dataKeyY: string;
  yLabel?: string;
  yDomain?: [number | string, number | string];
  unit?: string;
  height?: number;
  showNavigation?: boolean;
  initialWindowSize?: number;
  lineColor?: string;
  fillColor?: string;
  formatTooltip?: (value: number) => string;
}

export default function LineChartWithBrush({
  data,
  dataKeyX,
  dataKeyY,
  yLabel,
  yDomain = [0, 'auto'],
  unit = '',
  height = 320,
  showNavigation = true,
  initialWindowSize = 12,
  lineColor = '#c084fc',
  fillColor = '#f3e8ff',
  formatTooltip,
}: LineChartWithBrushProps) {
  const [brushRange, setBrushRange] = useState({
    startIndex: Math.max(0, data.length - initialWindowSize),
    endIndex: data.length - 1,
  });

  const visibleData = data.slice(brushRange.startIndex, brushRange.endIndex + 1);

  // Calculate stats for visible data
  const stats = useMemo(() => {
    const values = visibleData.map((d) => Number(d[dataKeyY]));
    const avg = Math.round(values.reduce((a, b) => a + b, 0) / values.length);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const current = values[values.length - 1];
    const peakItem = visibleData.reduce((prev, curr) =>
      Number(prev[dataKeyY]) > Number(curr[dataKeyY]) ? prev : curr
    );

    return { avg, min, max, current, peak: peakItem };
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
      {/* Chart header with stats */}
      {showNavigation && (
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs text-gray-600">
            Window: {visibleData.length} data points
          </span>
          <span className="text-xs text-gray-500">
            Peak: {stats.peak[dataKeyY]}{unit} at {stats.peak[dataKeyX]}
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
          <LineChart
            data={data}
            margin={{ top: 5, right: 20, left: 0, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey={dataKeyX} tick={{ fontSize: 11 }} stroke="#6b7280" />
            <YAxis
              tick={{ fontSize: 11 }}
              stroke="#6b7280"
              label={yLabel ? { value: yLabel, angle: -90, position: 'insideLeft' } : undefined}
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
            <Line
              type="monotone"
              dataKey={dataKeyY}
              stroke={lineColor}
              strokeWidth={2}
              dot={{ fill: lineColor, r: 3 }}
              activeDot={{ r: 5 }}
            />
            <Brush
              dataKey={dataKeyX}
              height={30}
              stroke={lineColor}
              fill={fillColor}
              startIndex={brushRange.startIndex}
              endIndex={brushRange.endIndex}
              onChange={handleBrushChange}
              travellerWidth={10}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-3 text-xs">
        <div>
          <span className="text-gray-600">Avg: </span>
          <span className="font-semibold text-gray-800">
            {stats.avg}{unit}
          </span>
        </div>
        <div>
          <span className="text-gray-600">Min: </span>
          <span className="font-semibold text-gray-800">
            {stats.min}{unit}
          </span>
        </div>
        <div>
          <span className="text-gray-600">Max: </span>
          <span className="font-semibold text-gray-800">
            {stats.max}{unit}
          </span>
        </div>
        <div>
          <span className="text-gray-600">Current: </span>
          <span className="font-semibold text-purple-600">
            {stats.current}{unit}
          </span>
        </div>
      </div>
    </div>
  );
}
