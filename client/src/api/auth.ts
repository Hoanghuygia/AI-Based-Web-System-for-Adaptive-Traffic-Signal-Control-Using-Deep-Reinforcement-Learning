import axiosInstanceAuth from '@src/config/axiosAuth';
import { LoginParam } from './ParamsInterface/LoginParams';
import { RegisterParam } from './ParamsInterface/RegisterParam';

export function login(param: LoginParam){
    return axiosInstanceAuth.post('/login', param);
}

export function register(param: RegisterParam){
    return axiosInstanceAuth.post('/register', param);
}