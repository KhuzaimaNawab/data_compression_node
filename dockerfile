FROM node:17

# Install Oracle Instant Client
RUN apt-get update && apt-get install -y libaio1 libaio-dev
RUN apt-get update && apt-get install -y python
ENV LD_LIBRARY_PATH="/opt/oracle/instantclient"
ENV OCI_HOME="/opt/oracle/instantclient"
ENV OCI_LIB_DIR="/opt/oracle/instantclient"
ENV OCI_INCLUDE_DIR="/opt/oracle/instantclient/sdk/include"

# Install your Node.js app and dependencies
WORKDIR /app
COPY package*.json /app/
RUN npm install
COPY . /app

EXPOSE 3000
CMD ["node", "index.js"]