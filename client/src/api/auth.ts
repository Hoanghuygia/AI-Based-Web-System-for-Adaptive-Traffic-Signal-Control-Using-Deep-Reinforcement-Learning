import axiosInstanceAuth from '@src/config/axiosAuth';

interface LoginParam{
    username: string;
    password: string;
}

export function login(param: LoginParam){
    return axiosInstanceAuth.post('/login', param);
}