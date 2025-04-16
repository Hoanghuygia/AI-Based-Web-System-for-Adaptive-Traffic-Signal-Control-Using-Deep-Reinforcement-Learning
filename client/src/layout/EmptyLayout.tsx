import { Layout } from "antd";
import { Content } from "antd/es/layout/layout";
import { Outlet } from "react-router-dom";

const EmptyLayout: React.FC = () => {
    return (
        <Layout style={{ minHeight: "100vh" }}>
            <Content
                style={{
                    height: "100%",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    background: 'white'
                }}
            >
                <Outlet />
            </Content>
        </Layout>
    );
};

export default EmptyLayout;
