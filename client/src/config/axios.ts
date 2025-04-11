import { message } from "antd";
import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL || '/api';

const axiosInstance = axios.create({
    baseURL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
})

axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if(token){
            config.headers.Authorization = `Token ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
)

axiosInstance.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        const {response} = error;

        if(response){
            switch(response.status){
                case 401:
                    message.error('Unauthorized, please login again!')
                    break;
                case 403: 
                    message.error("Forbidden access");
                    break;
                case 404: 
                    message.error("Resource not found")
                    break;
                case 500:
                    message.error("Server error, please try again later");
                    break;
                default:
                    message.error(response.data.message || "Something went wrong")
            }
        }
        else{
            message.error("Network error, check connection")
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;