import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { useMemo } from 'react';

export interface BarChartDataPoint {
  [key: string]: string | number;
}

export interface BarChartSimpleProps {
  data: BarChartDataPoint[];
  dataKeyX: string;
  dataKeyY: string;
  yDomain?: [number | string, number | string];
  unit?: string;
  height?: number;
  barColor?: string;
  showStats?: boolean;
  formatTooltip?: (value: number) => string;
}

export default function BarChartSimple({
  data,
  dataKeyX,
  dataKeyY,
  yDomain = [0, 'auto'],
  unit = '',
  height = 320,
  barColor = '#c084fc',
  showStats = true,
  formatTooltip,
}: BarChartSimpleProps) {
  // Calculate stats
  const stats = useMemo(() => {
    const values = data.map((d) => Number(d[dataKeyY]));
    const avg = Math.round(values.reduce((a, b) => a + b, 0) / values.length);
    const max = Math.max(...values);
    const maxItem = data.find((d) => Number(d[dataKeyY]) === max);

    return { avg, max, maxItem };
  }, [data, dataKeyY]);

  const tooltipFormatter = (value: number) => {
    if (formatTooltip) {
      return formatTooltip(value);
    }
    return `${value}${unit}`;
  };

  return (
    <div>
      {/* Chart header with stats */}
      {showStats && (
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs text-gray-600">{data.length} data points</span>
          <span className="text-xs text-gray-500">
            Highest: {stats.maxItem?.[dataKeyX]} ({stats.max}{unit})
          </span>
        </div>
      )}

      {/* Chart */}
      <div style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
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
          </BarChart>
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
