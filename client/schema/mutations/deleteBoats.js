import db from '../../pgAdaptor.js';
import { GraphQLString } from 'graphql';


const deleteBoats = {
    type: GraphQLString,
    resolve() {
        const query = `DELETE FROM boats`;

        return db
            .none(query)  // using 'none' as DELETE doesn't return rows
            .then(() => "All boats deleted.")  // Returning a confirmation message.
            .catch(err => err);
    }
};

export default deleteBoats;
