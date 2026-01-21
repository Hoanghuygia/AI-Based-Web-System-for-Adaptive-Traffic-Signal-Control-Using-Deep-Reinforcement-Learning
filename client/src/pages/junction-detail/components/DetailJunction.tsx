import {
    ClockCircleOutlined,
    CameraOutlined,
    RiseOutlined,
} from "@ant-design/icons";
import { Button, Progress } from "antd";

type DetailJunctionProps = {
    onViewChange: () => void;
    buttonText: string;
};

// Detail Junction Component
export default function DetailJunction({ onViewChange, buttonText }: DetailJunctionProps) {
    return (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Detailed Information
            </h2>
            <p className="text-gray-600 mb-6">
                Major intersection connecting Hai Ba Trung
                and Nguyen Thi Minh Khai streets in the
                heart of District 3
            </p>

            {/* Update time and congestion level */}
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center text-gray-500 text-sm">
                    <ClockCircleOutlined className="mr-2" />
                    Updated: 5 minutes ago
                </div>
                <div className="flex items-center text-gray-500 text-sm">
                    <RiseOutlined className="mr-2" />
                    Current congestion level
                </div>
            </div>

            {/* Progress bar */}
            <div className="mb-8">
                <div className="flex items-center gap-3">
                    <div className="flex-shrink-0">
                        <span className="inline-flex items-center justify-center w-12 h-8 bg-red-100 text-red-500 rounded text-sm font-semibold">
                            85%
                        </span>
                    </div>
                    <Progress
                        percent={85}
                        showInfo={false}
                        strokeColor="#ef4444"
                    />
                </div>
            </div>

            {/* Actions */}
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
                Actions
            </h3>
            <div className="grid grid-cols-2 gap-4 mb-8">
                <Button
                    type="primary"
                    size="large"
                    className="!bg-purple-400 hover:!bg-purple-500 !border-purple-400 h-12"
                >
                    Switch Phase
                </Button>
                <Button
                    size="large"
                    icon={<CameraOutlined />}
                    className="h-12"
                    onClick={onViewChange}
                >
                    {buttonText}
                </Button>
            </div>

            {/* Traffic Light Status */}
            <div className="mb-6">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-800">
                        Traffic Light Status
                    </h3>
                    <div className="flex items-center gap-2">
                        <span className="text-sm text-gray-600">
                            Mode:
                        </span>
                        <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded text-sm font-medium">
                            Auto
                        </span>
                    </div>
                </div>

                {/* Traffic light cards */}
                <div className="grid grid-cols-2 gap-4 mb-6">
                    {/* North-South */}
                    <div className="border border-gray-200 rounded-lg p-6 text-center">
                        <div className="text-gray-600 font-medium mb-4">
                            North-South
                        </div>
                        <div className="w-16 h-16 bg-red-500 rounded-full mx-auto mb-4"></div>
                        <div className="text-2xl font-semibold text-gray-800 mb-1">
                            6s
                        </div>
                        <div className="text-sm text-gray-500">
                            Red Light
                        </div>
                    </div>

                    {/* East-West */}
                    <div className="border border-gray-200 rounded-lg p-6 text-center">
                        <div className="text-gray-600 font-medium mb-4">
                            East-West
                        </div>
                        <div className="w-16 h-16 bg-green-500 rounded-full mx-auto mb-4"></div>
                        <div className="text-2xl font-semibold text-gray-800 mb-1">
                            6s
                        </div>
                        <div className="text-sm text-gray-500">
                            Green Light
                        </div>
                    </div>
                </div>

                {/* Cycle info */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="flex justify-between text-sm">
                        <span className="text-gray-600">
                            Cycle Time:
                        </span>
                        <span className="font-semibold text-gray-800">
                            90s
                        </span>
                    </div>
                    <div className="flex justify-between text-sm">
                        <span className="text-gray-600">
                            Next Phase:
                        </span>
                        <span className="font-semibold text-gray-800">
                            Yellow (E-W)
                        </span>
                    </div>
                </div>

                {/* Info banner */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 flex items-start">
                    <svg
                        className="w-5 h-5 text-blue-500 mr-2 flex-shrink-0 mt-0.5"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                    >
                        <path
                            fillRule="evenodd"
                            d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                            clipRule="evenodd"
                        />
                    </svg>
                    <span className="text-sm text-blue-700">
                        Not connected to SUMO. Showing
                        simulated traffic light data.
                    </span>
                </div>
            </div>
        </div>
    );
}
