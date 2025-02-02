import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
      vue(),
      VitePWA({
          includeAssets: ['vite.svg', 'vite.svg', 'vite.svg'],
          manifest: {
              name: 'FineW',
              short_name: 'FineW',
              description: 'Finance control, finance watcher',
              theme_color: '#ffffff',
              icons: [
                  {
                      src: 'vite.svg',
                      sizes: '192x192',
                      type: 'image/svg'
                  },
                  {
                      src: 'vite.svg',
                      sizes: '512x512',
                      type: 'image/svg'
                  }
              ]
          }
      }),
  ]
})
