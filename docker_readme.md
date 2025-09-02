### AI Application Packaging Basics: Using FastAPI and Docker

url: https://medium.com/@kbdhunga/ai-application-packaging-basics-using-fastapi-and-docker-c21575703264

![alt text](image.png)


## Testing the FASTAPI 

method: POST
Body: json 

{
    "text": "who won the election?"
}


## Containerizing a FastAPI Application:

Containers ensure that the application runs consistently across different computing environments, whether it’s on a developer’s local machine, a testing environment, or a production server.

step 1: create a Dockerfile

    Dockerfile image

    FROM python:3.12  # base image
    COPY . .    # copies all project files into the container
    RUN pip install -r requirements.txt # run python commands
    ENTRYPOINT [ "python" ]   # set entry point to execute python commands
    EXPOSE 80           # communication port for Docker container
    CMD ["main.py"]     # configures main.py as default scripts to run


## Docker Commands from Power Shell Terminal

docker build -t fastapi-health-faiss .
docker run -d -p 8080:80 fastapi-health-faiss
docker rm --force <docker_id>