import { Layout, Menu } from "antd";
const { Sider } = Layout;
import {
    DashboardOutlined,
    BarChartOutlined,
    SettingOutlined,
    ApartmentOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

type MainSiderProps = {
    selectedKey: string;
};

const MainSider: React.FC<MainSiderProps> = ({
    selectedKey,
}) => {
    const navigate = useNavigate();

    console.log("Render MainSider", selectedKey);

    return (
        <Sider
            width={260}
            className="bg-purple-500 shadow-md !rounded-xl"
            breakpoint="lg"
            collapsedWidth="0"
        >
            <Menu
                theme="dark"
                mode="inline"
                className="text-white font-semibond bg-purple-500 pt-6 px-4 !rounded-lg"
                selectedKeys={[selectedKey]}
                onClick={({ key }) => navigate(`/${key}`)}
                items={[
                    {
                        type: "group",
                        label: "OVERVIEW",
                        children: [
                            {
                                key: "dashboard",
                                icon: <DashboardOutlined />,
                                label: "Dashboard",
                            },
                            {
                                key: "analytics",
                                icon: <BarChartOutlined />,
                                label: "Analytics",
                            },
                        ],
                    },
                    {
                        type: "group",
                        label: "MANAGEMENT",
                        children: [
                            {
                                key: "junctions",
                                icon: <ApartmentOutlined />,
                                label: "Junctions",
                            },
                            {
                                key: "settings",
                                icon: <SettingOutlined />,
                                label: "System Settings",
                            },
                        ],
                    },
                ]}
            />
        </Sider>
    );
};

export default MainSider;
