import { Input, Button, Dropdown } from 'antd'
import { SearchOutlined, FilterOutlined } from '@ant-design/icons'

interface FilterBarProps {
  searchQuery: string
  onSearchChange: (value: string) => void
  onStatusChange: (status: string) => void
}

export default function FilterBar({ searchQuery, onSearchChange, onStatusChange }: FilterBarProps) {
  const filterItems = [
    {
      key: 'all',
      label: 'All',
      onClick: () => onStatusChange('all'),
    },
    {
      key: 'high',
      label: 'Heavy Traffic',
      onClick: () => onStatusChange('high'),
    },
    {
      key: 'medium',
      label: 'Moderate Traffic',
      onClick: () => onStatusChange('medium'),
    },
    {
      key: 'low',
      label: 'Light Traffic',
      onClick: () => onStatusChange('low'),
    },
  ]

  const handleMenuClick = ({ key }: { key: string }) => {
    onStatusChange(key)
  }

  return (
    <div className="bg-gray-50 p-4 rounded-lg mb-6 flex flex-col md:flex-row gap-4">
      <div className="flex-1">
        <Input
          type="text"
          placeholder="Search junctions..."
          prefix={<SearchOutlined className="text-gray-400" />}
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          className="w-full"
        />
      </div>
      <Dropdown 
        menu={{ 
          items: filterItems,
          onClick: handleMenuClick
        }} 
        placement="bottomRight"
        trigger={['click']}
      >
        <Button className="flex items-center gap-2">
          <FilterOutlined />
          Filter by Status
        </Button>
      </Dropdown>
    </div>
  )
}