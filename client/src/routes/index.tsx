import { JSX, lazy, SuspenseProps } from "react";
import { Navigate, RouteObject } from "react-router-dom";

const Auth = lazy(() => import('@pages/login'));

const RequireAuth = ({children}: {children: JSX.Element}) => {
    const token = localStorage.getItem('token');

    if(!token){
        return <Navigate to="/login" replace/>;
    }
    return children;
}

const routes: RouteObject[] = [
    {
        path: '/',
        element: (
            <Auth/>
        )
    }
];

export default routes;