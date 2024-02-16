# Topicaxis API

This repository contains the source code for the Topicaxis API.

## Configuration

Create a file and name it `.env`. Set the required configuration variables.
See `config/env.template` for an example configuration file.

| Name             | Description                                        |
|------------------|----------------------------------------------------|
| openapi_url      | The endpoint where the OpenAPI schema is served    |
| docs_url         | The endpoint where the documentation is served     |
| sqlalchemy_url   | The connection string for the PostgresSQL database |

## Build the docker image

```bash
docker build -t topicaxis/api .
```

## Installation

The Topicaxis API requires a PostgreSQL database. Before you start the API server you
have to run the database migrations using Docker.

```bash
docker container run \
--mount type=bind,source=/opt/topicaxis/api/config/.env,target=/app/.env \
--rm -it topicaxis/api migrate
```

## Start the API server using docker

```bash
docker container run -d \
--mount type=bind,source=/opt/topicaxis/api/config/.env,target=/app/.env \
-p 8000:8000 \
-it topicaxis/api run
```

## CLI

Use the cli commands to create users and load articles. See the available commands using docker.

```bash
docker container run \
--mount type=bind,source=/opt/topicaxis/api/config/.env,target=/app/.env \
--rm -it topicaxis/api topicaxisapi-cli --help
```

### Create user

```bash
docker container run \
--mount type=bind,source=/opt/topicaxis/api/config/.env,target=/app/.env \
--rm -it topicaxis/api topicaxisapi-cli users create user1
```

This command will output the users API key.

### Load the articles from a file

```bash
docker container run \
--mount type=bind,source=/opt/topicaxis/api/config/.env,target=/app/.env \
--rm -it topicaxis/api topicaxisapi-cli articles load articles.json
```

The articles file must contain one JSON record per line with the article data. This is an example article.

```json
{
  "id": "O5LG8oXx96W5XdbD4B7gNReP",
  "url": "https://example.com/page-1",
  "title": "Article title",
  "created_at": 1708013120,
  "source": {
    "id": "O5LG8oXx96Wm4bD4B7gNRePz",
    "name": "example",
    "url": "https://example.com"
  },
  "categories": [
    {
      "id": "VN2lZeLKMz0jGQX9JdPOnoyx",
      "name": "business",
      "taxonomy": {
        "id": "MkJA2n0wgeDwKDb5rVXNBO4E",
        "name": "topicaxis"
      }
    }
  ],
  "tags": [
    {
      "id": "YL4jroWBqw03yXdMKa9P57v3",
      "name": "Economy"
    }
  ],
  "channels": [
    {
      "id": "y0KYlk3p14G6vGDWmjrQeRgN",
      "name": "Hacker News",
      "url": "https://news.ycombinator.com",
      "posts": [
        {
          "title": "Article example",
          "url": "https://news.ycombinator.com/item?id=123456789123",
          "posted_at": 1708011634
        }
      ]
    }
  ],
  "description": "article description",
  "image": "https://example.com/image.png",
  "summary": "article summary",
  "keywords": ["keyword-1", "keyword-2"],
  "named_entities": [
    {
      "id": "njQd4g8r1DnNMKDZB5OGM9bx",
      "value": "named entity 1",
      "type": {
        "id": "3rNwgkWodM6wyDyj1A5Lamn9",
        "name": "GEOPOLITICAL_ENTITY"
      }
    }
  ]
}
```

## Known issues
* The proprietary Topicaxis API service used MongoDB in the database layer. The open source service is using PostgreSQL. 
  The database models aren't in their final state yet.
