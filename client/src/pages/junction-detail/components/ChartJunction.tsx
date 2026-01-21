export default function ChartJunction() {
    return (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">
                Daily Traffic Pattern
            </h2>

            {/* Chart header */}
            <div className="flex items-center justify-between mb-4">
                <span className="text-sm text-gray-600">
                    Traffic Volume (Last 12 Hours)
                </span>
                <span className="text-sm text-gray-500">
                    Peak: 86% at 18:00
                </span>
            </div>

            {/* Chart placeholder - you can replace with actual chart library */}
            <div className="h-64 bg-gray-50 rounded-lg mb-4 flex items-end justify-around p-4">
                {/* Simplified bar chart representation */}
                <div className="flex-1 flex flex-col items-center">
                    <div
                        className="w-full bg-red-400 rounded-t"
                        style={{
                            height: "60%",
                        }}
                    ></div>
                    <span className="text-xs text-gray-500 mt-2">
                        17:00
                    </span>
                </div>
                <div className="flex-1 flex flex-col items-center">
                    <div
                        className="w-full bg-red-500 rounded-t"
                        style={{
                            height: "70%",
                        }}
                    ></div>
                    <span className="text-xs text-gray-500 mt-2">
                        18:00
                    </span>
                </div>
                <div className="flex-1 flex flex-col items-center">
                    <div
                        className="w-full bg-red-500 rounded-t"
                        style={{
                            height: "65%",
                        }}
                    ></div>
                    <span className="text-xs text-gray-500 mt-2">
                        19:00
                    </span>
                </div>
                <div className="flex-1 flex flex-col items-center">
                    <div
                        className="w-full bg-red-500 rounded-t"
                        style={{
                            height: "58%",
                        }}
                    ></div>
                    <span className="text-xs text-gray-500 mt-2">
                        20:00
                    </span>
                </div>
                <div className="flex-1 flex flex-col items-center">
                    <div
                        className="w-full bg-yellow-400 rounded-t"
                        style={{
                            height: "40%",
                        }}
                    ></div>
                    <span className="text-xs text-gray-500 mt-2">
                        21:00
                    </span>
                </div>
                <div className="flex-1 flex flex-col items-center">
                    <div
                        className="w-full bg-yellow-400 rounded-t"
                        style={{
                            height: "32%",
                        }}
                    ></div>
                    <span className="text-xs text-gray-500 mt-2">
                        22:00
                    </span>
                </div>
                <div className="flex-1 flex flex-col items-center">
                    <div
                        className="w-full bg-green-500 rounded-t"
                        style={{
                            height: "15%",
                        }}
                    ></div>
                    <span className="text-xs text-gray-500 mt-2">
                        23:00
                    </span>
                </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                    <span className="text-gray-600">
                        Avg (12h):
                    </span>
                    <span className="font-semibold text-gray-800 ml-2">
                        37%
                    </span>
                </div>
                <div>
                    <span className="text-gray-600">
                        Min:
                    </span>
                    <span className="font-semibold text-gray-800 ml-2">
                        0%
                    </span>
                </div>
                <div>
                    <span className="text-gray-600">
                        Max:
                    </span>
                    <span className="font-semibold text-gray-800 ml-2">
                        86%
                    </span>
                </div>
                <div>
                    <span className="text-gray-600">
                        Current:
                    </span>
                    <span className="font-semibold text-blue-600 ml-2">
                        3%
                    </span>
                </div>
            </div>
        </div>
    );
}
