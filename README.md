http://127.0.0.1:5000/

docker build -t projectcard .

docker run -v C:\Users\Utilisateur\Bureau\code\dockeexs:/python-docker -p 5000:5000 projectcard