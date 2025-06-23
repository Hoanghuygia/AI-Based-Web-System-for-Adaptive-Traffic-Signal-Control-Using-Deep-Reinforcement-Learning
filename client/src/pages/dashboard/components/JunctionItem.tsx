import { Tag } from 'antd'
import { RightOutlined } from '@ant-design/icons'

interface Junction {
  id: number
  name: string
  status: string
  congestionLevel: number
  lastUpdated: string
}

const getStatusLabel = (status: string) => {
  switch (status) {
    case "high":
      return "Heavy Traffic"
    case "medium":
      return "Moderate Traffic"
    case "low":
      return "Light Traffic"
    default:
      return "Unknown"
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case "high":
      return "error"
    case "medium":
      return "warning"
    case "low":
      return "success"
    default:
      return "default"
  }
}

const getStatusDotColor = (status: string) => {
  switch (status) {
    case "high":
      return "bg-red-500"
    case "medium":
      return "bg-yellow-500"
    case "low":
      return "bg-green-500"
    default:
      return "bg-gray-500"
  }
}

export default function JunctionItem({ junction }: { junction: Junction }) {
  const handleClick = () => {
    window.location.href = `/junction/${junction.id}`
  }

  return (
    <div
      onClick={handleClick}
      className="grid grid-cols-12 p-4 hover:bg-gray-50 transition-colors items-center cursor-pointer"
    >
      <div className="col-span-6 flex items-center">
        <div className={`w-3 h-3 rounded-full mr-3 ${getStatusDotColor(junction.status)}`}></div>
        <div>
          <h3 className="font-medium text-gray-800">{junction.name}</h3>
          <div className="text-sm text-gray-500">Congestion Level: {junction.congestionLevel}%</div>
        </div>
      </div>
      <div className="col-span-3 text-center">
        <Tag color={getStatusColor(junction.status)}>
          {getStatusLabel(junction.status)}
        </Tag>
      </div>
      <div className="col-span-2 text-center text-sm text-gray-500">{junction.lastUpdated}</div>
      <div className="col-span-1 flex justify-end">
        <RightOutlined className="text-gray-400" />
      </div>
    </div>
  )
}