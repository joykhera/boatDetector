import db from '../../pgAdaptor.js';
import { GraphQLList } from 'graphql';
import BoatType from "../types.js";

const getBoats = {
    type: new GraphQLList(BoatType), // Using GraphQLList to indicate an array of BoatType
    async resolve() {  // Add the async keyword here
        console.log("getAllBoats");
        const query = `SELECT * FROM boats`;
        try {
            const response = await db.many(query);  // Use await here
            console.log(response);
            return response;
        } catch (err) {
            console.error(err);
            throw new Error("Error fetching boats.");  // You can customize the error message as required
        }
    }
};


export default getBoats;
