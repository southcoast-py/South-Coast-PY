from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()


    def create_friendship(self, person1_name, person2_name):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_friendship, person1_name, person2_name)
            for row in result:
                print("Created friendship between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))

    def create_roles(self, role):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction( self.__set_roles, role)
            for row in result:
                print("Created role: {p1} with ref: {p2}".format(p1=row['title'], p2=row['ref']))

    def create_areas(self, area):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction( self.__set_areas, area)
            for row in result:
                print("Created area: {p1} ".format(p1=row['name']))






    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:KNOWS]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_person(self, person_name):
        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]

        
    @staticmethod
    def __set_roles(tx, role):
        query = (
        "CREATE (r1:ROLE {}) "
        "set r1 += $person_name "
        "RETURN r1 as name"
        )
        result = tx.run(query, person_name=role)
        return [row['name'] for row in result]
    
    
    @staticmethod
    def __set_areas(tx, area):
        query = (
        "CREATE (r1:AREA { name: $person_name }) "
        "RETURN r1 as name"
        )
        result = tx.run(query, person_name=area)
        return [row["name"] for row in result]


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+ssc://6f06432b.databases.neo4j.io:7687"
    user = "neo4j"
    password = "UJKnMpvVOVLRox1o3NxhUT_kLPubvVZIf1VjGmdQoc4"
    app = App(uri, user, password)
    # app.create_friendship("Alice", "David")
    # app.find_person("Alice")

    roles=[ {'title': 'admin', 'ref':1}, 
            {'title': 'modirator', 'ref':2}, 
            {'title': 'creator', 'ref':3}, 
            {'title': 'subscriber', 'ref':4}, 
            {'title': 'reader', 'ref':5}]
    for role in roles:
        app.create_roles(role)
    areas=['Healing', 'Meditation', 'Philosophy', 'Personal Development']
    for area in areas:
        app.create_areas(area)
    app.close()