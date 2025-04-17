import { useEffect, useState } from "react"
import { Loader2 } from "lucide-react"

const LoadingPage = () => {
  const [progress, setProgress] = useState(0)

  console.log("LoadingPage: Component rendered");

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          return 100
        }
        return prev + 10
      })
    }, 300)

    return () => clearInterval(interval)
  }, [])

  // Optional: handle when loading finishes
  useEffect(() => {
    if (progress === 100) {
      // TODO: Replace with your own logic
      // For example: navigate("/home") or do something else
      console.log("Loading complete!")
    }
  }, [progress])

  return (
    <div className="flex h-screen items-center justify-center bg-gradient-to-r from-gray-200 to-indigo-200">
      <div className="w-full max-w-4xl overflow-hidden rounded-2xl shadow-lg">
          <div className="flex flex-col items-center justify-center bg-white p-8 py-12">
            <div
              className="mb-6 w-16 h-16 text-blue-500"
              role="status"
              aria-label="Loading spinner"
            >
              <Loader2 className="h-16 w-16 animate-spin" />
            </div>
            <h2 className="mb-2 text-2xl font-bold text-gray-900">Loading</h2>
            <div className="w-64 h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-500 transition-all duration-500 ease-in-out"
                style={{
                  width: `${progress}%`,
                  willChange: "width",
                }}
              />
            </div>
            <p className="mt-2 text-sm text-gray-500">Preparing your experience...</p>
          </div>
      </div>
    </div>
  )
}

export default LoadingPage;
