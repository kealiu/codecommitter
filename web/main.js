var config = {
};

var simplestore = {
    "alertmsg": "",
    "user": {
        "name": ""
    },
    "perms": {
        "isroot": true,
        "admins": []
    },
    "repos":[],
    "teams":[],
    "projects":[],
    "userarray":[],
    "currentProject": {},
    "currentTeam": {},
    "currentRepo": {},
    "currentRepoReader": [],
    "currentRepoWriter": []
}

const routes = [
    { path: '/', name: "home", redirect: function(to) {return simplestore.user.name ? "/user/profile":"/login"}},
    { path: '/login', name: "login", component: MainLogin},
    { path: '/user/', name: "user", component: MainUser},
    { path: '/user/profile', name: "profile", component: MainProfile},
    { path: '/user/:userid', name: "user", component: MainProfile},
    { path: '/project/', name: "project", component: MainProject},
    { path: '/project/:projectid', name: "project-edit", component: MainProjectEdit},
    { path: '/team/', name: "team", component: MainTeam},
    { path: '/team/:teamid', name: "team-edit", component: MainTeamEdit},
    { path: '/repo/', name: "repo", component: MainRepo},
    { path: '/repo/:repoid', name: "repo", component: MainRepoEdit},
    { path: '/perm/:repoid', name: "repoperm", component: MainPermEdit}
  ]

const router = new VueRouter({
    routes, // short for `routes: routes`
})

var app = new Vue({
    el:  "#app",
    data() {
      return {
          shared: simplestore
        }
    },
    mounted () {
        
    },
    router
  })
