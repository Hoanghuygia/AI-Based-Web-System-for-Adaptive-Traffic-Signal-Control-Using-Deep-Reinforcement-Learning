import React from "react";
import { Input, Button } from "antd";
import {
    UserOutlined,
    LockOutlined,
    MailOutlined,
} from "@ant-design/icons";

type RegisterFormProps = {
    registerUsername: string;
    setRegisterUsername: (value: string) => void;
    registerEmail: string;
    setRegisterEmail: (value: string) => void;
    registerPassword: string;
    setRegisterPassword: (value: string) => void;
    handleRegister: () => void;
};

const RegisterForm: React.FC<RegisterFormProps> = ({
    registerUsername,
    setRegisterUsername,
    registerEmail,
    setRegisterEmail,
    registerPassword,
    setRegisterPassword,
    handleRegister,
}) => {
    return (
        <div className="p-10">
            <h1 className="text-3xl font-bold mb-4">
                Register
            </h1>
            <div className="mb-4">
                <Input
                    size="large"
                    placeholder="Username"
                    prefix={<UserOutlined />}
                    value={registerUsername}
                    onChange={(e) =>
                        setRegisterUsername(e.target.value)
                    }
                />
            </div>
            <div className="mb-4">
                <Input
                    size="large"
                    placeholder="Email"
                    prefix={<MailOutlined />}
                    value={registerEmail}
                    onChange={(e) =>
                        setRegisterEmail(e.target.value)
                    }
                />
            </div>
            <div className="mb-4">
                <Input.Password
                    size="large"
                    placeholder="Password"
                    prefix={<LockOutlined />}
                    value={registerPassword}
                    onChange={(e) =>
                        setRegisterPassword(e.target.value)
                    }
                />
            </div>
            <Button
                type="default"
                block
                size="large"
                className="mb-4 !bg-purple-500 !text-white !border-white hover:!bg-white hover:!text-purple-500 hover:!border-purple-500 transition duration-300"
                onClick={handleRegister}
            >
                Register
            </Button>

            <p className="text-sm text-gray-500 text-center mb-2">
                or register with social platforms
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
                    className="px-3 py-2.5 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-blue-600 transition"
                >
                    <i className="bx bxl-facebook"></i>
                </a>
                <a
                    href="#"
                    className="px-3 py-2.5 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-black transition"
                >
                    <i className="bx bxl-github"></i>
                </a>
                <a
                    href="#"
                    className="px-3 py-2.5 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-blue-700 transition"
                >
                    <i className="bx bxl-linkedin"></i>
                </a>
            </div>
        </div>
    );
};

export default RegisterForm;
