import LoadingPage from "@src/pages/loading";
import { getToken } from "@src/utils/authUtils";
import { JSX, lazy, Suspense } from "react";
import { Navigate, RouteObject } from "react-router-dom";

const Auth = lazy(() => import('@src/pages/login_register'));
const NotFoundPage = lazy(() => import('@src/pages/error'));
const Test = lazy(() => import('@src/components/Test'));
const EmptyLayout = lazy(() => import('@src/layout/EmptyLayout'));

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
    return token ? <Navigate to="/test" replace /> : children;
};

const routes: RouteObject[] = [
    {
        path: '/',
        element: (
            <AuthRoute>
                <Suspense fallback={<LoadingPage/>}>
                    <EmptyLayout/>
                </Suspense>
            </AuthRoute>
        ),
        children: [
            {path: '', element: <Navigate to= "/test" replace />},
            {path: 'test', element: (
                <Test/>
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
//         path: '/',
//         element: (
//             // <Auth/>
//             <NotFoundPage/>
//         )
//     },
// ];

// export default routes;