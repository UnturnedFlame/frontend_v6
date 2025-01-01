import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    base:'./',
    server: {
      host: '0.0.0.0',
    },
    build: {
      assetsDir: 'static'
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'), // 配置 @ 指向 src 目录
      },
    },
  }
)
