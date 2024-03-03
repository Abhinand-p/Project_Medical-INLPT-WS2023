docker login --username=hrida

docker build --no-cache -t light:%1 -t light .

docker image tag light:%1 hrida/light:%1
docker image tag light:latest hrida/light:latest

docker image push hrida/light:%1
docker image push hrida/light:latest

docker rmi -f hrida/light:%1
docker rmi -f hrida/light:latest

