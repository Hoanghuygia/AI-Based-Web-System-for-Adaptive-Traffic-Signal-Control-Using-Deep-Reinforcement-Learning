import {
    ArrowDownOutlined,
    ArrowUpOutlined,
} from "@ant-design/icons";

interface LaneNumber {
    total: number;
    upbound: number;
    downbound: number;
}

type LaneCardProps = {
    label: string;
    laneNumber?: LaneNumber;
}

export default function LaneCard({ label, laneNumber }: LaneCardProps) {
    return (
        <div className="border border-gray-200 rounded-lg p-4">
            <h4 className="font-semibold text-gray-800 mb-4">
                {label}
            </h4>
            <div className="space-y-3">
                <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">
                        Total Lanes
                    </span>
                    <span className="font-semibold text-gray-800">
                        {laneNumber?.total ?? 6}
                    </span>
                </div>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <ArrowUpOutlined className="text-green-500 text-xs" />
                        <span className="text-sm text-gray-600">
                            Upbound Lanes
                        </span>
                    </div>
                    <span className="font-semibold text-gray-800">
                        {laneNumber?.upbound ?? 3}
                    </span>
                </div>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <ArrowDownOutlined className="text-orange-500 text-xs" />
                        <span className="text-sm text-gray-600">
                            Downbound Lanes
                        </span>
                    </div>
                    <span className="font-semibold text-gray-800">
                        {laneNumber?.downbound ?? 3}
                    </span>
                </div>
            </div>
        </div>
    );
}
