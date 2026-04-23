<template>
  <Teleport to="body">
    <Transition name="sheet">
      <div v-if="visible" class="fixed inset-0 z-[100]" @click.self="close">
        <!-- Scrim -->
        <div class="absolute inset-0 bg-on-surface/40 backdrop-blur-sm" @click="close"></div>

        <!-- Sheet -->
        <div
          class="absolute inset-x-0 bottom-0 bg-surface-container-lowest rounded-t-[36px] flex flex-col shadow-[0_-8px_30px_rgba(0,0,0,0.12)] max-h-[90vh] overflow-y-auto"
          @click.stop
        >
          <!-- Drag handle -->
          <div class="w-full pt-4 pb-2 flex justify-center shrink-0 sticky top-0 bg-surface-container-lowest rounded-t-[36px] z-10">
            <div class="w-12 h-1.5 bg-outline-variant/50 rounded-full"></div>
          </div>

          <!-- Content -->
          <div class="px-4 pb-8">
            <slot />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
const visible = defineModel<boolean>('visible', { default: false })

function close() {
  visible.value = false
}
</script>

<style scoped>
.sheet-enter-active {
  transition: all 0.3s ease-out;
}
.sheet-leave-active {
  transition: all 0.2s ease-in;
}
.sheet-enter-from,
.sheet-leave-to {
  opacity: 0;
}
.sheet-enter-from > div:last-child,
.sheet-leave-to > div:last-child {
  transform: translateY(100%);
}
</style>
