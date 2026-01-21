import { GlobalOutlined } from '@ant-design/icons';
import { Checkbox, ConfigProvider, InputNumber } from 'antd';
import { useState } from 'react';

interface Props {
    disabled?: boolean;
}

export default function APISettings({ disabled = false }: Props) {
    const [enableAPIAccess, setEnableAPIAccess] = useState(true);
    const [apiRateLimit, setApiRateLimit] = useState(1000);

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
                    <GlobalOutlined className='mr-2 text-lg' />
                    <h1 className='text-xl font-semibold m-0'>API Settings</h1>
                </div>
                
                {/* Enable API Access Checkbox */}
                <div className='flex items-start mb-6'>
                    <Checkbox
                        checked={enableAPIAccess}
                        onChange={(e) => setEnableAPIAccess(e.target.checked)}
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
                        value={apiRateLimit}
                        onChange={(value) => setApiRateLimit(value || 0)}
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
