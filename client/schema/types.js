import graphql from "graphql";
const { GraphQLObjectType, GraphQLString, GraphQLFloat, Graph } = graphql;

const BoatType = new GraphQLObjectType({
    name: "Boat",
    type: "Query",
    fields: {
        id: { type: GraphQLString },
        link: { type: GraphQLString },
        size: { type: GraphQLFloat },
        speed: { type: GraphQLFloat },
        timestamp: { type: GraphQLString }
    }
});

export default BoatType;