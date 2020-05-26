import axios from 'axios';
import https from "https";

export default axios.create({
    baseURL: 'https://localhost:5000/customer',
    headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Authorization'
    },
    httpsAgent: new https.Agent({
        rejectUnauthorized: false
    }),
});

