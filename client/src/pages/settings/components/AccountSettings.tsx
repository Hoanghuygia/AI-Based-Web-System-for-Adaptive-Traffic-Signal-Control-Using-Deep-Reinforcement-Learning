import { SettingOutlined } from '@ant-design/icons';
import { Input, Select } from 'antd';
import { useState } from 'react';

interface Props {
    disabled?: boolean;
}

export default function AccountSettings({ disabled = false }: Props) {
    const [email, setEmail] = useState('admin@traffic-system.local');
    const [phoneNumber, setPhoneNumber] = useState('+84 912 345 678');
    const [language, setLanguage] = useState('English');

    return (
        <div className="border border-gray-200 rounded-lg p-5">
            <div className='flex items-center mb-6'>
                <SettingOutlined className='mr-2 text-lg' />
                <h1 className='text-xl font-semibold m-0'>Account Settings</h1>
            </div>
            
            {/* Email and Phone Number Row */}
            <div className='grid grid-cols-1 md:grid-cols-2 gap-4 mb-4'>
                <div>
                    <label className='block mb-2 font-medium'>Email Address</label>
                    <Input 
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                        className='w-full'
                        disabled={disabled}
                    />
                </div>
                <div>
                    <label className='block mb-2 font-medium'>Phone Number</label>
                    <Input 
                        value={phoneNumber}
                        onChange={(e) => setPhoneNumber(e.target.value)}
                        placeholder="Enter your phone number"
                        className='w-full'
                        disabled={disabled}
                    />
                </div>
            </div>

            {/* Language Dropdown */}
            <div className='mb-4'>
                <label className='block mb-2 font-medium'>Language</label>
                <Select
                    value={language}
                    onChange={(value) => setLanguage(value)}
                    className='w-full'
                    disabled={disabled}
                    options={[
                        { value: 'English', label: 'English' },
                        { value: 'Vietnamese', label: 'Vietnamese' },
                        { value: 'Spanish', label: 'Spanish' },
                        { value: 'French', label: 'French' },
                    ]}
                />
            </div>
        </div>
    );
}