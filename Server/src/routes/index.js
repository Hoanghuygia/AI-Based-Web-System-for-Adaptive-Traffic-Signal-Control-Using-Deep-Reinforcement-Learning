import { userRoute } from './userRoute.js';


export function route(app){
    app.use('/user', userRoute);
}
