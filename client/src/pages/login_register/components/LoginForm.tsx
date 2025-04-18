import React from "react";
import { Input, Button } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";

type LoginFormProps = {
    loginUsername: string;
    setLoginUsername: (value: string) => void;
    loginPassword: string;
    setLoginPassword: (value: string) => void;
    handleLogin: () => void;
};

const LoginForm: React.FC<LoginFormProps> = ({
    loginUsername,
    setLoginUsername,
    loginPassword,
    setLoginPassword,
    handleLogin,
}) => {
    return (
        <div className="p-10">
            <h1 className="text-3xl font-bold mb-4">Login</h1>
            <div className="mb-4">
                <Input
                    size="large"
                    placeholder="Username"
                    prefix={<UserOutlined />}
                    value={loginUsername}
                    onChange={(e) => setLoginUsername(e.target.value)}
                />
            </div>
            <div className="mb-4">
                <Input.Password
                    size="large"
                    placeholder="Password"
                    prefix={<LockOutlined />}
                    value={loginPassword}
                    onChange={(e) => setLoginPassword(e.target.value)}
                />
            </div>
            <div className="mb-2 text-right">
                <a
                    href="#"
                    className="text-sm text-gray-500 hover:text-indigo-600"
                >
                    Forgot Password?
                </a>
            </div>
            <Button
                type="primary"
                block
                size="large"
                className="mb-4"
                onClick={handleLogin}
            >
                Login
            </Button>
            <p className="text-sm text-gray-500 text-center mb-2">
                or login with social platforms
            </p>
            <div className="flex justify-center space-x-4">
                <a
                    href="#"
                    className="px-3 py-2.5 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-red-500 transition"
                >
                    <i className="bx bxl-google"></i>
                </a>
                <a
                    href="#"
                    className="p-3 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-blue-600 transition"
                >
                    <i className="bx bxl-facebook"></i>
                </a>
                <a
                    href="#"
                    className="p-3 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-black transition"
                >
                    <i className="bx bxl-github"></i>
                </a>
                <a
                    href="#"
                    className="p-3 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-blue-700 transition"
                >
                    <i className="bx bxl-linkedin"></i>
                </a>
            </div>
        </div>
    );
};

export default LoginForm;
