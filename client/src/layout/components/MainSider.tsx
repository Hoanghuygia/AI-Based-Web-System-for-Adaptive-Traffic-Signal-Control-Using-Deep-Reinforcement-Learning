import { Layout, Menu } from "antd";
const { Sider } = Layout;
import {
    DashboardOutlined,
    BarChartOutlined,
    SettingOutlined,
    ApartmentOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

type MainSiderProps = {
    selectedKey: string;
};

const MainSider: React.FC<MainSiderProps> = ({
    selectedKey,
}) => {
    const navigate = useNavigate();
    const { t } = useTranslation();

    console.log("Render MainSider", selectedKey);

    return (
        <Sider
            width={260}
            className="bg-purple-500 shadow-md !rounded-l-lg"
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
                        label: t("dashboard.nav.overview"),
                        children: [
                            {
                                key: "dashboard",
                                icon: <DashboardOutlined />,
                                label: t("dashboard.nav.dashboard"),
                            },
                            {
                                key: "analytics",
                                icon: <BarChartOutlined />,
                                label: t("dashboard.nav.analytics"),
                            },
                        ],
                    },
                    {
                        type: "group",
                        label: t("dashboard.nav.management"),
                        children: [
                            {
                                key: "junctions",
                                icon: <ApartmentOutlined />,
                                label: t("dashboard.nav.junction"),
                            },
                            {
                                key: "settings",
                                icon: <SettingOutlined />,
                                label: t("dashboard.nav.systemSetting"),
                            },
                        ],
                    },
                ]}
            />
        </Sider>
    );
};

export default MainSider;
