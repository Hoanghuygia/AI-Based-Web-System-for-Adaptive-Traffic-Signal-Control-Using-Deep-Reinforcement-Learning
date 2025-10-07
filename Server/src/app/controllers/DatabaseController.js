import { User } from "../models/User.model.js";

export const registerNewUser = async (user) => {
    try {
        const newUser = new User(user);
        await newUser.save();
        return { success: true, message: "User created successfully", user: newUser };
    } catch (error) {
        return { success: false, message: error.message };
    }
};
export const getAllUsers = async () => {
    try {
        const users = await User.find();
        return { success: true, users };
    } catch (error) {
        return { success: false, message: error.message };
    }
};

export const getUserById = async (id) => {
    try {
        const user = await User.findById(id);
        if (!user) return { success: false, message: "User not found" };
        return { success: true, user };
    } catch (error) {
        return { success: false, message: error.message };
    }
};

export const updateUser = async (id, data) => {
    try {
        const user = await User.findByIdAndUpdate(id, data, { new: true });
        if (!user) return { success: false, message: "User not found" };
        return { success: true, user };
    } catch (error) {
        return { success: false, message: error.message };
    }
};
// ...existing code...
// ...existing code...
