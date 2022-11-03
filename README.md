# flask-website
Learning Flask by building my own website from scratch. I intend to use this for professional/career purposes, but I might also add a blog at some point...

When running the `flask` server, always `source flaskenv.sh` first, then `flask run` from the top directory.

Make sure to configure `application/database/db_config.py` with the proper database credentials before connecting. There is sensitive information in there, so it will not be version controlled.

I'm using some javascript plugin called Chosen for multiselect dropdowns:
```bash
wget https://github.com/harvesthq/chosen/releases/download/v1.8.7/chosen_v1.8.7.zip
```

## mysql-server
The blog utilizes mysql to store posts, tags, comments, etc.
The application uses a mysql docker image with a mounted volume that is spun up on app start.
See [this information](https://dev.mysql.com/doc/refman/8.0/en/docker-mysql-more-topics.html) about how to set up and use mysql with docker.

## Notes
* currently using `python` version `3.6.0`
* currently using `mysql` version `5.7.34`

## TODO
* set up docker and docker-compose
* set up mysql service and database
* set up poetry
* get app running on python3.10