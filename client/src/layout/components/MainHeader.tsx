import React from "react";
import { EnvironmentOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAppDispatch } from "@src/stores/hooks";
import { logout } from "@src/stores/user.slice";
import DropdownHeader from "./DropdownHeader";

type MainHeaderProps = {
    username: string;
};

const MainHeader: React.FC<MainHeaderProps> = ({
    username,
}) => {
    const { t } = useTranslation();
    const navigate = useNavigate();

    const dispatch = useAppDispatch();

    const handleLogout = () => {
        dispatch(logout());
        navigate("/login");
    };

    const items = [
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

    console.log("Render MainHeader");

    return (
        <div className="flex justify-between items-center">
            <div className="flex items-center space-x-3">
                <EnvironmentOutlined className="!text-purple-500 text-3xl" />
                <h1
                    className="cursor-pointer text-lg font-semibold"
                    onClick={() => navigate("/dashboard")}
                >
                    {t("dashboard.nav.appName")}
                </h1>
            </div>
            <DropdownHeader
                username={username}
                t={t}
                items={items}
                handleLogout={handleLogout}
                isInMainHeader={true}
            />
        </div>
    );
};

export default MainHeader;
