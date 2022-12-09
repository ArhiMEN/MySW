import Vue from 'vue'
import VueRouter from 'vue-router'
import LoginView from "@/views/LoginView";
import RegistrationView from "@/views/RegistrationView";
import AccountView from "@/views/AccountView";
import store from "@/store";
import WallView from "@/views/WallView";
import FriendsView from "@/views/FriendsView";
import AddFriendsView from "@/views/AddFriendsView";
import MessageView from "@/views/MessageView";

Vue.use(VueRouter)

function isAuth(to, from, next) {
    if (store.state.user_token != null) {
        next()
        return
    }
    next({name: 'login'})
}

const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginView
  },
  {
        path: '/registration/',
        name: 'registration',
        component: RegistrationView
    },
    {
        path: '/account/',
        name: 'account',
        component: AccountView,
        beforeEnter: isAuth
    },
    {
        path: '/account/wall/',
        name: 'wall',
        component: WallView,
        beforeEnter: isAuth
    },
    {
        path: '/account/friends/',
        name: 'friends',
        component: FriendsView,
        beforeEnter: isAuth
    },
    {
        path: '/account/friends/add',
        name: 'add_friends',
        component: AddFriendsView,
        beforeEnter: isAuth
    },
    {
        path: '/account/friends/messages/:id',
        name: 'messages',
        component: MessageView,
        beforeEnter: isAuth
    },
]

const router = new VueRouter({
  routes
})

export default router
