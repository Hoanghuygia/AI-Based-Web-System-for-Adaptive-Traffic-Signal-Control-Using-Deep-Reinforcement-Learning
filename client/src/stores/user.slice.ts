import { UserState } from "./states/UserState"
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { login as loginApi } from "@src/api/auth";
import { register as registerApi } from "@src/api/auth";
import { signInWithPopup } from "firebase/auth";
import { auth, googleProvider } from "@src/config/firebase";

const initialUserState: UserState = {
    currentUser: null,
    photoURL: null,
    email: null,
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

export const loginWithGoogle = createAsyncThunk(
    'user/loginWithGoogle',
    async (_, { rejectWithValue }) => {
        try {
            const result = await signInWithPopup(auth, googleProvider);
            const user = result.user;
            const idToken = await user.getIdToken(); 

            return {
                user: {
                    uid: user.uid,
                    name: user.displayName,
                    email: user.email,
                    photoURL: user.photoURL,
                },
                token: idToken,
                refreshToken: user.refreshToken, 
            };
        } catch (error: any) {
            console.error("Google login error:", error);
            return rejectWithValue(error.message);
        }
    }
);

export const register = createAsyncThunk(
    'user/register',
    async (credential: {
        username: string;
        password: string
    }) => {
        const response = await registerApi({ user: credential });
        return response.data;
    }
)

export const userSlice = createSlice({
    name: 'user',
    initialState: initialUserState,
    reducers: {
        logout: (state) => {
            console.log("User logged out");
            state.currentUser = null;
            state.photoURL = null;
            state.email = null;
            state.token = null;
            state.refreshToken = null;
            localStorage.removeItem('username');
            localStorage.removeItem('photoURL');
            localStorage.removeItem('email');
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
                localStorage.setItem('username', username);
            })
            .addCase(login.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || "Login failure"
            })
            .addCase(register.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(register.fulfilled, (_, action) => {
                console.log("payload", action.payload);
                console.log("Register successfully");
            })
            .addCase(register.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || "Register failure"
            })
            .addCase(loginWithGoogle.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(loginWithGoogle.fulfilled, (state, action) => {
                state.loading = false;
                state.error = null;

                const { user, token, refreshToken } = action.payload;

                state.currentUser = user.name;
                state.token = token;
                state.refreshToken = refreshToken;

                localStorage.setItem('token', token);
                localStorage.setItem('refresh-token', refreshToken);
                localStorage.setItem('username', user.name ?? '');
                localStorage.setItem('email', user.email ?? '');
                localStorage.setItem('photoURL', user.photoURL ?? '');
            })
            .addCase(loginWithGoogle.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string || "Google login failed";
            });
    }
})

export const { logout, setUser } = userSlice.actions;
export default userSlice.reducer;