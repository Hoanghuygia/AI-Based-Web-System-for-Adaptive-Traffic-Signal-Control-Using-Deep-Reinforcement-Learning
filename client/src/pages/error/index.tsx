"use client"

import React from "react"
import { Button } from "antd"
import { ArrowLeftOutlined, WarningOutlined } from "@ant-design/icons"
// import { useRouter } from "next/navigation"

// Component 404 sử dụng cả Ant Design và Tailwind CSS
const NotFoundPage: React.FC = () => {
//   const router = useRouter()
  
  const handleGoBack = () => {
    // router.back()
  }
  
  const handleGoHome = () => {
    // router.push("/")
  }
  
  return (
    <div className="flex h-screen items-center justify-center bg-gray-50">
      <div className="w-full max-w-4xl overflow-hidden rounded-2xl shadow-lg">
        <div className="flex flex-col md:flex-row">
          {/* Left panel */}
          <div className="flex flex-1 flex-col items-center justify-center bg-white p-8 py-12">
            <div className="mb-6 text-red-500">
              <WarningOutlined className="text-8xl" />
            </div>
            <h1 className="mb-2 text-6xl font-bold text-gray-900">404</h1>
            <h2 className="mb-4 text-2xl font-semibold text-gray-700">Page Not Found</h2>
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
          
          {/* Right panel */}
          <div className="flex flex-1 flex-col items-center justify-center bg-indigo-400 p-8 py-12 text-white">
            <div className="mb-6 relative">
              <div className="w-32 h-32 rounded-full bg-indigo-300 flex items-center justify-center">
                <div className="text-9xl font-bold text-indigo-100 leading-none">?</div>
              </div>
              <div className="absolute -top-3 -right-3 w-12 h-12 rounded-full bg-indigo-500 flex items-center justify-center text-2xl font-bold">
                404
              </div>
            </div>
            <h2 className="text-2xl font-bold mb-2">Lost Your Way?</h2>
            <p className="mt-2 text-center text-indigo-100">
              Don't worry, it happens to the best of us. Let's get you back on track.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default NotFoundPage