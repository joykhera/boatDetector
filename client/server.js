import express, { query } from 'express'
import dotenv from 'dotenv'
import fs from 'fs/promises'

dotenv.config({ path: '../.env' });

const app = express()
const port = process.env.CLIENTPORT;

app.use(express.static("public"));

app.get('/', async (req, res, next) => {
    res.send(await fs.readFile('index.html', 'utf8'))
})

app.listen(port, () => {
    console.log(`Server running at: http://localhost:${port}/`)
})