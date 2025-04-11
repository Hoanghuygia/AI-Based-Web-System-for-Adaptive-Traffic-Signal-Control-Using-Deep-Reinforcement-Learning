import axios from 'axios';

interface LoginParam{
    username: string;
    password: string;
}

export function login(param: LoginParam){
    return axios.post('/api/login', param);
}