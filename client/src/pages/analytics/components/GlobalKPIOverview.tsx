import { memo } from 'react';
import { GlobalKPIData } from '../types';
import KPICard from '@src/components/KPICard';
import {
  DatabaseOutlined,
  ThunderboltOutlined,
  WarningOutlined,
  ClockCircleOutlined,
  RiseOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons';

interface Props {
  data: GlobalKPIData;
  loading?: boolean;
}

function GlobalKPIOverview({ data, loading = false }: Props) {
  const getSystemHealthColor = (health: string) => {
    switch (health) {
      case 'Normal':
        return 'bg-green-100';
      case 'Warning':
        return 'bg-yellow-100';
      case 'Critical':
        return 'bg-red-100';
      default:
        return 'bg-gray-100';
    }
  };

  const formatThroughput = (value: number): string => {
    if (value >= 1000) {
      return `${(value / 1000).toFixed(1)}K`;
    }
    return value.toString();
  };

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Global KPI Overview
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <KPICard
          title="Total Junctions"
          value={data.totalJunctions}
          icon={<DatabaseOutlined />}
          iconBgColor="bg-blue-100"
          loading={loading}
        />

        <KPICard
          title="Active"
          value={data.activeJunctions}
          icon={<ThunderboltOutlined />}
          iconBgColor="bg-green-100"
          loading={loading}
        />

        <KPICard
          title="Avg Congestion"
          value={`${data.avgCongestion}%`}
          icon={<WarningOutlined />}
          iconBgColor="bg-orange-100"
          loading={loading}
        />

        <KPICard
          title="Avg Wait Time"
          value={`${data.avgWaitTime}s`}
          icon={<ClockCircleOutlined />}
          iconBgColor="bg-purple-100"
          loading={loading}
        />

        <KPICard
          title="Throughput"
          value={formatThroughput(data.throughput)}
          icon={<RiseOutlined />}
          iconBgColor="bg-cyan-100"
          loading={loading}
        />

        <KPICard
          title="System Health"
          value={data.systemHealth}
          icon={<CheckCircleOutlined />}
          iconBgColor={getSystemHealthColor(data.systemHealth)}
          loading={loading}
        />
      </div>
    </div>
  );
}

export default memo(GlobalKPIOverview);
