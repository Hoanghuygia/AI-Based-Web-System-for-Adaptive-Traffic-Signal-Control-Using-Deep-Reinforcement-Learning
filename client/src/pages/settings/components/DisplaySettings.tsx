import { BgColorsOutlined } from '@ant-design/icons';
import { Select } from 'antd';
import { useState } from 'react';

interface Props {
    disabled?: boolean;
}

export default function DisplaySettings({ disabled = false }: Props) {
    const [theme, setTheme] = useState('Light');
    const [dateFormat, setDateFormat] = useState('DD/MM/YYYY');
    const [timeFormat, setTimeFormat] = useState('24 Hour');

    return (
        <div className="border border-gray-200 rounded-lg p-6 mt-4">
            <div className='flex items-center mb-6'>
                <BgColorsOutlined className='mr-2 text-lg' />
                <h1 className='text-xl font-semibold m-0'>Display Settings</h1>
            </div>
            
            {/* Theme, Date Format, and Time Format Row */}
            <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
                <div>
                    <label className='block mb-2 font-medium'>Theme</label>
                    <Select
                        value={theme}
                        onChange={(value) => setTheme(value)}
                        className='w-full'
                        disabled={disabled}
                        options={[
                            { value: 'Light', label: 'Light' },
                            { value: 'Dark', label: 'Dark' },
                            { value: 'Auto', label: 'Auto' },
                        ]}
                    />
                </div>
                <div>
                    <label className='block mb-2 font-medium'>Date Format</label>
                    <Select
                        value={dateFormat}
                        onChange={(value) => setDateFormat(value)}
                        className='w-full'
                        disabled={disabled}
                        options={[
                            { value: 'DD/MM/YYYY', label: 'DD/MM/YYYY' },
                            { value: 'MM/DD/YYYY', label: 'MM/DD/YYYY' },
                            { value: 'YYYY/MM/DD', label: 'YYYY/MM/DD' },
                        ]}
                    />
                </div>
                <div>
                    <label className='block mb-2 font-medium'>Time Format</label>
                    <Select
                        value={timeFormat}
                        onChange={(value) => setTimeFormat(value)}
                        className='w-full'
                        disabled={disabled}
                        options={[
                            { value: '24 Hour', label: '24 Hour' },
                            { value: '12 Hour', label: '12 Hour' },
                        ]}
                    />
                </div>
            </div>
        </div>
    );
}
