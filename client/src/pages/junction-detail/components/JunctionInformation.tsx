import { ClockCircleOutlined } from "@ant-design/icons";
import LaneCard from "./LaneCard";
import SignalTraffic from "./SignalTraffic";

export default function JunctionInformation() {
    return (
        <div className="bg-white rounded-lg border border-gray-200 p-6 space-y-6">
            <h2 className="text-xl font-semibold text-gray-800">
                Junction Information
            </h2>

            {/* Lane Configuration Section */}
            <div className="border border-gray-200 rounded-lg p-6">
                <div className="flex items-center gap-2 mb-6">
                    <svg
                        className="w-5 h-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"
                        />
                    </svg>
                    <h3 className="text-base font-semibold text-gray-800">
                        Lane Configuration
                    </h3>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    {/* North-South Card */}
                    <LaneCard
                        label="North-South"
                        laneNumber={{
                            total: 6,
                            upbound: 3,
                            downbound: 3,
                        }}
                    />

                    {/* East-West Card */}
                    <LaneCard
                        label="East-West"
                        laneNumber={{
                            total: 6,
                            upbound: 3,
                            downbound: 3,
                        }}
                    />
                </div>
            </div>

            {/* Signal Timing Section */}
            <div className="border border-gray-200 rounded-lg p-5">
                <div className="flex items-center gap-2 mb-4">
                    <ClockCircleOutlined className="text-base" />
                    <h3 className="text-base font-semibold text-gray-800">
                        Signal Timing
                    </h3>
                </div>

                <div className="space-y-4">
                    {/* North-South Timing */}
                    <div>
                        <h4 className="text-sm font-medium text-gray-800 mb-2">
                            North-South
                        </h4>

                        {/* Straight */}
                        <SignalTraffic
                            direction="Straight"
                            waitingTime={{
                                green: 45,
                                yellow: 5,
                                red: 50,
                            }}
                        />

                        {/* Left */}
                        <SignalTraffic
                            direction="Left"
                            waitingTime={{
                                green: 15,
                                yellow: 3,
                                red: 82,
                            }}
                        />
                    </div>

                    {/* East-West Timing */}
                    <div>
                        <h4 className="text-sm font-medium text-gray-800 mb-2">
                            East-West
                        </h4>

                        {/* Straight */}
                        <SignalTraffic
                            direction="Straight"
                            waitingTime={{
                                green: 40,
                                yellow: 4,
                                red: 56,
                            }}
                        />

                        {/* Left */}
                        <SignalTraffic
                            direction="Left"
                            waitingTime={{
                                green: 10,
                                yellow: 2,
                                red: 88,
                            }}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
}
