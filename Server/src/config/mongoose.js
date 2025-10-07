import mongoose from 'mongoose';
import env from './index.js';

export async function connectMongooseCloud() {
    // const uri = process.env.MONGODB_URI;
    const uri = env.MONGODB_URL;
    console.log('MONGODB_URL:', env.MONGODB_URL);

    try {
        mongoose.connection.on('connected', () => {
            console.log('Mongoose connected to DB');
        });

        mongoose.connection.on('disconnected', () => {
            console.log('Mongoose disconnected from DB');
        });

        mongoose.connection.on('error', (err) => {
            console.error('Mongoose connection error:', err);
        });

        await mongoose.connect(uri, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });

        console.log('Mongoose DB connected');
    } catch (error) {
        console.error('Failed to connect to MongoDB:', error);
    }
}
