import { Empty } from 'antd'
import JunctionItem from "./JunctionItem"
import { Junction } from "../data/Junction.ts"


export default function JunctionList({ junctions }: { junctions: Junction[] }) {
  return (
    <div className="bg-white rounded-lg border overflow-hidden">
      <div className="grid grid-cols-12 bg-gray-50 p-4 border-b font-medium text-sm text-gray-500">
        <div className="col-span-6">JUNCTION NAME</div>
        <div className="col-span-3 text-center">STATUS</div>
        <div className="col-span-2 text-center">LAST UPDATE</div>
        <div className="col-span-1"></div>
      </div>
      {junctions.length > 0 ? (
        <div className="divide-y">
          {junctions.map((junction) => (
            <JunctionItem key={junction.id} junction={junction} />
          ))}
        </div>
      ) : (
        <div className="p-8 flex justify-center">
          <Empty 
            description="No junctions found matching your search criteria"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        </div>
      )}
    </div>
  )
}