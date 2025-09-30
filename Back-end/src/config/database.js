const { Sequelize } = require('sequelize');
require('dotenv').config();

console.log('Database configuration:');
console.log('Host:', process.env.DB_HOST || 'localhost');
console.log('Port:', process.env.DB_PORT || 3306);
console.log('Database:', process.env.DB_NAME);
console.log('User:', process.env.DB_USER);

const sequelize = new Sequelize(
    process.env.DB_NAME,
    process.env.DB_USER,
    process.env.DB_PASS,
    {
        host: process.env.DB_HOST || 'localhost',
        port: process.env.DB_PORT || 3306,
        dialect: 'mysql',
        logging: process.env.NODE_ENV === 'development' ? console.log : false,
        dialectOptions: {
            connectTimeout: 60000
        },
        retry: {
            max: 3,
            timeout: 30000
        }
    }
);

module.exports = sequelize;
