import express from 'express';
// import mongoose from 'mongoose';
import morgan from 'morgan';
import helmet from 'helmet';
import cors from 'cors';
import {route} from './routes/index.js';
import { handleError } from './middlewares/index.js';
import env from './config/index.js';
import { connectMongooseCloud } from './config/mongoose.js';


const app = express();

connectMongooseCloud();

app.use(morgan('dev'));
app.use(helmet());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cors());

// app.use("/", (req, res) => {
//     res.send("Welcome to the server!!!!")
// })

route(app)
handleError(app)

const PORT = env.PORT;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
