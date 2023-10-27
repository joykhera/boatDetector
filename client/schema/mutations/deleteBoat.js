import db from '../../pgAdaptor.js';
import { GraphQLID } from 'graphql';

const deleteBoat = {
    type: GraphQLID,
    args: {
        id: { type: GraphQLID }
    },
    resolve(parentValue, args) {
        const query = `DELETE FROM boats WHERE id=$1`;
        const values = [args.id];

        return db
            .none(query, values)  // using 'none' as DELETE doesn't return rows
            .then(() => args.id)  // Returning the ID of the deleted item for simplicity.
            .catch(err => err);
    }
};

export default deleteBoat;
