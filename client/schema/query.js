import { GraphQLObjectType } from 'graphql';
import getBoat from './queries/getBoat.js';
import getBoats from './queries/getBoats.js';

const RootQuery = new GraphQLObjectType({
    name: 'RootQueryType',
    fields: () => ({
        getBoat,
        getBoats,
    }),
});

export default RootQuery;