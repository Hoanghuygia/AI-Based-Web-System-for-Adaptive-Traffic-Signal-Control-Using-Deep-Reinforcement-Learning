import { use, useCallback, useState } from "react";
import {MemoizedLoginForm} from "./components/LoginForm";
import {MemoizedPanelLogin} from "./components/PaneLogin";
import {MemoizedRegisterForm} from "./components/RegisterForm";
import {MemoizedPanelRegister} from "./components/PanelRegister";
import { login, register } from "@src/stores/user.slice";
import { useNavigate } from "react-router-dom";
import { useAppDispatch } from "@src/stores/hooks";

const Auth = () => {
    const [isRegistering, setIsRegistering] =
        useState(false);

    // Login states
    const [loginUsername, setLoginUsername] = useState("");
    const [loginPassword, setLoginPassword] = useState("");

    // Register states
    const [registerUsername, setRegisterUsername] =
        useState("");
    const [registerEmail, setRegisterEmail] = useState("");
    const [registerPassword, setRegisterPassword] =
        useState("");

    // redx
    const dispatch = useAppDispatch();

    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const result = await dispatch(
                login({
                    username: loginUsername,
                    password: loginPassword,
                })
            ).unwrap();

            if (result) {
                console.log("Navigate to Dashboard");
                navigate("/dashboard");
            }
        } catch (error) {
            console.error("Login failed:", error);
        }
        console.log("Navigate to Dashboard");
        navigate("/dashboard");
    };

    const handleRegister = async () => {
        try {
            const result = await dispatch(
                register({
                    username: loginUsername,
                    password: loginPassword,
                })
            ).unwrap();

            if (result) {
                console.log("Navigate to login");
                navigate("/login");
            }
        } catch (error) {
            console.error("Register failed:", error);
        }
    };

    const resetStateInput = useCallback((isRegistering: boolean)=> {
        console.log("Resetl all state: ");
        setIsRegistering(isRegistering);
        setLoginPassword("");
        setLoginUsername("");
        setRegisterEmail("");
        setRegisterPassword("");
        setRegisterUsername("");
    }, [])

    return (
        <div className="relative w-full max-w-4xl h-[550px] bg-white shadow-2xl rounded-3xl overflow-hidden">
            {/*Can be merged, 1 for layout, 1 for style, easier to maintain */}
            <div className="flex h-full"> 
                <div className="w-1/2 h-full relative">
                    {/* Panel Login */}
                    <div
                        className={`transition-all duration-700 ${
                            isRegistering
                                ? "opacity-0 pointer-events-none"
                                : "opacity-100"
                        }`}
                    >
                        <MemoizedPanelLogin
                            resetStateInput={
                                resetStateInput
                            }
                        />
                    </div>

                    {/* Register Form */}
                    <div
                        className={`transition-all duration-700 ${
                            isRegistering
                                ? "opacity-100 pointer-events-auto"
                                : "opacity-0 pointer-events-none"
                        }`}
                    >
                        <MemoizedRegisterForm
                            registerUsername={
                                registerUsername
                            }
                            setRegisterUsername={
                                setRegisterUsername
                            }
                            registerEmail={registerEmail}
                            setRegisterEmail={
                                setRegisterEmail
                            }
                            registerPassword={
                                registerPassword
                            }
                            setRegisterPassword={
                                setRegisterPassword
                            }
                            handleRegister={handleRegister}
                        />
                    </div>
                </div>

                <div className="w-1/2 h-full relative">
                    {/* Panel Register */}
                    <div
                        className={`transition-all duration-700 ${
                            isRegistering
                                ? "opacity-100"
                                : "opacity-0 pointer-events-none"
                        }`}
                    >
                        <MemoizedPanelRegister
                            resetStateInput={
                                resetStateInput
                            }
                        />
                    </div>

                    {/* Login Form */}
                    <div
                        className={`transition-all duration-700 ${
                            isRegistering
                                ? "opacity-0 pointer-events-none"
                                : "opacity-100 pointer-events-auto"
                        }`}
                    >
                        <MemoizedLoginForm
                            loginUsername={loginUsername}
                            setLoginUsername={
                                setLoginUsername
                            }
                            loginPassword={loginPassword}
                            setLoginPassword={
                                setLoginPassword
                            }
                            handleLogin={handleLogin}
                        />
                    </div>
                </div>
            </div>
        </div>
        // </div>
    );
};

export default Auth;
