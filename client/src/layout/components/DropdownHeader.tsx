import { Button, Dropdown } from 'antd';
import { MenuOutlined } from "@ant-design/icons";

type DropdownHeaderPRos = {
    username: string | null;
    t: (key: string) => string;
    items: { key: string; label: string }[];
    handleLogout: () => void;
    isInMainHeader?: boolean;
}

const DropdownHeader: React.FC<DropdownHeaderPRos> = ({
    username,
    t,
    items,
    handleLogout,
    isInMainHeader = false,
}) => {
    return (
         <div className="flex items-center space-x-6">
                {isInMainHeader && (
                    <span className="text-gray-600">
                        {t("dashboard.nav.welcome")}, {username}
                    </span>
                )}

                <button className="cursor-pointer flex items-center justify-self-center h-8 px-4 rounded-md text-gray-600 hover:text-gray-800 hover:bg-gray-200">
                    {t("dashboard.nav.notification")}
                </button>

                <Dropdown
                    menu={{
                        items,
                        onClick: ({ key }) => {
                            if (key === "3") {
                                handleLogout();
                            } else if (key === "1") {
                                // navigate("/profile");
                            } else if (key === "2") {
                                // navigate("/settings");
                            }
                        },
                    }}
                    overlayClassName="custom-dropdown-mainheader"
                    placement="bottomRight"
                    trigger={["click"]}
                >
                    <Button
                        type="text"
                        icon={<MenuOutlined />}
                    />
                </Dropdown>
            </div>
    );
};

export default DropdownHeader;