<template>
  <div class="settings-container">
    <div class="fixed-top-right">
      <v-btn class="hide-sm" color="primary" v-if="!userLogged" round light large @click="dialog = true">
        <v-icon>perm_identity</v-icon> {{ $t('account.signIn') }}
      </v-btn>
      <v-btn class="hide-sm" color="primary" v-if="userLogged" round light large >
        <v-icon>perm_identity</v-icon> {{ user.username }}
      </v-btn>
      <v-btn class="show-sm" color="primary" v-if="!userLogged" fab light @click="dialog = true">
        <v-icon>perm_identity</v-icon>
      </v-btn>
      <v-btn  class="show-sm" color="primary" v-if="userLogged" fab light >
        {{ user.username[0] }}
      </v-btn>

      <v-menu offset-y>
        <v-btn class="hide-sm" slot="activator" color="primary" round light large>
          <v-icon>language</v-icon>
          {{ selectedLanguage }}
        </v-btn>
        <v-btn class="show-sm" slot="activator" color="primary" fab light>
          <v-icon>language</v-icon>
        </v-btn>
        <v-list>
          <v-list-tile
            v-for="(item, index) in languages"
            :key="index"
            @click="onSelectLanguage(item)"
          >
            <v-list-tile-title>{{ item }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
    </div>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" max-width="1024px">
        <AuthForm/>
      </v-dialog>
    </v-layout>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import AuthForm from '@/components/AuthForm.vue';

@Component({
    components: {
        AuthForm,
    },
})
export default class Settings extends Vue {
    public fab = false;
    public dialog = false;
    public selectedLanguage = this.$store.state.lang;
    public languages = ['English', 'Português'];

    public userLogged = false;
    public user: any = null;

    public onSelectLanguage(item: string) {
        this.selectedLanguage = item;
        this.$store.dispatch('setLang', this.selectedLanguage);
    }

    public toggleModal() {
        this.dialog = true;
    }

    public mounted() {
        this.$store.subscribe((mutation, state) => {
            this.dialog = state.isDialogOpen;
            if (mutation.type === 'SET_USER_KEYS') {
              this.user = state.user;
              this.userLogged = state.isLogged;
            }
        });
    }
}
</script>

<style lang="scss" scoped>
div.fixed-top-right {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    position: fixed;
    top: 16px;
    right: 16px;
    width: auto;
    z-index: 9999;
    @media (max-width: 768px) {
      bottom: 0;
      top: 22vh;
      flex-direction: column;
      justify-content: flex-start;
      right: 0.5rem;
      height: 0;
      width: 0;
    }
}

button.v-btn.v-btn--large.theme--light.blue {
    color: white;
}

.v-dialog__container {
    z-index: 99999;
}

.show-sm {
  display: none;
}

@media (max-width: 768px) {
  .hide-sm{
    display: none;
  }  

  .show-sm {
    display: block;
  }
}

</style>
