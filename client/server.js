import express from 'express'
import dotenv from 'dotenv'
import fs from 'fs/promises'
import pool from './pool.js'

dotenv.config({ path: '../.env' });

const app = express()
const port = process.env.EXPRESS_PORT;

app.use(express.static("public"));

app.get('/', async (req, res, next) => {
    res.send(await fs.readFile('index.html', 'utf8'))
})

app.listen(port, () => {
    console.log(`Server running at: http://localhost:${port}/`)
})

const result = await pool.query('SELECT * FROM boats');
console.log(result.rows);