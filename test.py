import MySQLdb as sql
import sshtunnel
import pandas as pd

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

with sshtunnel.SSHTunnelForwarder(
    ("ssh.pythonanywhere.com"),
    ssh_username="ecotner",
    ssh_password="Fusion1!",
    remote_bind_address=("ecotner.mysql.pythonanywhere-services.com", 3306),
) as tunnel:
    conn = sql.connect(
        user="ecotner",
        password="6M58txoyVxD0D2BUXQeGc",
        host="127.0.0.1",
        port=tunnel.local_bind_port,
        database="ecotner$blog",
    )
    query = """
    SELECT * FROM posts
    """
    df = pd.read_sql(query, conn)
    conn.close()
    print(df)
