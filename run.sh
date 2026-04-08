#!/bin/bash
#
# 啟動主程式：建立 Docker container 並執行應用程式

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly IMAGE_NAME="nk7260ynpa/tw-stock-webpage"
readonly CONTAINER_NAME="tw-stock-webpage"
readonly NETWORK_NAME="db_network"

# 確保 logs 資料夾存在
mkdir -p "${SCRIPT_DIR}/logs"

# 確保 Docker network 存在
if ! docker network ls --format '{{.Name}}' | grep -q "^${NETWORK_NAME}$"; then
  echo "建立 Docker network: ${NETWORK_NAME}"
  docker network create "${NETWORK_NAME}"
fi

# 建立 Docker image（如果尚未建立）
bash "${SCRIPT_DIR}/docker/build.sh"

# 停止並移除舊的 container（如果存在）
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "停止並移除舊的 container: ${CONTAINER_NAME}"
  docker stop "${CONTAINER_NAME}" 2>/dev/null || true
  docker rm "${CONTAINER_NAME}" 2>/dev/null || true
fi

# 啟動 Docker container，掛載 logs 資料夾
echo "啟動 container: ${CONTAINER_NAME}"
docker run -d \
  --name "${CONTAINER_NAME}" \
  --network "${NETWORK_NAME}" \
  --restart always \
  -p 7938:8000 \
  -v "${SCRIPT_DIR}/logs:/app/logs" \
  -e TZ=Asia/Taipei \
  "${IMAGE_NAME}:latest"

echo "應用程式已啟動，請開啟瀏覽器前往 http://localhost:7938"
