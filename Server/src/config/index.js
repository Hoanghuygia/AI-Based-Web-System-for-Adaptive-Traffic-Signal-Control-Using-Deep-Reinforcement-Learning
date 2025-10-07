import dotenv from 'dotenv';
dotenv.config();

export default {
  PORT: parseInt(process.env.PORT || '8000', 10),
  MONGODB_URI: process.env.MONGODB_URI || 'mongodb://localhost:27017/nodejs-app',
};