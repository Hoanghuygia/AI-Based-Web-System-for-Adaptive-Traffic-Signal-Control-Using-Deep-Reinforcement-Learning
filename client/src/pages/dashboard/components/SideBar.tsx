import { Menu } from 'antd';
import { DashboardOutlined, BarChartOutlined, NodeIndexOutlined, SettingOutlined } from '@ant-design/icons';
import { useState } from 'react';
import type { MenuProps } from 'antd'; // <-- Thêm dòng này để nhập kiểu MenuProps

export default function Sidebar() {
  const [selectedKey, setSelectedKey] = useState('dashboard');

  const menuItems: MenuProps['items'] = [ // <-- Thêm kiểu cho menuItems
    {
      key: 'overview',
      label: 'OVERVIEW',
      type: 'group',
      children: [
        {
          key: 'dashboard',
          icon: <DashboardOutlined />,
          label: <a href="/dashboard">Dashboard</a>,
        },
        {
          key: 'analytics',
          icon: <BarChartOutlined />,
          label: <a href="/analytics">Analytics</a>,
        },
      ],
    },
    {
      key: 'management',
      label: 'MANAGEMENT',
      type: 'group',
      children: [
        {
          key: 'junctions',
          icon: <NodeIndexOutlined />,
          label: <a href="/junctions">Junctions</a>,
        },
        {
          key: 'settings',
          icon: <SettingOutlined />,
          label: <a href="/settings">System Settings</a>,
        },
      ],
    },
  ];

  // <-- Sửa lỗi ở đây: thêm kiểu cho tham số 'e'
  const handleMenuClick: MenuProps['onClick'] = (e) => {
    setSelectedKey(e.key);
  };

  return (
    <div className="w-full md:w-64 bg-purple-500 text-white">
      <div className="p-6">
        <Menu
          mode="inline"
          selectedKeys={[selectedKey]}
          onClick={handleMenuClick}
          items={menuItems}
          className="bg-transparent border-none"
          theme="dark"
          style={{
            backgroundColor: 'transparent',
            color: 'white',
          }}
        />
      </div>

      <style jsx>{`
        :global(.ant-menu-dark .ant-menu-item-group-title) {
          color: rgb(196 181 253) !important;
          font-size: 0.875rem;
          font-weight: 500;
          padding-left: 12px;
          margin-bottom: 12px;
        }
        :global(.ant-menu-dark .ant-menu-item) {
          color: white !important;
          margin-bottom: 8px;
          border-radius: 6px;
        }
        :global(.ant-menu-dark .ant-menu-item:hover) {
          background-color: rgb(147 51 234) !important;
        }
        :global(.ant-menu-dark .ant-menu-item-selected) {
          background-color: rgb(124 58 237) !important;
        }
        :global(.ant-menu-dark .ant-menu-item a) {
          color: inherit !important;
          text-decoration: none;
        }
      `}</style>
    </div>
  );
}