docker login --username=hrida --email=h.rida1@hotmail.com

docker build -t lamp:%1 -t lamp .

docker image tag lamp:%1 hrida/lamp:%1
docker image tag lamp:latest hrida/lamp:latest

docker image push hrida/lamp:%1
docker image push hrida/lamp:latest

docker rmi -f hrida/lamp:%1
docker rmi -f hrida/lamp:latest

