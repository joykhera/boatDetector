import { GraphQLObjectType } from 'graphql';
import deleteBoat from './mutations/deleteBoat.js';
import deleteBoats from './mutations/deleteBoats.js';

const RootMutation = new GraphQLObjectType({
    name: 'RootMutationType',
    fields: () => ({
        deleteBoat,
        deleteBoats,
    }),
});

export default RootMutation;