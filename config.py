class DISCORD:
    """"
    Main Discord configuration class.
    """
    TOKEN: str = "MTMzNjc3NjgxNDE2NDQ0MzI0Nw.GVpr9q.fMddovizGB5IV15IeeFflBIU3c7tgj5Ul6uMic"
    PREFIX: str = "?"
    APPLICATION_ID: int = "1336776814164443247"
    CLIENT_ID: str = "1336776814164443247"
    PUBLIC_KEY: str = "f508120236c6f6f3bb2ca7f7de29d04c3e69a22de1bf28e9c7c447220e836dc5"
    OWNER_IDS: list[int] = [
        785042666475225109,
        608450597347262472
    ]

class DATABASE:
    """
    Postgres database configuration class.
    """
    DSN: str = "postgres://postgress:admin@localhost/hiroshima"