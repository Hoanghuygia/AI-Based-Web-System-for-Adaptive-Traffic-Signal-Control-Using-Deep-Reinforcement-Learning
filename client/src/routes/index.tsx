import Test from "@src/components/Test";
import EmptyLayout from "@src/layout/EmptyLayout";
import NotFoundPage from "@src/pages/error";
import { JSX, lazy, Suspense } from "react";
import { Navigate, RouteObject } from "react-router-dom";

const Auth = lazy(() => import('@src/pages/login_register'));
const LoadingPage = lazy(() => import('@src/pages/loading'));

const RequireAuth = ({children}: {children: JSX.Element}) => {
    const token = localStorage.getItem('token');
    console.log("Token: ", token);

    if(!token){
        return <Navigate to="/login" replace/>;
    }
    return children;
}

/*
Use for testing purpose 
*/
const routes: RouteObject[] = [
    {
        path: '/',
        element: (
            // <Auth/>
            <NotFoundPage/>
        )
    },
];

export default routes;

// const routes: RouteObject[] = [
    // {
        // path: '/',
        // element: (
        //     <RequireAuth>
        //         <EmptyLayout/>
        //     </RequireAuth>
        // ),
        // children: [
        //     {path: '', element: <Navigate to= "/test" replace />},
        //     {path: 'test', element: (
        //         <Suspense fallback={<LoadingPage/>}>
        //             <Test/>
        //         </Suspense>
        //     )}
        // ]
    // },
    // {
    //     path: '/login',
    //     element: <EmptyLayout/>,
    //     children: [
    //         {
    //             path: '',
    //             element: (
    //                 <Suspense fallback={<LoadingPage/>}>
    //                     <Auth/>
    //                 </Suspense>
    //             )
    //         }
    //     ]
    // }
// ];

// export default routes;