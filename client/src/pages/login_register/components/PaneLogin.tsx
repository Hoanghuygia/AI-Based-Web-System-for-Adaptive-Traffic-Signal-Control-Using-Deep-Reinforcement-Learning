import React from "react";
import { Button } from "antd";

type PanelLoginProps = {
    resetStateInput: (value: boolean) => void;
};

const PanelLogin: React.FC<PanelLoginProps> = ({
    resetStateInput,
}) => {
    return (
        <div className="absolute inset-0 flex flex-col items-center justify-center text-white text-center bg-purple-500 p-6">
            <h1 className="text-2xl font-bold mb-2">
                Hello, Welcome!
            </h1>
            <p className="mb-4">Don't have an account?</p>
            <Button
                type="default"
                onClick={() => resetStateInput(true)}
                className="!bg-purple-500 !text-white !border-white hover:!bg-white hover:!text-purple-500 hover:!border-purple-500 transition duration-300"
            >
                Register
            </Button>
        </div>
    );
};

export default PanelLogin;
