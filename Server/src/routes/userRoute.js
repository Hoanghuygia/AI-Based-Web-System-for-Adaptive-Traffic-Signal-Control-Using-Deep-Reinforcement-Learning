import { Router } from "express";
import { UserController } from "../app/controllers/UserController.js";

const route = Router();
const userController = new UserController();

route.get("/", userController.getAllUser);
route.post("/", userController.signup);
route.get("/:id", userController.getUserById);
route.put("/:id", userController.updateUser);

export {route as userRoute}