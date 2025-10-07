import express from 'express';
import mongoose from 'mongoose';
import morgan from 'morgan';
import helmet from 'helmet';
import cors from 'cors';
import {route} from './routes/index.js';
import { handleError } from './middlewares/index.js';
import config from './config/index.js';


const app = express();

mongoose.connect(config.MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
}).then(() => {
    console.log('Connected to MongoDB Cloud');
}).catch((err) => {
    console.error('MongoDB connection error:', err);
});

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

const PORT = config.PORT;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
