import pandas as pd
import sshtunnel
import MySQLdb as sql

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

from application.db_config import DBConfig

config = DBConfig()


class FakeTunnel:
    def __enter__(self):
        pass

    def __exit__(self):
        pass


def open_ssh_tunnel():
    tunnel = sshtunnel.SSHTunnelForwarder(
        ssh_address_or_host=config["PYTHONANYWHERE_SSH_TUNNEL_HOST"],
        ssh_username=config["PYTHONANYWHERE_SSH_TUNNEL_USER"],
        ssh_password=config["PYTHONANYWHERE_SSH_TUNNEL_PASSWORD"],
        remote_bind_address=(
            config["PYTHONANYWHERE_MYSQL_HOST"],
            config["PYTHONANYWHERE_MYSQL_PORT"],
        ),
    )
    return tunnel


def open_mysql_connection(database="BLOG", tunnel=None):
    if isinstance(tunnel, FakeTunnel):
        port = (config["PYTHONANYWHERE_MYSQL_PORT"],)
    elif isinstance(tunnel, sshtunnel.SSHTunnelForwarder):
        port = tunnel.local_bind_port
    else:
        raise KeyError("provide valid ssh tunnel")
    conn = sql.connect(
        user=config["PYTHONANYWHERE_MYSQL_USER"],
        password=config["PYTHONANYWHERE_MYSQL_PASSWORD"],
        host="127.0.0.1",
        port=port,
        database=config[f"PYTHONANYWHERE_MYSQL_{database}_DB"],
    )
    return conn


def mysql_to_df(query, database="BLOG"):
    if config["USE_SSH"]:
        tunnel = open_ssh_tunnel()
    else:
        tunnel = FakeTunnel()
    with tunnel:
        conn = open_mysql_connection(database, tunnel)
        df = pd.read_sql(query, conn)
        conn.close()
    return df

