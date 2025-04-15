import React from "react";
import { Button } from "antd";

type PanelRegisterProps = {
    resetStateInput: (value: boolean) => void;
}

const PanelRegister: React.FC<PanelRegisterProps> = ({ resetStateInput }) => {
  return (
    <div className="absolute inset-0 flex flex-col items-center justify-center text-white text-center bg-indigo-400 p-6">
      <h1 className="text-2xl font-bold mb-2">Welcome Back!</h1>
      <p className="mb-4">Already have an account?</p>
      <Button
        onClick={() => resetStateInput(false)}
        className="border-white text-white bg-indigo-400 hover:bg-indigo-500"
      >
        Login
      </Button>
    </div>
  );
};

export default PanelRegister;