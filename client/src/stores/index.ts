import { configureStore } from "@reduxjs/toolkit";
import userReducer from './user.slice'; // ưe can name it anything with the export default, since each file only one export default

export const store = configureStore({
    reducer: {
        user: userReducer
    },
    devTools: process.env.NODE_ENV !== 'production',
})

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;