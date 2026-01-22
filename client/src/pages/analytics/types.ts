import { ReactNode } from 'react';

export interface KPICardProps {
  title: string;
  value: string | number;
  icon: ReactNode;
  iconBgColor?: string;
  trend?: 'up' | 'down' | 'neutral';
  subtitle?: string;
  loading?: boolean;
}

export interface GlobalKPIData {
  totalJunctions: number;
  activeJunctions: number;
  avgCongestion: number;
  avgWaitTime: number;
  throughput: number;
  systemHealth: 'Normal' | 'Warning' | 'Critical';
}

export interface TrafficPerformanceData {
  totalVehicles: number;
  avgSpeed: number;
  peakHourTraffic: number;
  flowRate: number;
}

export interface CongestionData {
  currentLevel: number;
  density: number;
  congestionZones: number;
  averageDuration: number;
}

export interface AnalyticsData {
  globalKPI: GlobalKPIData;
  trafficPerformance: TrafficPerformanceData;
  congestion: CongestionData;
  timestamp: string;
}

export const DEFAULT_ANALYTICS_DATA: AnalyticsData = {
  globalKPI: {
    totalJunctions: 16,
    activeJunctions: 15,
    avgCongestion: 38,
    avgWaitTime: 42,
    throughput: 2400,
    systemHealth: 'Normal',
  },
  trafficPerformance: {
    totalVehicles: 15420,
    avgSpeed: 45,
    peakHourTraffic: 3200,
    flowRate: 1850,
  },
  congestion: {
    currentLevel: 38,
    density: 65,
    congestionZones: 3,
    averageDuration: 285,
  },
  timestamp: new Date().toISOString(),
};
