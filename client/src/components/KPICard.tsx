import { Card, Spin } from 'antd';
import { memo } from 'react';
import { KPICardProps } from '@src/pages/analytics/types';

function KPICard({
  title,
  value,
  icon,
  iconBgColor = 'bg-blue-100',
  trend,
  subtitle,
  loading = false,
}: KPICardProps) {
  return (
    <Card className="shadow-sm hover:shadow-md transition-shadow duration-200">
      <div className="flex flex-col h-full">
        {/* Top section: Title and Icon */}
        <div className="flex items-center justify-between mb-3">
          <p className="text-gray-500 text-sm mb-0 leading-tight mr-2">{title}</p>
          <div
            className={`${iconBgColor} w-12 h-12 rounded-lg flex items-center justify-center text-xl flex-shrink-0`}
          >
            {icon}
          </div>
        </div>

        {/* Bottom section: Value */}
        <div className='flex items-center justify-center'>
          {loading ? (
            <Spin size="small" />
          ) : (
            <h3 className="text-2xl font-bold text-gray-900 mb-0 leading-tight">{value}</h3>
          )}
          {subtitle && (
            <p className="text-xs text-gray-400 mt-1">{subtitle}</p>
          )}
          {trend && (
            <div className="mt-1">
              {trend === 'up' && (
                <span className="text-green-600 text-xs">↑ Trending up</span>
              )}
              {trend === 'down' && (
                <span className="text-red-600 text-xs">↓ Trending down</span>
              )}
              {trend === 'neutral' && (
                <span className="text-gray-600 text-xs">→ Stable</span>
              )}
            </div>
          )}
        </div>
      </div>
    </Card>
  );
}

export default memo(KPICard);
