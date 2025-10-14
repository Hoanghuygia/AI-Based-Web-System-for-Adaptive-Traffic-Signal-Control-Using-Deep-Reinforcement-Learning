import { useAppDispatch } from "@src/stores/hooks";
import { logout } from "@src/stores/user.slice";
import { Button, Dropdown, Input } from "antd";
import { useNavigate } from "react-router-dom";
import {
    SearchOutlined,
    FilterOutlined,
    ArrowRightOutlined,
} from "@ant-design/icons";
import HeaderRow from "./components/HeaderRow";

export default function Dashboard() {
    console.log("Render Dashboard");

    const items = [
        {
            key: "1",
            label: "All",
        },
        {
            key: "2",
            label: "Heavy Traffic",
        },
        {
            key: "3",
            label: "Moderate Traffic",
        },
        {
            key: "4",
            label: "Light Traffic",
        },
    ];

    return (
        <div className="flex flex-col justify-start items-center gap-y-5 p-4">
            <div className="w-full flex flex-col justify-center items-start">
                <h1 className="text-2xl font-bold mb-4">
                    Traffic Junction List
                </h1>
                <p>
                    Monitor and manage traffic congestion at
                    various junctions in District 3, Ho Chi
                    Minh City
                </p>
            </div>
            <div
                id="filter-bar"
                className="w-full flex flex-row justify-start items-center bg-gray-200 p-4 rounded-md"
            >
                <div className="relative flex-1">
                    <SearchOutlined className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 z-10" />
                    <Input
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2
                        focus:ring-purple-500 focus:border-transparent  hover:!border-purple-500 hover:!text-purple-500 transition duration-300"
                        placeholder="Search junctions..."
                    />
                </div>

                <Dropdown
                    menu={{ items }}
                    overlayClassName="custom-dropdown-search-bar"
                    placement="bottomLeft"
                    trigger={["click"]}
                >
                    <Button
                        icon={<FilterOutlined />}
                        className="ml-4 h-10 bg-white rounded-md 
                    hover:!border-purple-500 hover:!text-purple-500 
                    transition duration-300"
                    >
                        Filter By Status
                    </Button>
                </Dropdown>
            </div>
            <div className="w-full flex flex-col justify-start items-center">
                <HeaderRow/>

                {/* Card row */}
                <div
                    id="card"
                    className="relative w-full flex flex-row items-center cursor-pointer 
        bg-white px-6 py-4 border border-gray-200 hover:shadow-md transition-shadow"
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
                                Hai Ba Trung - Nguyen Thi
                                Minh Khai
                            </p>
                            <p className="text-xs text-gray-500">
                                ID: JCT-001 • Congestion:
                                45%
                            </p>
                        </div>
                    </div>

                    {/* Status */}
                    <div className="flex flex-[2] justify-center">
                        <p className="inline-block text-xs font-semibold bg-red-400 text-white px-3 py-1 rounded-2xl">
                            Heavy Traffic
                        </p>
                    </div>

                    {/* Last Update */}
                    <p className="flex-[1] text-left text-sm text-gray-500">
                        5 minutes ago
                    </p>

                    {/* Arrow Icon */}
                    <ArrowRightOutlined className="absolute right-6 text-gray-400 text-lg hover:text-gray-600 transition-colors" />
                </div>
            </div>
        </div>
    );
}
