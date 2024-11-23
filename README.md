# SW-Repo

Simple file hosting site for serving my provisioning scripts / installers. 

## Usage

- Refer to `backend/files.yaml.sample` to create a `files.yaml`
- Run the container with mounting the `files.yaml` as `app/files.yaml`.
- The default port is `8080`.
- Docker Compose file sample :

```yaml
services:
  app:
    image: registry.gitlab.com/kingkingyyk/sw-repo:master
    volumes:
      - ./files.yaml:/app/files.yaml:ro
    ports:
      - 8080
```
