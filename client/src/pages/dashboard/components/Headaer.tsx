import { Button, Dropdown } from 'antd'
import { BellOutlined, MenuOutlined, EnvironmentOutlined } from '@ant-design/icons'


export default function Header() {
  const menuItems = [
    {
      key: 'profile',
      label: 'Profile',
    },
    {
      key: 'settings', 
      label: 'Settings',
    },
    {
      key: 'logout',
      label: <a href="/" className="block">Logout</a>,
    },
  ]

  return (
    <header className="bg-white shadow">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center">
          <div className="bg-purple-500 text-white p-2 rounded-md mr-3">
            <EnvironmentOutlined className="text-2xl" />
          </div>
          <h1 className="text-xl font-bold text-gray-800">Traffic Management System</h1>
        </div>
        <div className="flex items-center gap-4">
          <Button 
            type="text" 
            className="text-gray-600 hover:text-gray-800"
            icon={<BellOutlined />}
          >
            Notifications
          </Button>
          <Dropdown 
            menu={{ items: menuItems }} 
            placement="bottomRight"
            trigger={['click']}
          >
            <Button 
              type="text" 
              className="text-gray-600 hover:text-gray-800"
              icon={<MenuOutlined />}
            />
          </Dropdown>
        </div>
      </div>
    </header>
  )
}