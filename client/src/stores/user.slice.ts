import { UserState } from "./states/UserState"
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { login as loginApi } from "@src/api/auth";

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
            .addCase(login.fulfilled, (state, action) => {
                console.log("Login payload:", action.payload);
                const { username, token, refresh_token } = action.payload.user;

                state.loading = false;
                state.currentUser = username; 
                state.token = token;
                state.refreshToken = refresh_token;

                localStorage.setItem('token', token);
                localStorage.setItem('refresh-token', refresh_token);
            })
            .addCase(login.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || "Login failure"
            })
    }
})

export const {logout, setUser} = userSlice.actions;
export default userSlice.reducer;