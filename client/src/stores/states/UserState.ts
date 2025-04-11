export interface UserState {
    currentUser: any | null;
    token: string | null;
    refreshToken: string | null;
    loading: boolean | null;
    error: string | null;
}