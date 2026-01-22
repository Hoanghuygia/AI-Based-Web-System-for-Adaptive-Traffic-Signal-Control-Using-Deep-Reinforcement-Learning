import { GlobalOutlined } from '@ant-design/icons';
import { Checkbox, ConfigProvider, InputNumber } from 'antd';
import { memo } from 'react';
import { APISettingsData } from '../types';

interface Props {
    disabled?: boolean;
    data: APISettingsData;
    onChange: (data: Partial<APISettingsData>) => void;
}

function APISettings({ disabled = false, data, onChange }: Props) {
    return (
        <ConfigProvider
            theme={{
                token: {
                    colorPrimary: '#8b5cf6',
                },
            }}
        >
            <div className="border border-gray-200 rounded-lg p-6 mt-4">
                <div className='flex items-center mb-6'>
                    <GlobalOutlined className='mr-2 text-lg' />
                    <h1 className='text-xl font-semibold m-0'>API Settings</h1>
                </div>
                
                {/* Enable API Access Checkbox */}
                <div className='flex items-start mb-6'>
                    <Checkbox
                        checked={data.enableAPIAccess}
                        onChange={(e) => onChange({ enableAPIAccess: e.target.checked })}
                        className='mt-1'
                        disabled={disabled}
                    >
                        <div>
                            <div className='font-medium text-base'>Enable API Access</div>
                            <div className='text-sm text-gray-500'>Allow third-party integrations via API</div>
                        </div>
                    </Checkbox>
                </div>

                {/* API Rate Limit Input */}
                <div>
                    <label className='block mb-2 font-medium'>API Rate Limit (requests/hour)</label>
                    <InputNumber
                        value={data.apiRateLimit}
                        onChange={(value) => onChange({ apiRateLimit: value || 100 })}
                        min={100}
                        max={10000}
                        className='w-full md:w-1/2'
                        disabled={disabled}
                    />
                </div>
            </div>
        </ConfigProvider>
    );
}

export default memo(APISettings);
