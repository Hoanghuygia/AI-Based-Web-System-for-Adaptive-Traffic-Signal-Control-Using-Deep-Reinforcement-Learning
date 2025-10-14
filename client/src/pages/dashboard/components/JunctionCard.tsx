import React from "react";
import { ArrowRightOutlined } from "@ant-design/icons";

type Junction = {
    id: string;
    name: string;
    lat: number;
    lng: number;
    status: "low" | "medium" | "high";
    lastUpdated: string;
    congestionLevel: number;
    location: string;
};

type JunctionCardProps = {
    junction: Junction;
    onClick?: (id: string) => void;
};

const JunctionCard: React.FC<JunctionCardProps> = ({
    junction,
    onClick,
}) => {
    const statusColors: Record<string, string> = {
        high: "bg-red-400 text-white",
        medium: "bg-yellow-400 text-black",
        low: "bg-green-400 text-white",
    };

    const statusText: Record<string, string> = {
        high: "Heavy Traffic",
        medium: "Moderate Traffic",
        low: "Light Traffic",
    };

    return (
        <div
            id="card"
            onClick={() => onClick?.(junction.id)}
            className="relative w-full flex flex-row items-center cursor-pointer 
      bg-white px-6 py-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow mb-2"
        >
            {/* Junction Info */}
            <div className="flex flex-row flex-[3] items-center">
                <p
                    id="dot"
                    className="font-bold text-5xl leading-none text-red-500 flex items-center justify-center h-full"
                >
                    •
                </p>
                <div className="flex flex-col justify-center items-start pl-4">
                    <p className="text-base font-semibold text-gray-800">
                        {junction.name}
                    </p>
                    <p className="text-xs text-gray-500">
                        ID: {junction.id} • Congestion:{" "}
                        {junction.congestionLevel}%
                    </p>
                </div>
            </div>

            {/* Status */}
            <div className="flex flex-[2] justify-center">
                <p
                    className={`inline-block text-xs font-semibold px-3 py-1 rounded-2xl ${
                        statusColors[junction.status]
                    }`}
                >
                    {statusText[junction.status]}
                </p>
            </div>

            {/* Last Update */}
            <p className="flex-[1] text-left text-sm text-gray-500">
                {junction.lastUpdated}
            </p>

            {/* Arrow Icon */}
            <ArrowRightOutlined className="absolute right-6 text-gray-400 text-lg hover:text-gray-600 transition-colors" />
        </div>
    );
};

export default JunctionCard;
