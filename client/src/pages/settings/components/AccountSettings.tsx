import { SettingOutlined } from '@ant-design/icons';
import { Input, Select } from 'antd';
import { memo } from 'react';
import { AccountSettingsData } from '../types';

interface Props {
    disabled?: boolean;
    data: AccountSettingsData;
    onChange: (data: Partial<AccountSettingsData>) => void;
}

function AccountSettings({ disabled = false, data, onChange }: Props) {
    const validateEmail = (email: string): boolean => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newEmail = e.target.value;
        onChange({ email: newEmail });
    };

    const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        onChange({ phoneNumber: e.target.value });
    };

    const handleLanguageChange = (value: string) => {
        onChange({ language: value });
    };

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
                        value={data.email}
                        onChange={handleEmailChange}
                        placeholder="Enter your email"
                        className='w-full'
                        disabled={disabled}
                        status={!disabled && data.email && !validateEmail(data.email) ? 'error' : ''}
                    />
                    {!disabled && data.email && !validateEmail(data.email) && (
                        <span className='text-xs text-red-500 mt-1'>Please enter a valid email address</span>
                    )}
                </div>
                <div>
                    <label className='block mb-2 font-medium'>Phone Number</label>
                    <Input 
                        value={data.phoneNumber}
                        onChange={handlePhoneChange}
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
                    value={data.language}
                    onChange={handleLanguageChange}
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

export default memo(AccountSettings);