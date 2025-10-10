import { Layout } from "antd";
import React from "react";
import { Outlet } from "react-router-dom";

const { Content } = Layout;

type EmptyLayoutPros = {
    children?: React.ReactNode;
};

const EmptyLayout: React.FC<EmptyLayoutPros> = ({ children }) => {
    return (
        <Layout id="empty-layout" className="h-dvh bg-gradient-to-r from-customGray to-customIndigo">
            <Content className="flex justify-center items-center bg-transparent">
                {children || <Outlet />}
            </Content>
        </Layout>
    );
};

export default EmptyLayout;
