import { LockOutlined } from '@ant-design/icons';
import { Checkbox, ConfigProvider, InputNumber } from 'antd';
import { useState } from 'react';

interface Props {
    disabled?: boolean;
}

export default function SecuritySettings({ disabled = false }: Props) {
    const [twoFactorAuth, setTwoFactorAuth] = useState(false);
    const [sessionTimeout, setSessionTimeout] = useState(30);

    return (
        <ConfigProvider
            theme={{
                token: {
                    colorPrimary: '#8b5cf6', // purple-400
                },
            }}
        >
            <div className="border border-gray-200 rounded-lg p-6">
                <div className='flex items-center mb-6'>
                    <LockOutlined className='mr-2 text-lg' />
                    <h1 className='text-xl font-semibold m-0'>Security Settings</h1>
                </div>
                
                <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
                    {/* Two-Factor Authentication Checkbox */}
                    <div className='flex items-start'>
                        <Checkbox
                            checked={twoFactorAuth}
                            onChange={(e) => setTwoFactorAuth(e.target.checked)}
                            className='mt-1'
                            disabled={disabled}
                        >
                            <div>
                                <div className='font-medium text-base'>Two-Factor Authentication</div>
                                <div className='text-sm text-gray-500'>Add an extra layer of security</div>
                            </div>
                        </Checkbox>
                    </div>

                    {/* Session Timeout Input */}
                    <div>
                        <label className='block mb-2 font-medium'>Session Timeout (minutes)</label>
                        <InputNumber
                            value={sessionTimeout}
                            onChange={(value) => setSessionTimeout(value || 0)}
                            min={5}
                            max={120}
                            className='w-full'
                            disabled={disabled}
                        />
                    </div>
                </div>
            </div>
        </ConfigProvider>
    );
}
