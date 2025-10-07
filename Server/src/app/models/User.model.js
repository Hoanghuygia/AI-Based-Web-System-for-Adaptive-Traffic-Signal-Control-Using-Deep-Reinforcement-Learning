import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
    email: { type: String, required: true, unique: true },
    name: { type: String, default: 'Anonymous' },
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now },
    isAdmin: { type: Boolean, default: false }
});

export const User = mongoose.model('User', userSchema);