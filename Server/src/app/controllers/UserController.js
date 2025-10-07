import { registerNewUser, getAllUsers, getUserById, updateUser } from "./DatabaseController.js";

export class UserController {
    getAllUser = async (req, res) => {
        const result = await getAllUsers();
        if (result.success) {
            return res.status(200).json(result);
        } else {
            return res.status(500).json(result);
        }
    };

    signup = async (req, res) => {
        const user = req.body;
        const result = await registerNewUser(user);
        if (result.success) {
            return res.status(201).json(result);
        } else {
            return res.status(400).json(result);
        }
    };

    getUserById = async (req, res) => {
        const { id } = req.params;
        const result = await getUserById(id);
        if (result.success) {
            return res.status(200).json(result);
        } else {
            return res.status(404).json(result);
        }
    };

    updateUser = async (req, res) => {
        const { id } = req.params;
        const data = req.body;
        const result = await updateUser(id, data);
        if (result.success) {
            return res.status(200).json(result);
        } else {
            return res.status(404).json(result);
        }
    };
}
