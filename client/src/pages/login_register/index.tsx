import { useState } from "react";
import LoginForm from "./components/LoginForm";
import PanelLogin from "./components/PaneLogin";
import RegisterForm from "./components/RegisterForm";
import PanelRegister from "./components/PanelRegister";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "@src/stores";
import { login, register } from "@src/stores/user.slice";
import { useNavigate } from "react-router-dom";

const Auth = () => {
  const [isRegistering, setIsRegistering] = useState(false);

  // Login states
  const [loginUsername, setLoginUsername] = useState("");
  const [loginPassword, setLoginPassword] = useState("");

  // Register states
  const [registerUsername, setRegisterUsername] = useState("");
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");

  // redx
  const dispatch = useDispatch<AppDispatch>();
  // const { currentUser, loading, error, token, refreshToken } = useSelector((state: RootState) => state.user);

  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      console.log("Login with: ", loginUsername, loginPassword);
      const result = await dispatch(login({
        username: loginUsername,
        password: loginPassword
      })).unwrap(); 
      
      if (result) { 
        console.log("Navigate to test");
        navigate('/test');
      }
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  const handleRegister = async () => {
    try {
      console.log("Register with: ", registerUsername, registerEmail, registerPassword);
      const result = await dispatch(register({
        username: registerUsername,
        password: registerPassword
      })).unwrap(); 
      
      if (result) { 
        console.log("Navigate to login");
        resetStateInput(false);
        // navigate('/login');
      }
    } catch (error) {
      console.error('Register failed:', error);
    }
  };

  const resetStateInput = (isRegistering: boolean) => {
    console.log("Resetl all state: ");
    setIsRegistering(isRegistering);
    setLoginPassword("");
    setLoginUsername("");
    setRegisterEmail("");
    setRegisterPassword("");
    setRegisterUsername("");
  }

  return (
    // <div className="w-full h-full flex items-center justify-center min-h-screen bg-gradient-to-r from-gray-200 to-indigo-200">
      <div className="relative w-full max-w-4xl h-[550px] bg-white shadow-2xl rounded-3xl overflow-hidden">
        <div className="flex h-full">
          <div className="w-1/2 h-full relative">
            {/* Panel Login */}
            <div className={`transition-all duration-700 ${isRegistering ? "opacity-0 pointer-events-none" : "opacity-100"}`}>
              <PanelLogin resetStateInput={resetStateInput} />
            </div>

            {/* Register Form */}
            <div className={`transition-all duration-700 ${isRegistering ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"}`}>
              <RegisterForm
                registerUsername={registerUsername}
                setRegisterUsername={setRegisterUsername}
                registerEmail={registerEmail}
                setRegisterEmail={setRegisterEmail}
                registerPassword={registerPassword}
                setRegisterPassword={setRegisterPassword}
                handleRegister={handleRegister}
              />
            </div>
          </div>

          <div className="w-1/2 h-full relative">
            {/* Panel Register */}
            <div className={`transition-all duration-700 ${isRegistering ? "opacity-100" : "opacity-0 pointer-events-none"}`}>
              <PanelRegister resetStateInput={resetStateInput} />
            </div>

            {/* Login Form */}
            <div className={`transition-all duration-700 ${isRegistering ? "opacity-0 pointer-events-none" : "opacity-100 pointer-events-auto"}`}>
              <LoginForm
                loginUsername={loginUsername}
                setLoginUsername={setLoginUsername}
                loginPassword={loginPassword}
                setLoginPassword={setLoginPassword}
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