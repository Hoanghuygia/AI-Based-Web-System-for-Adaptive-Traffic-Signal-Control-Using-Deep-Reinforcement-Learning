import { Input } from "antd";

export default function InputFields() {
    return (
        <div>
            <div className="mb-2">Email Address</div>
            {/* <Input placeholder="Enter your email" type="email" className="mb-4" /> */}
            <Input
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2
                        focus:ring-black focus:border-transparent  transition duration-300"
                placeholder={"Enter your email"}
            />
        </div>
    );
}
