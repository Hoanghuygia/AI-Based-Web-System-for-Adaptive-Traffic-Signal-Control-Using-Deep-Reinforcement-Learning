import { useState } from "react";
import { useParams } from "react-router-dom";
import HeaderJunction from "./components/HeaderJunction";
import DetailJunction from "./components/DetailJunction";
import ChartJunction from "./components/ChartJunction";
import ViewSumo from "./components/ViewSumo";
import JunctionInformation from "./components/JunctionInformation";

type RightViewType = "chart" | "sumo" | "info" | "all";

export default function JunctionDetail() {
    const { id } = useParams<{ id: string }>();
    const [rightView, setRightView] = useState<RightViewType>("chart");

    const handleViewChange = () => {
        if (rightView === "chart") {
            setRightView("sumo");
        } else if (rightView === "sumo") {
            setRightView("info");
        } else if (rightView === "info") {
            setRightView("all");
        } else {
            setRightView("chart");
        }
    };

    const getButtonText = () => {
        if (rightView === "chart") return "View SUMO Live";
        if (rightView === "sumo") return "View Junction Information";
        if (rightView === "info") return "Show All";
        return "View SUMO Live";
    };

    console.log("Junction ID:", id);

    return (
        <div className="flex flex-col justify-start items-start h-full w-full bg-white rounded-xl">
            {/* Header Junction Section */}
            <HeaderJunction />
            {/* Content Area */}
            <div className="w-full border-gray-200 px-6 py-6 border-t">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Left content area */}
                    <div className="space-y-6">
                        {/* Detailed Information */}
                        <DetailJunction 
                            onViewChange={handleViewChange}
                            buttonText={getButtonText()}
                        />
                    </div>

                    {/* Right content area - conditional rendering */}
                    {rightView === "chart" && <ChartJunction />}
                    {rightView === "sumo" && <ViewSumo />}
                    {rightView === "info" && <JunctionInformation />}
                    {rightView === "all" && (
                        <div className="space-y-6">
                            <ChartJunction />
                            <ViewSumo />
                            <JunctionInformation />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
