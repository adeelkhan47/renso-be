FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx_config.conf /etc/nginx/conf.d/virtual.conf
EXPOSE 80