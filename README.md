# webca-2

A simple web interface for managaing own Certificate Authorities. Python Flask incl. OpenSSL Module in the backend and VueJS as SPA in the Frontend.

  

**Build SPA (Web-Frontend) in Docker**

    $ chmod +x build_in_docker.sh 
    $ ./build_in_docker.sh
  
  <br>
  
**Build Docker Image and run Container (Example)**

    $ docker build -t webca-2:v01 .
    $ docker run -itd -p 8080:80 --name mywebca webca-2:v01

Open your browser and navigate to:
http://YOURDOCKERHOST:8080/#/init