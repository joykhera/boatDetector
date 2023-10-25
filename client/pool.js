import pg from 'pg'
import dotenv from 'dotenv'

dotenv.config({ path: '../.env' });

const pool = new pg.Pool({
    connectionString: process.env.POSTGRES_URL,
    ssl: {
        rejectUnauthorized: false
    }

});
console.log(pool)

export default pool