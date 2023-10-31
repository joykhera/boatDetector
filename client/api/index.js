import express from 'express'
import dotenv from 'dotenv'
import fs from 'fs/promises'
import expressGraphQl from 'express-graphql'
import schema from '../schema/index.js'

dotenv.config({ path: '../.env' });

const app = express()
const port = process.env.EXPRESS_PORT;

app.use(express.static("public"));

app.use(
    '/api/graphql',
    expressGraphQl.graphqlHTTP({
        schema: schema,
        graphiql: true
    })
);

app.listen(port, () => {
    console.log(`Server running at: http://localhost:${port}/`)
})

export default app