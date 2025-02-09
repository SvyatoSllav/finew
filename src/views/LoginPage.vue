<template>
  <div class="login">
    <div class="login__wrapper">
      <h1 class="login__title">Логин</h1>
      <form class="login__form" @submit.prevent="login">
        <InputField v-model="email" label="Почта" placeholder="Введите вашу почту" required type="email"/>
        <InputField v-model="password" label="Пароль" placeholder="Введите ваш пароль" required type="password"/>
        <Button buttonText="Войти" class="login__form__submit-btn" type="submit"/>
      </form>
      <p class="login__sign-up-text">Нет аккаунта?
        <router-link to="/signup"><span class="login__sign-up-text_accent">Зарегистрируйтесь</span></router-link>
      </p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue';
import {useRouter} from 'vue-router';
import {useFirebaseAuth,} from "vuefire";
import InputField from "../Components/InputField.vue";
import Button from "@/Components/Button.vue";
import {signInWithEmailAndPassword} from "@firebase/auth";

const auth = useFirebaseAuth()
const email = ref('');
const password = ref('');
const router = useRouter();

const login = async () => {
  try {
    await signInWithEmailAndPassword(auth, email.value, password.value).then(() => {
      router.push('/');
    })
  } catch (error) {
    console.error('Error logging in:', error);
    alert('Invalid email or password');
  }
};
</script>

<style lang="scss" scoped>
.login {
  max-width: 568px;
  margin: 0 auto;
  height: 100%;
  background-color: #7D8D43;
  display: flex;
  align-items: flex-end;
  border-bottom-right-radius: 36px;
  border-bottom-left-radius: 36px;

  &__wrapper {
    min-height: 538px;
    margin: 0 auto;
    padding: 24px;
    background-color: #F9EEEE;
    width: 100%;
    border-top-left-radius: 36px;
    border-top-right-radius: 36px;
  }

  &__title {
    font-size: 18px;
    font-weight: 600;
    line-height: 26px;
    letter-spacing: 0.09px;
    margin-bottom: 24px;
  }

  &__form {
    display: flex;
    flex-direction: column;
    gap: 12px;

    &__submit-btn {
      margin-top: 32px;
    }
  }

  &__sign-up-text {
    color: #8E8E8E;
    font-size: 16px;
    font-weight: 500;
    line-height: 24px;
    letter-spacing: 0.08px;
    text-align: center;

    &_accent {
      text-decoration: none;
      color: #2B7979;
    }
  }
}
</style>
