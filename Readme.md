# Multi Hops RAG System 
Multi-hops Retrieval-augmented generation (MRAG) is a system that enhances large language models (LLMs) by retrieving relevant contextual knowledge. Thus addressing LLM hallucinations, and improving response quality by leveraging in-context learning.

#### System Architecutre
![Multi-hops RAG Architecutre](./assets/architecture.png)
That is a system architecture followed by above multi hops RAG System.
You can find the detail explanation of architecture [here.](./assets/MRAG_Architecture_Explanation.pdf)

You can also refer to the lucid chart diagram given below and you can make some comments regarding the improvement of a system.
[Go to Lucid Chart Diagram.](https://lucid.app/lucidspark/dc2502f8-c0da-431f-a7fb-613d32f5bdae/edit?viewport_loc=-812%2C-118%2C3840%2C1862%2C0_0&invitationId=inv_55a3e945-f28f-4432-b264-70a9a6594a53)


### Requirements

```sh
Python v3.8 (*)
Elasticsearch v8.12 (*)
Docker v25.0.3 
docker-compose v2.24.5
```

### Installation Guide
You can run this applicaton either by installing the packages and dependencies manually or using the `Docker`,

- Copy `.env-SAMPLE` to `.env` and configure the environment variables

To run the fast api server,
```sh
    pip install -r requirements.txt
    pipenv run start_api
```
or,
You can also run the api server container by following below steps,
```sh
 docker build -t multi_hop_rag .
 docker run -d --name multi_hop_rag -p 8080:8080
```
Note: At default application runs at port 8080

### Running the whole application

You can directly run the whole application that contains both frontend and backend server using the command below,
Go to the `root` directory,
```sh
    docker-compose up
```
Note: You can access the frontend at port 3000 and api server at port 8080.

### Guideline for Indexing Documents
prerequisites: Before running the script, create folders inside `./documents` and add pdf files that you want to index inside each folder.

Note: Every folders inside the `./documents` creates index in Elasticsearch and every documents inside the corresponding folder are indexed.

To run the indexing script,
```sh
pipenv run index_documents
```

### API Documentation
You can refer to the fast api documentation that uses openapi 3.0 at the following link
[Swagger Documentation for Fast API.](http://localhost:8080/docs).
i.e. http://thisapphost.com/docs

![Swagger Documentation for the above system api](./assets/api_documentation.jpg)
You will get above swagger docs for your reference after visiting the documentation url.


### Client-Side UI (React App)
![Multi hops RAG Chat Application](./assets/chatbot2.jpg)
You can access the client side application made with React JS by accessing `./client` folder and by running the application.
Also, you can find the [Readme.md for React Application](./client/README.md) which guides you through the process to install application locally.

### Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.
