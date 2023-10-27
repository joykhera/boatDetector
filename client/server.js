import express from 'express'
import dotenv from 'dotenv'
import fs from 'fs/promises'
import pg from 'pg'
import graphql from 'graphql'
import expressGraphQl from 'express-graphql'
import schema from './schema/index.js'

dotenv.config({ path: '../.env' });

const app = express()
const port = process.env.EXPRESS_PORT;

app.use(express.static("public"));

app.use(
    '/graphql',
    expressGraphQl.graphqlHTTP({
        schema: schema,
        graphiql: true
    })
);
console.log('schema', schema)

app.get('/', async (req, res, next) => {
    res.send(await fs.readFile('index.html', 'utf8'))
})

app.listen(port, () => {
    console.log(`Server running at: http://localhost:${port}/`)
})

// try {
//     const pool = new pg.Pool({ connectionString: process.env.POSTGRES_URL });
//     const result = await pool.query('SELECT * FROM boats');

//     for (let row of result.rows) {
//         console.log(row.link);

//     }

//     pool.end();

// } catch (err) {
//     console.error(err);
// }
