<template>
  <div class="input-wrapper">
    <label v-if="props.label" class="input-wrapper__label">{{ props.label }}</label>
    <input v-model="model" :placeholder="props.placeholder" :type="props.type" class="input-wrapper__input-field"/>
  </div>
</template>

<script lang="ts" setup>
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


<style lang="scss" scoped>
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
    background-color: #fff;
    border: none;
    outline: none;

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