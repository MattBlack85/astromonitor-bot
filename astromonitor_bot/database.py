import sqlite3


class _Connection:

    def execute(self, query, args=None):
        with sqlite3.connect('astromonitor.db') as conn:
            cursor = conn.cursor()
            if args:
                return cursor.execute(query, args)
            else:
                return cursor.execute(query)

    def _setup_schema(self):
        query = """
        CREATE TABLE IF NOT EXISTS api_tokens
        (api_token text, user_id integer)
        """
        return self.execute(query)

    def start(self):
        self._setup_schema()


connection = _Connection()
