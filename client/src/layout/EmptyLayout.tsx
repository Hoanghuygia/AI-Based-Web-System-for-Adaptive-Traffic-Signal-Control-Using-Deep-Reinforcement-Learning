import { Layout } from "antd";
import React from "react";
import { Outlet } from "react-router-dom";

const { Content } = Layout;

type EmptyLayoutPros = {
    children ?: React.ReactNode
};

const EmptyLayout: React.FC<EmptyLayoutPros> = ({children}) => {
  return (
    <Layout style={{ minHeight: "100vh", background: "linear-gradient(to right, #e5e7eb, #a5b4fc)"}}>
      <Content
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: "transparent", 
        }}
      >
        {children || <Outlet />}
      </Content>
    </Layout>
  );
};

export default EmptyLayout;

