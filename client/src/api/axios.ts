import axios from 'axios'
import {message} from 'antd'

const baseURL = import.meta.env.BASE_API_URL || '/apiv1'

const axiosInstance = axios.create({
    baseURL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor is thing that chặn request để edit trước khi gửi, response interceptor thì ngược lai
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token){
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        console.error('Request Error:', error);
        return Promise.reject(error);
    }
);

axiosInstance.interceptors.response.use(
    (response) => {
        return response
    },
    (error) => {
        const {response} = error;
        if(response){
            switch(response.status){
                case 401:
                    message.error('Unauthorized, please login again');
                    // redirect to login page
                    break;
                case 403:
                    message.error('Forbidden, you don\'t have permission to access this resource');
                    break;
                case 404:
                    message.error('Not Found, the requested resource could not be found');
                    break;
                case 500:
                    message.error('Server Error, please try again later');
                    break;
                default:
                    message.error(`Error ${response.status}: ${response.data.message}`);
                    break;
            }
        }
        else{
            message.error("Network Error, please check your connection and try again later.")
        }
        return Promise.reject(error);
    }
);