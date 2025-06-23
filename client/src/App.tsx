import Test from "@components/Test"
import { useRoutes } from "react-router-dom"
import routes from "./routes"


function App() {
  const element = useRoutes(routes);

  return (
    <>
      {element}
      {/* <Test/> */}
    </>
  )
}

export default App
