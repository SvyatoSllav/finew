import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
            '@assets': path.resolve(__dirname, './src/assets'),
            '@components': path.resolve(__dirname, './src/components'),
        },
    },
  plugins: [
      vue(),
      VitePWA({
          includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'mask-icon.svg'],
          manifest: {
              name: 'FineW',
              short_name: 'FineW',
              description: 'Finance control, finance watcher',
              theme_color: '#ffffff',
              icons: [
                  {
                      src: 'web-app-manifest-192x192.png',
                      sizes: '192x192',
                      type: 'image/png'
                  },
                  {
                      src: 'web-app-manifest-512x512.png',
                      sizes: '512x512',
                      type: 'image/png'
                  }
              ]
          }
      }),
  ],
})
