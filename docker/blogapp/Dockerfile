FROM python:3.9
ENV WORKSPACE=/var/www/blogapp/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p $WORKSPACE
WORKDIR $WORKSPACE
COPY . $WORKSPACE

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN ["chmod", "+x", "/var/www/blogapp/docker/blogapp/entrypoint.sh"]
CMD ["/var/www/blogapp/docker/blogapp/entrypoint.sh"]

EXPOSE 8000
