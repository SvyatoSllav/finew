<template>
  <button class="button">{{props.buttonText}}</button>
</template>

<script setup lang="ts">
interface Props {
  buttonText: string;
}

const props = defineProps<Props>()
</script>



<style scoped lang="scss">
.button {
  width: 100%;
  padding: 12px;
  color: #FDFDFD;
  font-size: 16px;
  font-weight: 500;
  line-height: 24px;
  letter-spacing: 0.08px;
  border-radius: 16px;
  background: #105D38;
}
</style>