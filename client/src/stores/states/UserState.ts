export interface UserState {
    currentUser: any | null;
    photoURL: any | null;
    email: any | null;
    token: string | null;
    refreshToken: string | null;
    loading: boolean | null;
    error: string | null;
}