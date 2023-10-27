import { GraphQLID } from 'graphql';
import BoatType from "../types.js";
import db from '../../pgAdaptor.js';

const getBoat = {
    type: BoatType,
    args: { id: { type: GraphQLID } },
    resolve(parentValue, args) {
        const query = `SELECT * FROM boats WHERE id=$1`;
        const values = [args.id];

        return db
            .one(query, values)
            .then(res => res)
            .catch(err => err);
    }
};

export default getBoat;
