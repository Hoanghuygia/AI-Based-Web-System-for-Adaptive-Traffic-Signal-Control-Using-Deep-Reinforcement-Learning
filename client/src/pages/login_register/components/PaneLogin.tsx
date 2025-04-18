import React from "react";
import { Button } from "antd";

type PanelLoginProps = {
    resetStateInput: (value: boolean) => void;
}

const PanelLogin: React.FC<PanelLoginProps> = ({ resetStateInput }) => {
  return (
    <div className="absolute inset-0 flex flex-col items-center justify-center text-white text-center bg-indigo-400 p-6">
      <h1 className="text-2xl font-bold mb-2">Hello, Welcome!</h1>
      <p className="mb-4">Don't have an account?</p>
      <Button
        onClick={() => resetStateInput(true)}
        className="border-white text-white bg-indigo-400 hover:bg-indigo-500"
      >
        Register
      </Button>
    </div>
  );
};

export default PanelLogin;