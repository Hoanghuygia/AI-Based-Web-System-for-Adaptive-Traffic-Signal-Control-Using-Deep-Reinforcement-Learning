import { ArrowUpOutlined } from '@ant-design/icons';
type SignalTrafficProps = {
    direction: "Straight" | "Left" | "Right";
    waitingTime: {
        green: number;
        yellow: number;
        red: number;
    };
};

export default function SignalTraffic({
    direction,
    waitingTime,
}: SignalTrafficProps) {
    return (
        <div className="mb-3">
            <div className="flex items-center gap-1.5 mb-1.5">
                <ArrowUpOutlined className='text-xs'/>
                <span className="text-xs text-gray-700">
                    {direction}
                </span>
            </div>
            <div className="grid grid-cols-3 gap-1.5">
                <div className="bg-green-50 border border-green-200 rounded px-2 py-1.5 text-center">
                    <div className="w-5 h-5 bg-green-500 rounded-full mx-auto mb-1"></div>
                    <span className="text-xs font-medium text-gray-800">
                        {waitingTime.green}s
                    </span>
                </div>
                <div className="bg-yellow-50 border border-yellow-200 rounded px-2 py-1.5 text-center">
                    <div className="w-5 h-5 bg-yellow-500 rounded-full mx-auto mb-1"></div>
                    <span className="text-xs font-medium text-gray-800">
                        {waitingTime.yellow}s
                    </span>
                </div>
                <div className="bg-red-50 border border-red-200 rounded px-2 py-1.5 text-center">
                    <div className="w-5 h-5 bg-red-500 rounded-full mx-auto mb-1"></div>
                    <span className="text-xs font-medium text-gray-800">
                        {waitingTime.red}s
                    </span>
                </div>
            </div>
        </div>
    );
}
