const { Sequelize } = require('sequelize');
require('dotenv').config();

console.log('Creating database if it doesn\'t exist...');


const sequelize = new Sequelize('', process.env.DB_USER, process.env.DB_PASS, {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 3306,
    dialect: 'mysql',
    logging: console.log
});

async function createDatabase() {
    try {

        const [results] = await sequelize.query(`SHOW DATABASES LIKE '${process.env.DB_NAME}'`);
        
        if (results.length > 0) {
            console.log(`✅ Database '${process.env.DB_NAME}' already exists`);
        } else {
            // Create the database
            await sequelize.query(`CREATE DATABASE ${process.env.DB_NAME}`);
            console.log(`✅ Database '${process.env.DB_NAME}' created successfully`);
        }
        

        const dbSequelize = new Sequelize(
            process.env.DB_NAME,
            process.env.DB_USER,
            process.env.DB_PASS,
            {
                host: process.env.DB_HOST || 'localhost',
                port: process.env.DB_PORT || 3306,
                dialect: 'mysql'
            }
        );
        
        await dbSequelize.authenticate();
        console.log('✅ Connection to database successful!');
        
        await sequelize.close();
        await dbSequelize.close();
        
    } catch (error) {
        console.error('❌ Error:', error.message);
        console.log('\n💡 Make sure:');
        console.log('1. MySQL user has permission to create databases');
        console.log('2. MySQL server is running');
        console.log('3. Connection details are correct');
    }
}

createDatabase();
