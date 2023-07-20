from driver import PostgresDriver, PostgresCredentials


class PostgresQueries:
    def __init__(self, host, port, user, password, db):
        self._credentials = PostgresCredentials(host, port, user, password, db)

    async def _execute(self, command, *args):
        driver = await PostgresDriver.get_instance(self._credentials)
        conn = await driver.get_connection()
        try:
            await conn.execute(command, *args)
        finally:
            await driver.release_connection(conn)

    async def _fetch_row(self, command, *args):
        driver = await PostgresDriver.get_instance(self._credentials)
        conn = await driver.get_connection()
        try:
            return await conn.fetchrow(command, *args)
        finally:
            await driver.release_connection(conn)

    async def _fetch(self, command, *args):
        driver = await PostgresDriver.get_instance(self._credentials)
        conn = await driver.get_connection()
        try:
            return await conn.fetch(command, *args)
        finally:
            await driver.release_connection(conn)

    async def _fetch_value(self, command, *args):
        driver = await PostgresDriver.get_instance(self._credentials)
        conn = await driver.get_connection()
        try:
            return await conn.fetchval(command, *args)
        finally:
            await driver.release_connection(conn)
