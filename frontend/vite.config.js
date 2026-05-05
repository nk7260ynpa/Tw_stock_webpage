import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// 透過 Dashboard 反向代理時，瀏覽器路徑為 /app/webpage/...
// Vite base 設定讓所有靜態資源路徑（JS/CSS）自動加上前綴
// 可透過 VITE_BASE 環境變數覆蓋，方便直接存取（= '/'）或本地開發
export default defineConfig({
  base: process.env.VITE_BASE || '/app/webpage/',
  plugins: [react()],
  build: {
    outDir: '../static',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
