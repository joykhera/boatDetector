import dotenv from 'dotenv'
import pgPromise from 'pg-promise'
import pg from 'pg'

dotenv.config({ path: '../.env' });

const pgp = pgPromise({}); // Empty object means no additional config required

const config = {
    host: process.env.POSTGRES_HOST,
    port: process.env.POSTGRES_PORT,
    database: process.env.POSTGRES_DB,
    user: process.env.POSTGRES_USER,
    password: process.env.POSTGRES_PASSWORD,
    ssl: {
        rejectUnauthorized: false
    }
};

const db = pgp(config);

export default db;

// const db = new pg.Pool({ connectionString: process.env.POSTGRES_URL });
// export default db;