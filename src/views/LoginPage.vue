<template>
  <div class="login">
    <div>
      <h1 class="login__title">Логин</h1>
      <h3 class="login__advice">Войдите в свой аккаунт</h3>
      <form class="login__form" @submit.prevent="login">
        <InputField v-model="email" label="Почта" placeholder="Введите вашу почту" required type="email"/>
        <InputField v-model="password" label="Пароль" placeholder="Введите ваш пароль" required type="password"/>
        <Button buttonText="Войти" type="submit"/>
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
  padding: 48px 24px;
  max-width: 568px;
  margin: 0 auto;

  &__title {
    text-align: center;
    font-size: 18px;
    font-weight: 600;
    line-height: 26px;
    letter-spacing: 0.09px;
    margin-bottom: 44px;
  }

  &__advice {
    font-size: 26px;
    font-weight: 600;
    line-height: 32px;
    letter-spacing: 0.13px;
  }

  &__advice-subtitle {
    color: #78828A;
    font-size: 13px;
    font-weight: 400;
    line-height: 22px;
    letter-spacing: 0.065px;
  }

  &__form {
    display: flex;
    flex-direction: column;
    margin-top: 56px;
    gap: 12px;

    &__submit-btn {
      margin-top: 20px;
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
