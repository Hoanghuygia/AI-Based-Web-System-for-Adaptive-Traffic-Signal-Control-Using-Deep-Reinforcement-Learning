import React from "react";
import { Input } from "antd";
import {
    ArrowLeftOutlined,
    EnvironmentOutlined,
    SearchOutlined,
} from "@ant-design/icons";
import { useNavigate, useParams } from "react-router-dom";
import DropdownHeader from "./DropdownHeader";
import { useTranslation } from "react-i18next";
import { useAppDispatch } from "@src/stores/hooks";
import { logout } from "@src/stores/user.slice";

const JunctionDetailHeader: React.FC = () => {
    const {t} = useTranslation();

    const navigate = useNavigate();
    const dispatch = useAppDispatch();

    const { id } = useParams<{ id: string }>();
    
    const handleLogout = () => {
        dispatch(logout());
        navigate("/login");
    };

        const itemsDropdown = [
        {
            key: "1",
            label: t("dashboard.nav.profile"),
        },
        {
            key: "2",
            label: t("dashboard.nav.setting"),
        },
        {
            key: "3",
            label: t("dashboard.nav.logout"),
        },
    ];

    return (
        <div className="flex justify-between items-center">
            <div className="flex items-center space-x-6">
                {/* Back to Dashboard Button */}
                <button
                    onClick={() => navigate("/dashboard")}
                    className="flex items-center space-x-2 text-gray-600 hover:text-purple-500 transition-colors cursor-pointer"
                >
                    <ArrowLeftOutlined className="text-lg" />
                    <span className="font-medium">Back to Dashboard</span>
                </button>

                {/* Divider */}
                <div className="h-6 w-px bg-gray-300"></div>

                {/* Junction ID */}
                <div className="flex items-center space-x-2">
                    <EnvironmentOutlined className="text-purple-500 text-xl" />
                    <span className="text-gray-700 font-medium">
                        Junction ID: {id}
                    </span>
                </div>
            </div>

            <div className="flex items-center space-x-4">
                {/* Search Box */}
                <div className="relative">
                    <SearchOutlined className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 z-10" />
                    <Input
                        className="w-80 pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2
                        focus:ring-purple-500 focus:border-transparent hover:!border-purple-500 transition duration-300"
                        placeholder="Search other junctions..."
                    />
                </div>

                {/* Simulated Badge
                <div className="flex items-center space-x-2 text-gray-500">
                    <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                    <span className="text-sm font-medium">Simulated</span>
                </div> */}
                <DropdownHeader
                    username={null}
                    t={t}
                    items={itemsDropdown}
                    handleLogout={handleLogout}
                />
            </div>
        </div>
    );
};

export default JunctionDetailHeader;
