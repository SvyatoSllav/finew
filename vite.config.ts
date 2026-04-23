import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import {VitePWA} from 'vite-plugin-pwa'
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        tailwindcss(),
        vue({
            template: {
                transformAssetUrls: {
                    // Add your custom components here
                    icon: ['data'], // Allow the `data` attribute on `<icon>` to be treated as an asset URL
                    img: ['src'],  // Allow the `src` attribute on `<img>` to be treated as an asset URL
                },
            },
        }),
        VitePWA({
            includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'mask-icon.vue-icons'],
            manifest: {
                name: 'FineW',
                short_name: 'FineW',
                description: 'Finance control, finance watcher',
                theme_color: '#53621d',
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
    resolve: {
        alias: {
            '@': path.resolve(__dirname, 'src'),
            '@assets': path.resolve(__dirname, 'src/assets'),
            '@components': path.resolve(__dirname, 'src/components'),
            '@vue-icons': path.resolve(__dirname, 'src/assets/vue-icons'),
        },
    },
    assetsInclude: ['**/*.woff', '**/*.woff2', '**/*.ttf',],
})
