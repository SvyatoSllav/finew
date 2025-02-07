<template>
  <div class="input-wrapper">
    <label class="input-wrapper__label" v-if="props.label">{{ props.label }}</label>
    <input class="input-wrapper__input-field" v-model="model" :type="props.type" :placeholder="props.placeholder"/>
  </div>
</template>

<script setup lang="ts">
const model = defineModel()

interface Props {
  label?: string;
  type?: string;
  placeholder?: string;
}
const props = withDefaults(defineProps<Props>(), {
  label: '',
  placeholder: '',
  type: 'text',
});
</script>


<style scoped lang="scss">
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;

  &__label {
    font-size: 14px;
    font-weight: 600;
    line-height: 22px;
    letter-spacing: 0.07px;
  }

  &__input-field {
    padding: 16px;
    border-radius: 20px;
    border: 1px solid #ECF1F6;

    &::placeholder {
      color: #78828A;
      font-size: 12px;
      font-style: normal;
      font-weight: 400;
      line-height: 20px;
      letter-spacing: 0.06px;
    }
  }
}
</style>