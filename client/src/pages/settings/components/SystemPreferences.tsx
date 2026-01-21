import { ThunderboltOutlined } from '@ant-design/icons';
import { Checkbox, ConfigProvider, InputNumber } from 'antd';
import { useState } from 'react';

interface Props {
    disabled?: boolean;
}

export default function SystemPreferences({ disabled = false }: Props) {
    const [updateFrequency, setUpdateFrequency] = useState(5);
    const [maxCongestionThreshold, setMaxCongestionThreshold] = useState(80);
    const [enableAutoOptimization, setEnableAutoOptimization] = useState(true);

    return (
        <ConfigProvider
            theme={{
                token: {
                    colorPrimary: '#8b5cf6', // purple-500
                },
            }}
        >
            <div className="border border-gray-200 rounded-lg p-6 mt-4">
                <div className='flex items-center mb-6'>
                    <ThunderboltOutlined className='mr-2 text-lg' />
                    <h1 className='text-xl font-semibold m-0'>System Preferences</h1>
                </div>
                
                {/* Update Frequency and Max Congestion Threshold Row */}
                <div className='grid grid-cols-1 md:grid-cols-2 gap-4 mb-4'>
                    <div>
                        <label className='block mb-2 font-medium'>Update Frequency (seconds)</label>
                        <InputNumber
                            value={updateFrequency}
                            onChange={(value) => setUpdateFrequency(value || 0)}
                            min={1}
                            max={60}
                            className='w-full'
                            disabled={disabled}
                        />
                    </div>
                    <div>
                        <label className='block mb-2 font-medium'>Max Congestion Threshold (%)</label>
                        <InputNumber
                            value={maxCongestionThreshold}
                            onChange={(value) => setMaxCongestionThreshold(value || 0)}
                            min={0}
                            max={100}
                            className='w-full'
                            disabled={disabled}
                        />
                    </div>
                </div>

                {/* Enable Auto Optimization Checkbox */}
                <div className='flex items-start mt-6'>
                    <Checkbox
                        checked={enableAutoOptimization}
                        onChange={(e) => setEnableAutoOptimization(e.target.checked)}
                        className='mt-1'
                        disabled={disabled}
                    >
                        <div>
                            <div className='font-medium text-base'>Enable Auto Optimization</div>
                            <div className='text-sm text-gray-500'>Automatically optimize traffic signals based on real-time data</div>
                        </div>
                    </Checkbox>
                </div>
            </div>
        </ConfigProvider>
    );
}
