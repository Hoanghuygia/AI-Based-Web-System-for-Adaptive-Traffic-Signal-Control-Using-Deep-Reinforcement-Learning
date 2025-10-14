import React from "react";
import { Outlet } from "react-router-dom";
import { Layout, Menu } from "antd";
const { Header, Sider, Content } = Layout;
import { useAppSelector } from "@src/stores/hooks";
import MainHeader from "@src/layout/components/MainHeader";
import {
    DashboardOutlined,
    BarChartOutlined,
    SettingOutlined,
    ApartmentOutlined,
} from "@ant-design/icons";

type MainLayoutPros = {
    children?: React.ReactNode;
};

const MainLayout: React.FC<MainLayoutPros> = ({
    children,
}) => {
    const username = useAppSelector(
        (state) => state.user.currentUser
    );

    return (
        <Layout className="h-dvh">
            <Header className="bg-white shadow-md sticky top-0 z-50 ">
                <MainHeader username={username} />
            </Header>
            <div id="container-a" className="my-8 px-12 h-full">
                <Layout className="w-full h-full">
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
                            defaultSelectedKeys={["1"]}
                            items={[
                                {
                                    type: "group",
                                    label: "OVERVIEW",
                                    children: [
                                        {
                                            key: "dashboard",
                                            icon: (
                                                <DashboardOutlined />
                                            ),
                                            label: "Dashboard",
                                        },
                                        {
                                            key: "analytics",
                                            icon: (
                                                <BarChartOutlined />
                                            ),
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
                                            icon: (
                                                <ApartmentOutlined />
                                            ),
                                            label: "Junctions",
                                        },
                                        {
                                            key: "system",
                                            icon: (
                                                <SettingOutlined />
                                            ),
                                            label: "System Settings",
                                        },
                                    ],
                                },
                            ]}
                        />
                    </Sider>
                    <Content className="p-4 bg-gray-100">
                        {children || <Outlet />}
                    </Content>
                </Layout>
            </div>
        </Layout>
    );
};

export default MainLayout;
