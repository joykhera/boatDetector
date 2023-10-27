import { GraphQLSchema } from 'graphql';
import mutation from './mutation.js';
import query from './query.js';

const schema = new GraphQLSchema({
    mutation,
    query,
});

export default schema