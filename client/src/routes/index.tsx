import MainLayout from "@src/layout/MainLayout";
import LoadingPage from "@src/pages/loading";
import { getToken } from "@src/utils/authUtils";
import { JSX, lazy, Suspense } from "react";
import { Navigate, RouteObject } from "react-router-dom";

const Auth = lazy(
    () => import("@src/pages/login_register")
);
const NotFoundPage = lazy(() => import("@src/pages/error"));
// const Test = lazy(() => import('@src/components/Test'));
const Dashboard = lazy(
    () => import("@src/pages/dashboard")
);
const EmptyLayout = lazy(
    () => import("@src/layout/EmptyLayout")
);

const AuthRoute = ({children}: {children: JSX.Element}) => {

    // need to check if the token is valid or expired or not
    // using api
    const token = getToken();
    console.log("Token: ", token);

    if(!token){
        return <Navigate to="/login" replace/>;
    }
    return children;
}

const GuestRoute = ({ children }: { children: JSX.Element }) => {
    const token = getToken()
    return token ? <Navigate to="/dashboard" replace /> : children;
};

const routes: RouteObject[] = [
    {
        path: '/',
        element: (
            <AuthRoute>
                <Suspense fallback={<LoadingPage/>}>
                    <MainLayout/>
                </Suspense>
            </AuthRoute>
        ),
        children: [
            {path: '', element: <Navigate to= "/dashboard" replace />},
            {path: 'dashboard', element: (
                <Dashboard/>
            )}
        ]
    },
    {
        path: '/login',
        element: <EmptyLayout/>,
        children: [
            {
                path: '',
                element: (
                    <GuestRoute>
                        <Suspense fallback={<LoadingPage/>}>
                            <Auth/>
                        </Suspense>
                    </GuestRoute>
                )
            }
        ]
    },
    {
        path: '*',
        element: (
            <EmptyLayout>
                <Suspense fallback={<LoadingPage />}>
                    <NotFoundPage />
                </Suspense>
            </EmptyLayout>
        ),

    }
];

export default routes;

/*
Use for testing purpose 
*/
// const routes: RouteObject[] = [
//     {
//         path: "/",
//         element: (
//             <EmptyLayout>
//                 <Suspense fallback={<LoadingPage />}>
//                     {/* <Auth/> */}
//                     {/* <NotFoundPage /> */}
//                     <Dashboard />
//                 </Suspense>
//             </EmptyLayout>
//         ),
//     },
// ];

// export default routes;
