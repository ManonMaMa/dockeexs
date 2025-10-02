FROM alpine
LABEL maintainer="DockerGeek"

# CMD ["echo", "Conversation depuis l'intérieur de la baleine"]

# RUN apk update && apk upgrade && apk add figlet

# ENTRYPOINT [ "figlet" ]

COPY ./index.html /usr/share/nginx/html/

EXPOSE 80