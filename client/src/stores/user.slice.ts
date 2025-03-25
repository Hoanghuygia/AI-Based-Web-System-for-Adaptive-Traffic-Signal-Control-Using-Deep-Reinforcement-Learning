import { Locale } from '../App';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserState{
    logged: boolean,
    username: string,
    role: string,
    token: string,
    locale: Locale,
}

const initialState: UserState = {
    logged: false,
    username: '',
    role: '',
    token: '',
    locale: 'en_US',
}

const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers:{
         setLocale: (state, action: PayloadAction<Locale>) => {
            state.locale = action.payload
         }
    }
})

export const {setLocale} = userSlice.actions;
export default userSlice.reducer;