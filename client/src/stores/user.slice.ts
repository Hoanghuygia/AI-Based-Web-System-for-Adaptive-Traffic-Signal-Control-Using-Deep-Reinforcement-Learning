import { UserState } from "./states/UserState"
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { login as loginApi } from "@src/api/auth";
import { register as registerApi} from "@src/api/auth";

const initialUserState: UserState = {
    currentUser: null,
    token: localStorage.getItem("token"),
    refreshToken: localStorage.getItem('refresh-token'),
    loading: false,
    error: null
}

export const login = createAsyncThunk(
    'user/login',
    async (credential: {
        username: string;
        password: string
    }) => {
        const response = await loginApi({ user: credential });
        return response.data;
    }
)

export const register = createAsyncThunk(
    'user/register',
    async(credential: {
        username: string;
        password: string
    }) => {
        console.log("Register credential: ", credential);
        const response = await registerApi(credential);
        return response.data;
    }
)

export const userSlice = createSlice({
    name: 'user',
    initialState: initialUserState,
    reducers: {
        logout: (state) => {
            state.currentUser = null;
            state.token = null;
            state.refreshToken = null;
            localStorage.removeItem('token');
            localStorage.removeItem('refresh-token');
        },
        setUser: (state, action) => {
            state.currentUser = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(login.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(register.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(login.fulfilled, (state, action) => {
                console.log("Login payload:", action.payload);
                const { username, token, refresh_token } = action.payload.user;

                state.loading = false;
                state.currentUser = username; 
                state.token = token;
                state.refreshToken = refresh_token;

                localStorage.setItem('token', token);
                localStorage.setItem('refresh-token', refresh_token);
                localStorage.setItem('username', username);
            })
            .addCase(register.fulfilled, (_, action)=> {
                console.log("payload", action.payload);
                console.log("Register successfully");
            })
            .addCase(login.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || "Login failure"
            })
            .addCase(register.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || "Register failure"
            })
    }
})

export const {logout, setUser} = userSlice.actions;
export default userSlice.reducer;