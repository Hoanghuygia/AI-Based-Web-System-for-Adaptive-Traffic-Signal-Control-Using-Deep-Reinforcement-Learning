import React from "react";
import { Outlet, useLocation } from "react-router-dom";
import { Layout } from "antd";
const { Header, Content } = Layout;
import { useAppSelector } from "@src/stores/hooks";
import MainHeader from "@src/layout/components/MainHeader";
import MainSider from "./components/MainSider";

type MainLayoutPros = {
    children?: React.ReactNode;
};

const MainLayout: React.FC<MainLayoutPros> = ({
    children,
}) => {
    const username = useAppSelector(
        (state) => state.user.currentUser
    );
    const location = useLocation();
    const selectedKey = location.pathname.replace('/', '') || 'dashboard';

    console.log("Render MainLayout")

    return (
        <Layout className="h-dvh">
            <Header className="bg-white shadow-md sticky top-0 z-50 ">
                <MainHeader username={username} />
            </Header>
            <div id="container-a" className="my-8 px-12 h-full">
                <Layout className="w-full h-full">
                    <MainSider selectedKey={selectedKey} />
                    <Content className="p-4 bg-gray-100">
                        {children || <Outlet />}
                    </Content>
                </Layout>
            </div>
        </Layout>
    );
};

export default MainLayout;
