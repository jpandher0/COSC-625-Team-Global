import { createBrowserRouter } from "react-router-dom";
import { Layout } from "./pages/Layout";
import { About } from "./pages/About";
import { Mancala } from "./pages/Mancala";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <Layout/>,
    },
    {
        path: "/mancala",
        element: <Mancala />
    },
    {
        path: "/about",
        element: <About />
    }
]);
