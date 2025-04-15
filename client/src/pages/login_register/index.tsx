// import React, { useState } from "react";
// import { Input, Button } from "antd";
// import { UserOutlined, LockOutlined, MailOutlined } from "@ant-design/icons";

// const Auth = () => {
//     const [isRegistering, setIsRegistering] = useState(false);

//     // Login states
//     const [loginUsername, setLoginUsername] = useState("");
//     const [loginPassword, setLoginPassword] = useState("");

//     // Register states
//     const [registerUsername, setRegisterUsername] = useState("");
//     const [registerEmail, setRegisterEmail] = useState("");
//     const [registerPassword, setRegisterPassword] = useState("");

//     // Handlers
//     const handleLogin = () => {
//         console.log("Login với:", {
//             username: loginUsername,
//             password: loginPassword,
//         });
//         alert(`Login with user: ${loginUsername}, ${loginPassword}`);
//     };

//     const handleRegister = () => {
//         console.log("Đăng ký với:", {
//             username: registerUsername,
//             email: registerEmail,
//             password: registerPassword,
//         });
//         alert(
//             `Đăng ký với: ${registerUsername}, ${registerEmail}, ${registerPassword}`
//         );
//     };

//     return (
//         <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-gray-200 to-indigo-200">
//             <div className="relative w-full max-w-4xl h-[550px] bg-white shadow-2xl rounded-3xl overflow-hidden">
//                 <div className="flex h-full">
//                     <div className="w-1/2 h-full relative">
//                         <div
//                             className={`absolute inset-0 flex flex-col items-center justify-center text-white text-center bg-indigo-400 p-6 transition-all duration-700 ${
//                                 isRegistering
//                                     ? "opacity-0 pointer-events-none"
//                                     : "opacity-100"
//                             }`}
//                         >
//                             <h1 className="text-2xl font-bold mb-2">
//                                 Hello, Welcome!
//                             </h1>
//                             <p className="mb-4">Don't have an account?</p>
//                             <Button
//                                 onClick={() => setIsRegistering(true)}
//                                 className="border-white text-white bg-indigo-400 hover:bg-indigo-500"
//                             >
//                                 Register
//                             </Button>
//                         </div>

//                         {/* Register Form */}
//                         <div
//                             className={`absolute inset-0 p-10 transition-all duration-700 ${
//                                 isRegistering
//                                     ? "opacity-100 pointer-events-auto"
//                                     : "opacity-0 pointer-events-none"
//                             }`}
//                         >
//                             <h1 className="text-3xl font-bold mb-4">
//                                 Register
//                             </h1>
//                             <div className="mb-4">
//                                 <Input
//                                     size="large"
//                                     placeholder="Username"
//                                     prefix={<UserOutlined />}
//                                     value={registerUsername}
//                                     onChange={(e) =>
//                                         setRegisterUsername(e.target.value)
//                                     }
//                                 />
//                             </div>
//                             <div className="mb-4">
//                                 <Input
//                                     size="large"
//                                     placeholder="Email"
//                                     prefix={<MailOutlined />}
//                                     value={registerEmail}
//                                     onChange={(e) =>
//                                         setRegisterEmail(e.target.value)
//                                     }
//                                 />
//                             </div>
//                             <div className="mb-4">
//                                 <Input.Password
//                                     size="large"
//                                     placeholder="Password"
//                                     prefix={<LockOutlined />}
//                                     value={registerPassword}
//                                     onChange={(e) =>
//                                         setRegisterPassword(e.target.value)
//                                     }
//                                 />
//                             </div>
//                             <Button
//                                 type="primary"
//                                 block
//                                 size="large"
//                                 className="mb-4"
//                                 onClick={handleRegister}
//                             >
//                                 Register
//                             </Button>
//                             <p className="text-sm text-gray-500 text-center mb-2">
//                                 or register with social platforms
//                             </p>
//                             <div className="flex justify-center space-x-4">
//                                 <a
//                                     href="#"
//                                     className="px-3 py-2.5 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-red-500 transition"
//                                 >
//                                     <i className="bx bxl-google"></i>
//                                 </a>
//                                 <a
//                                     href="#"
//                                     className="p-3 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-blue-600 transition"
//                                 >
//                                     <i className="bx bxl-facebook"></i>
//                                 </a>
//                                 <a
//                                     href="#"
//                                     className="p-3 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-black transition"
//                                 >
//                                     <i className="bx bxl-github"></i>
//                                 </a>
//                                 <a
//                                     href="#"
//                                     className="p-3 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-blue-700 transition"
//                                 >
//                                     <i className="bx bxl-linkedin"></i>
//                                 </a>
//                             </div>
//                         </div>
//                     </div>

//                     <div className="w-1/2 h-full relative">
//                         <div
//                             className={`absolute inset-0 flex flex-col items-center justify-center text-white text-center bg-indigo-400 p-6 transition-all duration-700 ${
//                                 isRegistering
//                                     ? "opacity-100"
//                                     : "opacity-0 pointer-events-none"
//                             }`}
//                         >
//                             <h1 className="text-2xl font-bold mb-2">
//                                 Welcome Back!
//                             </h1>
//                             <p className="mb-4">Already have an account?</p>
//                             <Button
//                                 onClick={() => setIsRegistering(false)}
//                                 className="border-white text-white bg-indigo-400 hover:bg-indigo-500"
//                             >
//                                 Login
//                             </Button>
//                         </div>

//                         <div
//                             className={`absolute inset-0 p-10 transition-all duration-700 ${
//                                 isRegistering
//                                     ? "opacity-0 pointer-events-none"
//                                     : "opacity-100 pointer-events-auto"
//                             }`}
//                         >
//                             <h1 className="text-3xl font-bold mb-4">Login</h1>
//                             <div className="mb-4">
//                                 <Input
//                                     size="large"
//                                     placeholder="Username"
//                                     prefix={<UserOutlined />}
//                                     value={loginUsername}
//                                     onChange={(e) =>
//                                         setLoginUsername(e.target.value)
//                                     }
//                                 />
//                             </div>
//                             <div className="mb-4">
//                                 <Input.Password
//                                     size="large"
//                                     placeholder="Password"
//                                     prefix={<LockOutlined />}
//                                     value={loginPassword}
//                                     onChange={(e) =>
//                                         setLoginPassword(e.target.value)
//                                     }
//                                 />
//                             </div>
//                             <div className="mb-2 text-right">
//                                 <a
//                                     href="#"
//                                     className="text-sm text-gray-500 hover:text-indigo-600"
//                                 >
//                                     Forgot Password?
//                                 </a>
//                             </div>
//                             <Button
//                                 type="primary"
//                                 block
//                                 size="large"
//                                 className="mb-4"
//                                 onClick={handleLogin}
//                             >
//                                 Login
//                             </Button>
//                             <p className="text-sm text-gray-500 text-center mb-2">
//                                 or login with social platforms
//                             </p>
//                             <div className="flex justify-center space-x-4">
//                                 <a
//                                     href="#"
//                                     className="px-3 py-2.5 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-red-500 transition"
//                                 >
//                                     <i className="bx bxl-google"></i>
//                                 </a>
//                                 <a
//                                     href="#"
//                                     className="p-3 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-blue-600 transition"
//                                 >
//                                     <i className="bx bxl-facebook"></i>
//                                 </a>
//                                 <a
//                                     href="#"
//                                     className="p-3 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-black transition"
//                                 >
//                                     <i className="bx bxl-github"></i>
//                                 </a>
//                                 <a
//                                     href="#"
//                                     className="p-3 border-2 border-gray-300 rounded-md text-2xl text-gray-800 hover:text-blue-700 transition"
//                                 >
//                                     <i className="bx bxl-linkedin"></i>
//                                 </a>
//                             </div>
//                         </div>
//                     </div>
//                 </div>
//             </div>
//         </div>
//     );
// };

// export default Auth;


import React, { useState } from "react";
import LoginForm from "./components/loginForm";
import PanelLogin from "./components/PaneLogin";
import RegisterForm from "./components/RegisterForm";
import PanelRegister from "./components/PanelRegister";

const Auth = () => {
  const [isRegistering, setIsRegistering] = useState(false);

  // Login states
  const [loginUsername, setLoginUsername] = useState("");
  const [loginPassword, setLoginPassword] = useState("");

  // Register states
  const [registerUsername, setRegisterUsername] = useState("");
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");

  // Handlers
  const handleLogin = () => {
    console.log("Login with:", {
      username: loginUsername,
      password: loginPassword,
    });
    alert(`Login with user: ${loginUsername}, ${loginPassword}`);
  };

  const handleRegister = () => {
    console.log("Register with:", {
      username: registerUsername,
      email: registerEmail,
      password: registerPassword,
    });
    alert(
      `Register with: ${registerUsername}, ${registerEmail}, ${registerPassword}`
    );
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
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-gray-200 to-indigo-200">
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
    </div>
  );
};

export default Auth;