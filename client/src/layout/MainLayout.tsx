import React from "react";
import { Outlet } from "react-router-dom";
import { Layout, Menu, Button } from "antd";
const { Header, Sider, Content, Footer } = Layout;
import {
    EnvironmentOutlined,
    MenuOutlined,
} from "@ant-design/icons";
import { useAppSelector } from "@src/stores/hooks";
import MainHeader from "@src/layout/components/MainHeader";

type MainLayoutPros = {
    children?: React.ReactNode;
};

const MainLayout: React.FC<MainLayoutPros> = ({
    children,
}) => {
    const username = useAppSelector(
        (state) => state.user.currentUser
    );
    console.log("Username: " + username);

    return (
        <Layout className="h-dvh">
            <Header className="bg-white shadow-md sticky top-0 z-50 ">
                <MainHeader username={username} />
            </Header>
            <div id="container-a" className="my-8 px-12">
                <Layout className="w-full">
                    <Sider
                        width={200}
                        className="bg-white shadow-md"
                        breakpoint="lg"
                        collapsedWidth="0"
                    >
                        <Menu
                            theme="dark"
                            mode="inline"
                            defaultSelectedKeys={["1"]}
                            items={[
                                {
                                    key: "1",
                                    label: "Dashboard",
                                },
                                {
                                    key: "2",
                                    label: "Settings",
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
