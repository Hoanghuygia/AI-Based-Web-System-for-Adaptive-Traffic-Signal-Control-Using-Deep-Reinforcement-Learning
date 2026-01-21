import { Layout } from "antd";
import { Content, Header } from "antd/es/layout/layout";
import { Outlet } from "react-router-dom";
import JunctionDetailHeader from "./components/JunctionDetailHeader";

type DisplayLayoutPros = {
    children?: React.ReactNode;
}

const DisplayLayout: React.FC<DisplayLayoutPros> = ({
    children,
}) => {
    return (
        <Layout className="min-h-screen">
            <Header className="bg-white shadow-md sticky top-0 z-50 ">
                <JunctionDetailHeader/>
            </Header>
            <div id="container-a" className="my-8 px-12 h-full">
                <Layout className="w-full h-full">
                    <Content className="p-4 bg-gray-100">
                        {children || <Outlet />}
                    </Content>
                </Layout>
            </div>
        </Layout>
    );
}

export default DisplayLayout;