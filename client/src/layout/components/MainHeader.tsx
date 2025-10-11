import React from "react";
import { Button, Dropdown } from "antd";
import {
    EnvironmentOutlined,
    MenuOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

type MainHeaderProps = {
    username: string;
};

const MainHeader: React.FC<MainHeaderProps> = ({
    username,
}) => {
    const { t } = useTranslation();
    const navigate = useNavigate();

    const items = [
        {
            key: "1",
            label: "Profile",
        },
        {
            key: "2",
            label: "Settings",
        },
        {
            key: "3",
            label: "Logout",
        },
    ];

    return (
        <div className="flex justify-between items-center">
            <div className="flex items-center space-x-3">
                <EnvironmentOutlined className="!text-purple-500 text-3xl" />
                <h1 className="cursor-pointer text-lg font-semibold" onClick={() => navigate("/dashboard")}>
                    {t("dashboard.appName")}
                </h1>
            </div>
            <div className="flex items-center space-x-6">
                <span className="text-gray-600">
                    {t("dashboard.welcome")}, {username}
                </span>

                <button className="cursor-pointer flex items-center justify-self-center h-8 px-4 rounded-md text-gray-600 hover:text-gray-800 hover:bg-gray-200">
                    {t("dashboard.notification")}
                </button>

                <Dropdown
                    menu={{ items }}
                    overlayClassName="custom-dropdown"
                    placement="bottomRight"
                    trigger={["click"]}
                >
                    <Button
                        type="text"
                        icon={<MenuOutlined />}
                    />
                </Dropdown>
            </div>
        </div>
    );
};

export default MainHeader;
