<template>
  <div>
    <v-card class="content" v-bind:class="{ animate: !isSignIn }">
      <v-card-title v-bind:class="{ hidden: !isSignIn }">
        <img src="/img/logo_colored.png" alt="Brazillian Sea Observatory Brand">
      </v-card-title>
      <v-card-title class="sign-up--content" v-bind:class="{ hidden: isSignIn }">
        <img src="/img/logo_colored.png" alt="Brazillian Sea Observatory Brand">
      </v-card-title>
      <v-card-text v-bind:class="{ hidden: !isSignIn }">
        <v-container fluid>
          <v-layout row>
            <v-flex class="form--panel" xs8>
              <v-layout column align-center align-content-center>
                <h1>{{ $t("account.title") }}</h1>
                <v-form ref="form" v-model="valid" lazy-validation>
                  <v-text-field v-model="user.email" :label="$t('account.email')" type="email" required></v-text-field>
                  <v-text-field
                    v-model="user.password"
                    :append-icon="showPass ? 'visibility_off' : 'visibility'"
                    :type="showPass ? 'text' : 'password'"
                    name="password"
                    :label="$t('account.password')"
                    :hint="$t('account.passHint')"
                    counter
                    @click:append="showPass = !showPass"
                  ></v-text-field>                
                </v-form>

                <v-btn flat small>{{ $t('account.forgot') }}</v-btn>
                <v-btn @click="signIn()" round color="indigo" large>{{ $t('account.signIn') }}</v-btn>
              </v-layout>
            </v-flex>
            <v-flex xs4 class="hide-sm sign-up--panel">
              <h1>{{ $t('account.welcomeUp') }}</h1>
              <p>{{ $t('account.welcomeUp2') }}</p>
              <v-btn round color="white" outline large @click="isSignIn = false">{{ $t('account.signUp') }}</v-btn>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>

      <v-card-text v-bind:class="{ hidden: isSignIn }">
        <v-container fluid>
          <v-layout row>
            <v-flex class="form--panel sign-up--content" xs8>
              <v-layout column align-center align-content-center>
                <h1>{{ $t('account.title2') }}</h1>
                <v-form ref="form" v-model="valid" lazy-validation>
                  <v-text-field v-model="user.name" :label="$t('account.name')" required></v-text-field>
                  <v-text-field v-model="user.email" :label="$t('account.email')" required></v-text-field>
                  <v-text-field
                    v-model="user.password"
                    :append-icon="showPass ? 'visibility_off' : 'visibility'"
                    :type="showPass ? 'text' : 'password'"
                    name="password"
                    :label="$t('account.password')"
                    :hint="$t('account.passHint')"
                    counter
                    @click:append="showPass = !showPass"
                  ></v-text-field>
                  <v-text-field v-model="user.institution" :label="$t('account.institution')" required></v-text-field>
                  <v-text-field v-model="user.city" :label="$t('account.city')" required></v-text-field>
                </v-form>
                <v-btn @click="signUp()" round color="indigo" large>{{ $t('account.signUp') }}</v-btn>
              </v-layout>
            </v-flex>
            <v-flex xs4 class="sign-up--content sign-up--panel">
              <h1>{{ $t('account.welcomeIn') }}</h1>
              <p>{{ $t('account.welcomeIn2') }}</p>
              <v-btn round color="white" outline large @click="isSignIn = true">{{ $t('account.signIn') }}</v-btn>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>
    </v-card>

    <v-snackbar
      v-model="snackbar"
      :color="'error'"
      :timeout="6000"
      :top="true"
    >
      {{ text }}
      <v-btn
        dark
        flat
        @click="snackbar = false"
      >
        {{ $t('account.close') }}
      </v-btn>
    </v-snackbar>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import UserService from '../providers/user.service';

@Component({
    components: {},
})
export default class AuthForm extends Vue {
    public valid = true;
    public showPass = false;
    public isSignIn = true;
    public user = {
        name: '',
        username: '',
        email: '',
        password: '',
        institution: '',
        city: '',
    };
    public text = '';
    public snackbar = false;

    private userService = new UserService();
    public signIn() {
        this.$store.dispatch('auth', this.user)
          .catch((err: any) => {
            this.snackbar = true;
            this.text = this.$t('account.error1').toString();
          });
    }

    public signUp() {
      this.user.username = this.user.email;
      this.$store.dispatch('createUser', this.user)
        .catch((err: any) => {
          this.snackbar = true;
          this.text = this.$t('account.error2').toString();
        });
    }
}
</script>

<style lang="scss" scoped>
img {
    max-width: 6rem;
}
.v-card__title {
    position: absolute;
}
.container.fluid,
.v-card__text {
    padding: 0;
    margin: 0;
}

.form--panel {
    padding: 0 15%;
    min-height: 500px;
    align-items: center;
    display: flex;
    h1 {
        color: #4e76ed;
    }
    form {
        width: 100%;
    }

    .indigo {
        color: white;
    }
}
.sign-up--panel {
    background: #4e76ed;
    color: white;
    margin-left: 1rem;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    p {
        text-align: center;
        margin: 1rem;
    }
}

.sign-up--content {
    transform: rotateY(180deg);
}

.hidden {
    display: none;
}

.content {
    will-change: transform;
    transition: ease-in 0.5s;

    &.animate {
        transform: rotateX(0) rotateY(180deg) rotateZ(0);
    }
}

button.v-btn.v-btn--large.v-btn--round.theme--light.indigo{
  width: 100%;
}

@media (max-width: 768px) {
  .hide-sm {
    display: none;
  }
}
</style>
