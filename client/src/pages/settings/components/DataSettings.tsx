import { DatabaseOutlined } from '@ant-design/icons';
import { Checkbox, ConfigProvider, InputNumber } from 'antd';
import { memo } from 'react';
import { DataSettingsData } from '../types';

interface Props {
    disabled?: boolean;
    data: DataSettingsData;
    onChange: (data: Partial<DataSettingsData>) => void;
}

function DataSettings({ disabled = false, data, onChange }: Props) {
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
                    <DatabaseOutlined className='mr-2 text-lg' />
                    <h1 className='text-xl font-semibold m-0'>Data Settings</h1>
                </div>
                
                {/* Data Retention Input */}
                <div className='mb-6'>
                    <label className='block mb-2 font-medium'>Data Retention (days)</label>
                    <InputNumber
                        value={data.dataRetention}
                        onChange={(value) => onChange({ dataRetention: value || 1 })}
                        min={1}
                        max={365}
                        className='w-full md:w-1/2'
                        disabled={disabled}
                    />
                </div>

                {/* Enable Data Export Checkbox */}
                <div className='flex items-start mb-4'>
                    <Checkbox
                        checked={data.enableDataExport}
                        onChange={(e) => onChange({ enableDataExport: e.target.checked })}
                        className='mt-1'
                        disabled={disabled}
                    >
                        <div>
                            <div className='font-medium text-base'>Enable Data Export</div>
                            <div className='text-sm text-gray-500'>Allow exporting data to CSV/Excel</div>
                        </div>
                    </Checkbox>
                </div>

                {/* Auto Backup Checkbox */}
                <div className='flex items-start'>
                    <Checkbox
                        checked={data.autoBackup}
                        onChange={(e) => onChange({ autoBackup: e.target.checked })}
                        className='mt-1'
                        disabled={disabled}
                    >
                        <div>
                            <div className='font-medium text-base'>Auto Backup</div>
                            <div className='text-sm text-gray-500'>Automatically backup system data daily</div>
                        </div>
                    </Checkbox>
                </div>
            </div>
        </ConfigProvider>
    );
}

export default memo(DataSettings);
