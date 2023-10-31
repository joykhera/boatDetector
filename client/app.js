import express from 'express'
import dotenv from 'dotenv'
import fs from 'fs/promises'
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

// app.get('/', async (req, res, next) => {
//     res.send(await fs.readFile('index.html', 'utf8'))
// })

// app.get('/about', async (req, res, next) => {
//     res.send(await fs.readFile('public/about.html', 'utf8'))
// })

// app.get('/docs', async (req, res, next) => {
//     res.send(await fs.readFile('public/docs.html', 'utf8'))
// })

app.listen(port, () => {
    console.log(`Server running at: http://localhost:${port}/`)
})