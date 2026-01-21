import { BellOutlined } from '@ant-design/icons';
import { Checkbox, ConfigProvider } from 'antd';
import { useState } from 'react';

interface Props {
    disabled?: boolean;
}

export default function NotificationSettings({ disabled = false }: Props) {
    const [emailNotifications, setEmailNotifications] = useState(true);
    const [trafficAlerts, setTrafficAlerts] = useState(true);
    const [systemNotifications, setSystemNotifications] = useState(true);
    const [weeklyReport, setWeeklyReport] = useState(true);

    return (
        <ConfigProvider
            theme={{
                token: {
                    colorPrimary: '#8b5cf6', 
                },
            }}
        >
            <div className="border border-gray-200 rounded-lg p-5 mt-4">
                <div className='flex items-center mb-6'>
                    <BellOutlined className='mr-2 text-lg' />
                    <h1 className='text-xl font-semibold m-0'>Notification Settings</h1>
                </div>
                
                <div className='space-y-3'>
                {/* Email Notifications */}
                <div className='flex items-start'>
                    <Checkbox
                        checked={emailNotifications}
                        onChange={(e) => setEmailNotifications(e.target.checked)}
                        className='mt-1'
                        disabled={disabled}
                    >
                        <div>
                            <div className='font-medium text-base'>Email Notifications</div>
                            <div className='text-sm text-gray-500'>Receive updates via email</div>
                        </div>
                    </Checkbox>
                </div>

                {/* Traffic Alerts */}
                <div className='flex items-start'>
                    <Checkbox
                        checked={trafficAlerts}
                        onChange={(e) => setTrafficAlerts(e.target.checked)}
                        className='mt-1'
                        disabled={disabled}
                    >
                        <div>
                            <div className='font-medium text-base'>Traffic Alerts</div>
                            <div className='text-sm text-gray-500'>Get notified about traffic congestion</div>
                        </div>
                    </Checkbox>
                </div>

                {/* System Notifications */}
                <div className='flex items-start'>
                    <Checkbox
                        checked={systemNotifications}
                        onChange={(e) => setSystemNotifications(e.target.checked)}
                        className='mt-1'
                        disabled={disabled}
                    >
                        <div>
                            <div className='font-medium text-base'>System Notifications</div>
                            <div className='text-sm text-gray-500'>System updates and alerts</div>
                        </div>
                    </Checkbox>
                </div>

                {/* Weekly Report */}
                <div className='flex items-start'>
                    <Checkbox
                        checked={weeklyReport}
                        onChange={(e) => setWeeklyReport(e.target.checked)}
                        className='mt-1'
                        disabled={disabled}
                    >
                        <div>
                            <div className='text-sm font-medium'>Weekly Report</div>
                            <div className='text-xs text-gray-500'>Receive weekly traffic summary</div>
                        </div>
                    </Checkbox>
                </div>
            </div>
        </div>
        </ConfigProvider>
    );
}
