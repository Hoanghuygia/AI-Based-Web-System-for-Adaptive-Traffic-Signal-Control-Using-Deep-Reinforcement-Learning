import { EnvironmentOutlined } from '@ant-design/icons';

export default function HeaderJunction() {
    return (
        <div className="flex flex-row justify-between items-center w-full p-6">
            <div className="flex flex-col justify-start items-start">
                <h1 className="text-2xl font-semibold text-gray-800 mb-2">
                    Hai Ba Trung - Nguyen Thi Minh Khai
                </h1>
                <p className="text-base text-gray-600">
                    <EnvironmentOutlined className="!text-purple-500 mr-2" />
                    District 3, Ho Chi Minh City • Lat:
                    10.782879, Lng: 106.698107
                </p>
            </div>
            {/* Badge for Traffic Status */}
            <div className="flex items-center px-4 py-2 bg-red-100 rounded-full">
                <span className="text-sm font-medium text-red-400">
                    Heavy Traffic
                </span>
            </div>
        </div>
    );
}
