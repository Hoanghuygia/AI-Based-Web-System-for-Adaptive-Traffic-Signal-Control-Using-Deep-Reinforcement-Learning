import React from "react"
import { Button } from "antd"
import { ArrowLeftOutlined} from "@ant-design/icons"
import { useNavigate } from 'react-router-dom';

const NotFoundPage: React.FC = () => {
    const navigate = useNavigate();
  
    const handleGoBack = () => {
        navigate(-1);
    }
    
    const handleGoHome = () => {

    }
  
    return (
        <div className="w-full max-w-4xl overflow-hidden rounded-2xl shadow-lg">
            <div className="flex flex-col items-center justify-center bg-white p-8 py-12">
                <div className="mb-6 relative">
                    <div className="w-32 h-32 rounded-full bg-indigo-300 flex items-center justify-center">
                        <div className="text-9xl font-bold text-indigo-100 leading-none">?</div>
                    </div>
                    <div className="absolute -top-3 -right-3 w-12 h-12 rounded-full bg-indigo-500 flex items-center justify-center text-2xl font-bold">
                        404
                    </div>
                </div>
                
                <h1 className="mb-2 text-6xl font-bold text-gray-900">404</h1>
                <h2 className="mb-4 text-2xl font-semibold text-gray-700">Lost Your Way?</h2>
                <p className="mb-8 text-center text-gray-500">
                Oops! The page you are looking for might have been removed or is temporarily unavailable.
                </p>
                <div className="flex flex-col sm:flex-row gap-4">
                <Button
                    type="primary"
                    size="large"
                    icon={<ArrowLeftOutlined />}
                    onClick={handleGoBack}
                    className="!bg-blue-500 hover:!bg-blue-600"
                >
                    Go Back
                </Button>
                <Button 
                    size="large" 
                    onClick={handleGoHome}
                    className="border-gray-300 hover:border-gray-400"
                >
                    Go Home
                </Button>
                </div>
            </div>
        </div>
    )
}

export default NotFoundPage