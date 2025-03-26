import React, { FC } from 'react'
import { Navigate, RouteObject, useRoutes } from "react-router-dom";
import LoginPage from '@pages/login'

// const routers: RouteObject[] = [
//     {
//         path: '/login',
//         // element: <LoginPage />  
//         element: React.createElement(LoginPage)
//     }
// ]

const routers: RouteObject[] = [
    {
        path: '/login',
        element: <LoginPage />  // Sử dụng trực tiếp component
    },
    {
        path: '/',  // Thêm route gốc
        element: <Navigate to="/login" />  // Chuyển hướng đến trang login mặc định
    }
]

const RenderRouter: FC = () => {
    const element = useRoutes(routers);
    return element;
}

export default RenderRouter;
