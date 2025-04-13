import Test from "@components/Test"
import { useRoutes } from "react-router-dom"
import routes from "./routes"


function App() {
  const element = useRoutes(routes);

  return (
    <>
      {element}
      {/* <Test/> */}
      {/* <h1 className="title">Hello World</h1>
      <h1 className="text-3xl font-bold underline">Hello World</h1> */}
    </>
  )
}

export default App
