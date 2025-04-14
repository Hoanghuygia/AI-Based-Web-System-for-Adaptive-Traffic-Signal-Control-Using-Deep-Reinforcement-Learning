import React, { useState } from "react";
import { Input, Button } from "antd";
import {
    UserOutlined,
    LockOutlined,
    MailOutlined,
    GoogleOutlined,
    GithubOutlined,
    FacebookOutlined,
    LinkedinOutlined,
    LinkedinFilled,
    FacebookFilled,
} from "@ant-design/icons";
// import "tailwindcss/tailwind.css";

const Auth: React.FC = () => {
    const [isRegistering, setIsRegistering] = useState(false);

    return (
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-gray-200 to-indigo-200">
            <div className="relative w-full max-w-4xl h-[550px] bg-white shadow-2xl rounded-3xl overflow-hidden">
                {/* Form Container */}
                <div
                    className={`absolute w-1/2 h-full p-10 transition-all duration-700 ${
                        isRegistering
                            ? "-right-full opacity-0"
                            : "right-0 opacity-100"
                    }`}
                >
                    <h1 className="text-3xl font-bold mb-4">Login</h1>
                    <div className="mb-4">
                        <Input
                            size="large"
                            placeholder="Username"
                            prefix={<UserOutlined />}
                        />
                    </div>
                    <div className="mb-4">
                        <Input.Password
                            size="large"
                            placeholder="Password"
                            prefix={<LockOutlined />}
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
                    <Button type="primary" block size="large" className="mb-4">
                        Login
                    </Button>
                    <p className="text-sm text-gray-500 text-center mb-2">
                        or login with social platforms
                    </p>
                    <div className="flex justify-center space-x-4">
                        <a
                            href="#"
                            className="p-3 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-red-500 transition"
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

                {/* Register Form */}
                <div
                    className={`absolute w-1/2 h-full p-10 transition-all duration-700 ${
                        isRegistering
                            ? "left-0 opacity-100"
                            : "left-full opacity-0"
                    }`}
                >
                    <h1 className="text-3xl font-bold mb-4">Register</h1>
                    <div className="mb-4">
                        <Input
                            size="large"
                            placeholder="Username"
                            prefix={<UserOutlined />}
                        />
                    </div>
                    <div className="mb-4">
                        <Input
                            size="large"
                            placeholder="Email"
                            prefix={<MailOutlined />}
                        />
                    </div>
                    <div className="mb-4">
                        <Input.Password
                            size="large"
                            placeholder="Password"
                            prefix={<LockOutlined />}
                        />
                    </div>
                    <Button type="primary" block size="large" className="mb-4">
                        Register
                    </Button>
                    <p className="text-sm text-gray-500 text-center mb-2">
                        or register with social platforms
                    </p>
                    <div className="flex justify-center space-x-4">
                        <a
                            href="#"
                            className="p-3 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-red-500 transition"
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

                {/* Toggle Panel */}
                <div className="absolute w-full h-full flex z-10">
                    <div
                        className={`w-1/2 h-full flex flex-col items-center justify-center text-white text-center bg-indigo-400 p-6 transition-all duration-700 ${
                            isRegistering
                                ? "-translate-x-full opacity-0"
                                : "translate-x-0 opacity-100"
                        }`}
                    >
                        <h1 className="text-2xl font-bold mb-2">
                            Hello, Welcome!
                        </h1>
                        <p className="mb-4">Don't have an account?</p>
                        <Button
                            onClick={() => setIsRegistering(true)}
                            className="border-white text-white bg-indigo-400"
                        >
                            Register
                        </Button>
                    </div>
                    <div
                        className={`w-1/2 h-full flex flex-col items-center justify-center text-white text-center bg-indigo-400 p-6 transition-all duration-700 ${
                            isRegistering
                                ? "translate-x-0 opacity-100"
                                : "translate-x-full opacity-0"
                        }`}
                    >
                        <h1 className="text-2xl font-bold mb-2">
                            Welcome Back!
                        </h1>
                        <p className="mb-4">Already have an account?</p>
                        <Button
                            onClick={() => setIsRegistering(false)}
                            className="border-white text-white bg-indigo-400"
                        >
                            Login
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Auth;
