const { Sequelize } = require('sequelize');
require('dotenv').config();

console.log('Testing MySQL connection...');
console.log('Environment variables:');
console.log('DB_HOST:', process.env.DB_HOST);
console.log('DB_PORT:', process.env.DB_PORT || 3306); 
console.log('DB_NAME:', process.env.DB_NAME);
console.log('DB_USER:', process.env.DB_USER);
console.log('DB_PASS:', process.env.DB_PASS ? '*** (password set)' : 'undefined');


const sequelize = new Sequelize(
    process.env.DB_NAME,
    process.env.DB_USER,
    process.env.DB_PASS,
    {
        host: process.env.DB_HOST,
        port: process.env.DB_PORT || 3306,
        dialect: 'mysql',
        logging: console.log, 
        dialectOptions: {
            connectTimeout: 60000
        },
        retry: {
            max: 3,
            timeout: 30000
        }
    }
);

console.log('\nAttempting to connect...');

sequelize.authenticate()
    .then(() => {
        console.log('✅ Connection successful!');
        console.log('Database connection established successfully.');
        process.exit(0);
    })
    .catch(err => {
        console.error('❌ Connection failed:');
        console.error('Error name:', err.name);
        console.error('Error message:', err.message);
        console.error('Error code:', err.original?.code);
        
        if (err.original) {
            console.error('Original error:', err.original);
        }
        
        console.log('\n💡 Troubleshooting tips:');
        console.log('1. Check if MySQL Docker container is running: docker ps');
        console.log('2. Verify container port mapping: docker port <container_name>');
        console.log('3. Check if database exists in MySQL');
        console.log('4. Verify username/password credentials');
        console.log('5. Try connecting from host: mysql -h <host> -P <port> -u <user> -p');
        
        process.exit(1);
    });
