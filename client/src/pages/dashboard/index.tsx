import { useAppDispatch } from "@src/stores/hooks";
import { logout } from "@src/stores/user.slice";
import { Button, Dropdown, Input } from "antd";
import { useNavigate } from "react-router-dom";
import {
    SearchOutlined,
    FilterOutlined,
} from "@ant-design/icons";

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
        <div className="flex flex-col justify-start items-center gap-y-4 p-4">
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
        </div>
    );
}
