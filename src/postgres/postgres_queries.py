from driver import PostgresDriver


class PostgresQueries:
    async def _execute(self, command, *args):
        driver = await PostgresDriver.get_instance()
        conn = await driver.get_connection()
        try:
            await conn.execute(command, *args)
        finally:
            await driver.release_connection(conn)

    async def _fetch_row(self, command, *args):
        driver = await PostgresDriver.get_instance()
        conn = await driver.get_connection()
        try:
            return await conn.fetchrow(command, *args)
        finally:
            await driver.release_connection(conn)

    async def _fetch(self, command, *args):
        driver = await PostgresDriver.get_instance()
        conn = await driver.get_connection()
        try:
            return await conn.fetch(command, *args)
        finally:
            await driver.release_connection(conn)

    async def _fetch_value(self, command, *args):
        driver = await PostgresDriver.get_instance()
        conn = await driver.get_connection()
        try:
            return await conn.fetchval(command, *args)
        finally:
            await driver.release_connection(conn)
