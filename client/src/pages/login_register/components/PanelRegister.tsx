import React from "react";
import { Button } from "antd";
import { useTranslation } from "react-i18next";

type PanelRegisterProps = {
    resetStateInput: (value: boolean) => void;
};

const PanelRegister: React.FC<PanelRegisterProps> = ({
    resetStateInput,
}) => {
    const { t } = useTranslation();
    console.log("Render PanelRegister");
    return (
        <div className="absolute inset-0 flex flex-col items-center justify-center text-white text-center bg-purple-500 p-6">
            <h1 className="text-2xl font-bold mb-2">
                {t("login-register.welcome-back")}
            </h1>
            <p className="mb-4">{t("login-register.already-have-an-account")}</p>
            <Button
                type="default"
                onClick={() => resetStateInput(false)}
                className="!bg-purple-500 !text-white !border-white hover:!bg-white hover:!text-purple-500 hover:!border-purple-500 transition duration-300"
            >
                Login
            </Button>
        </div>
    );
};

export const MemoizedPanelRegister = React.memo(PanelRegister);
