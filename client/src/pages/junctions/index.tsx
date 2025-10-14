import { useAppDispatch } from "@src/stores/hooks";
import {logout} from "@src/stores/user.slice";
import { Button } from "antd";
import { useNavigate } from "react-router-dom";

export default function Junctions() {
    console.log("Render Junctions");
    const dispatch = useAppDispatch();
    const navigate = useNavigate();

    const handleLogout = () => {
        dispatch(logout());
        navigate("/login");
    };

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold mb-4">Junctions</h1>
            <p>Welcome to the Junctions!</p>

            <Button
                type="primary"
                block
                size="large"
                className="p-4 mt-4 !bg-purple-500 !text-white !border-white hover:!bg-white hover:!text-purple-500 hover:!border-purple-500 transition duration-300"
                onClick={handleLogout}
            >
                Logout
            </Button>
        </div>
    );
}