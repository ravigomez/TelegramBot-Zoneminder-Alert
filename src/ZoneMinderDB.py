import os

import mysql.connector


class ZoneMinderDB:
    def __init__(self):
        super().__init__()

    def latestEvents(self, latestEventID):
        cnx = mysql.connector.connect(user=os.environ.get('MYSQL_USER'), password=os.environ.get('MYSQL_PASSWORD'),
                                      host=os.environ.get('MYSQL_HOST'),
                                      database=os.environ.get('MYSQL_DATABASE'))
        cursor = cnx.cursor()

        query = (
            f'SELECT EventId FROM Events_Week WHERE EventId > {latestEventID}')

        cursor.execute(query)
        events = []
        for (EventId) in cursor:
            events.append(EventId[0])

        cursor.close()
        cnx.close()

        return events
