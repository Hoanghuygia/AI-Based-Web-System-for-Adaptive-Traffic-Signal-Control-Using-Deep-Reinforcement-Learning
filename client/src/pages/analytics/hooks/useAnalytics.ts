import { useState, useCallback, useEffect } from 'react';
import { AnalyticsData, DEFAULT_ANALYTICS_DATA } from '../types';

interface UseAnalyticsReturn {
  analytics: AnalyticsData;
  isLoading: boolean;
  error: string | null;
  refreshAnalytics: () => Promise<void>;
}

export function useAnalytics(): UseAnalyticsReturn {
  const [analytics, setAnalytics] = useState<AnalyticsData>(DEFAULT_ANALYTICS_DATA);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refreshAnalytics = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      // TODO: Replace with actual API call
      // const response = await fetch('/api/analytics');
      // const data = await response.json();

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 800));

      // For now, use default data with some randomization
      const fetchedData: AnalyticsData = {
        ...DEFAULT_ANALYTICS_DATA,
        globalKPI: {
          ...DEFAULT_ANALYTICS_DATA.globalKPI,
          avgCongestion: Math.floor(Math.random() * 30) + 25,
          avgWaitTime: Math.floor(Math.random() * 20) + 35,
          throughput: Math.floor(Math.random() * 500) + 2200,
        },
        timestamp: new Date().toISOString(),
      };

      setAnalytics(fetchedData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch analytics data');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Fetch analytics on mount
  useEffect(() => {
    refreshAnalytics();
  }, [refreshAnalytics]);

  // Auto-refresh every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      refreshAnalytics();
    }, 30000);

    return () => clearInterval(interval);
  }, [refreshAnalytics]);

  return {
    analytics,
    isLoading,
    error,
    refreshAnalytics,
  };
}
