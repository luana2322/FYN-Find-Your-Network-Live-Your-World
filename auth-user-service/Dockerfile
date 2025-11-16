version: "3.9"

services:

  minio:
    image: minio/minio:RELEASE.2025-10-01T04-33-00Z
    container_name: minio
    restart: always
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - ./minio_data:/data   # <-- bind-mount local folder
