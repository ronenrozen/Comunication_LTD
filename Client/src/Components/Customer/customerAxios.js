import axios from 'axios';

export default axios.create({
    baseURL: 'http://localhost:5000/customer',
    headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Authorization'
    }
});

