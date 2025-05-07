# DevNon
test everything 

ip host = "159.89.207.194"

uvicorn app.main:app --host 0.0.0.0 --port 8000

scp -r backend/app root@159.89.207.194:/root/Website/backend/app