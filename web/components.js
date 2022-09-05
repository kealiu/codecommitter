//  ------------------- Header -------------------
const AppHeader = {
    template: `<b-container class="bv-example-row">
            <b-row>
                <b-col> </b-col>
                <b-col cols="8"> <b-alert v-if="shared.alertmsg" show dismissible id="header-alert"> {{shared.alertmsg}} </b-alert> </b-col>
                <b-col> 
                    <div v-if="shared.user.name"> <router-link to="/user/profile"> {{shared.user.name}} </router-link> </div>
                    <div v-else> <router-link to="/login">login</router-link> </div> 
                </b-col>
            </b-row>
        </b-container>`,
    data: function(){
        return {
            shared: simplestore
        }
    }
};
Vue.component('app-header', AppHeader);

//  ------------------- Nav -------------------
const AppNav = {
    template: "<slot></slot>",
    data: function(){
        return {
            shared: simplestore
        }
    }
};
Vue.component('app-nav', AppNav);

//  ------------------- Footer -------------------
const AppFooter = {
    template: "<slot></slot>",
    data: function(){
        return {
            shared: simplestore
        }
    }
}; 
Vue.component('app-footer', AppFooter);

//  ------------------- Project -------------------
const MainProject = {
    template: `<b-table-simple hover small caption-top responsive>
                <b-thead head-variant="dark">
                    <b-tr>
                        <b-th colspan="2">Id</b-th>
                        <b-th colspan="3">Name</b-th>
                        <b-th colspan="7">Desc</b-th>
                    </b-tr>
                </b-thead>
                <b-tbody>
                    <b-tr v-for="project in shared.projects" :key="project.id">
                        <b-th>  <router-link :to=project.link> {{project.id}} </router-link> </b-th>
                        <b-th> {{project.name}} </b-th>
                        <b-th> {{project.desc}} </b-th>
                    </b-tr>
                </b-tbody>
            </b-table-simple>`,
    data: function(){
        return {
            fields: ['id', 'name', 'desc'],
            shared: simplestore
        }
    },
    computed: {
    },
    mounted () {
        axios.get('/project/').then(function(resp){
            //this.projects = Object.assign({}, this.projects, resp.data)
            simplestore.projects = resp.data
            simplestore.projects.forEach(function(val, idx){
                val['link'] = '/project/'+ val.id
            })
        }).catch(function(err){
            console.log(err)
            simplestore.alertmsg = err.message
        })
    },
    methods: {
        getProjects: function(){
            const p = axios.get('/project/');
            return p.then(function(resp){
                Vue.set(this.projects, resp.data)
                //return resp.data.map(p => {return {"id": "<router-link to=\"/project/"+p.id+"\">"+p.id+"</router-link>", "name": p.name, "desc": p.desc}}) || []
                return resp.data || []
            });
        }
    }
};
Vue.component('main-project', MainProject);

//  ------------------- Project Edit -------------------
const MainProjectEdit = {
    template: `<b-container fluid>
                <b-row>
                    <b-col sm="3">
                        <label>project name</label>
                    </b-col>
                    <b-col sm="9">
                        <b-form-input v-model="shared.currentProject.name"> </b-form-input>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col sm="3">
                        <label>project description</label>
                    </b-col>
                    <b-col sm="9">
                        <b-form-input v-model="shared.currentProject.desc"></b-form-input>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col sm="3">
                        <label>project admin</label>
                    </b-col>
                    <b-col sm="9">
                        <b-form-input v-model="admin"></b-form-input>
                    </b-col>
                </b-row>
                <b-row> <b-button v-on:click="submitproject">Submit</b-button> </b-row>
            </b-container>`,
    data: function(){
        return {
            admin: "",
            projectid: this.$route.params.projectid,
            shared: simplestore
        }
    },
    mounted () {
        if (this.$route.params.projectid && this.$route.params.projectid != 0) {
            self = this
            axios.get('/project/'+this.$route.params.projectid).then(function(resp){
                //this.project = resp.data
                simplestore.currentProject = resp.data
                if (simplestore.currentProject.admins && simplestore.currentProject.admins[0]) {
                    adminid = simplestore.currentProject.admins[0].id
                    axios.get('/user/'+adminid).then(function(resp){
                        self.admin = resp.data.name
                    })
                }
                //this.project = Object.assign({}, this.project, resp.data)
            }).catch(function(err){
                console.log(err)
                simplestore.alertmsg = err.message
            })
        } else {
            simplestore.currentProject = {
                "name" : "",
                "desc" : ""
            }
        }
    },
    methods: {
        submitproject: function(){
            submitprom = null;
            self = this
            admin = this.admin
            usercheck = axios.get('/user/name/'+admin)
            usercheck.then(function(resp){
                adminid = resp.data.id
                if (self.projectid != 0) {
                    submitprom = axios.put('/project/'+self.projectid, simplestore.currentProject);
                } else {
                    submitprom = axios.post('/project/', simplestore.currentProject)
                }
                submitprom.then(function(resp){
                    simplestore.currentProject = resp.data
                    tmpdata = {"userid": adminid, "projectid": simplestore.currentProject.id}
                    theprom = null
                    if (simplestore.currentProject.admins && simplestore.currentProject.admins.length != 0) {
                        adminid = simplestore.currentProject.admins[0].id
                        theprom = axios.put('/project/'+simplestore.currentProject.id+'/admin/'+adminid, tmpdata)
                    } else {
                        theprom = axios.post('/project/'+simplestore.currentProject.id+'/admin/', tmpdata)
                    }
                    theprom.then(function(resp){
                        router.push('/project/')    
                    }).catch(function(err){
                        simplestore.alertmsg = err.message
                    })
                }).catch(function(err){
                    console.log(err)
                    simplestore.alertmsg = err.message
                });
            }).catch(function(err){
                console.log(err)
                simplestore.alertmsg = err.message
            })
        }
    }
};
Vue.component('main-project-edit', MainProjectEdit);

//  ------------------- Team -------------------
const MainTeam = {
    template: `<b-table-simple hover small caption-top responsive>
                <b-thead head-variant="dark">
                    <b-tr>
                        <b-th colspan="2">Id</b-th>
                        <b-th colspan="3">Name</b-th>
                        <b-th colspan="7">Desc</b-th>
                    </b-tr>
                </b-thead>
                <b-tbody>
                    <b-tr v-for="team in shared.teams" :key="team.id">
                        <b-th>  <router-link :to=team.link> {{team.id}} </router-link> </b-th>
                        <b-th> {{team.name}} </b-th>
                        <b-th> {{team.desc}} </b-th>
                    </b-tr>
                </b-tbody>
            </b-table-simple>`,
    data: function(){
        return {
            shared: simplestore
        }
    },
    computed: {
    },
    mounted () {
        axios.get('/team/').then(function(resp){
            simplestore.teams = resp.data
            simplestore.teams.forEach(function(val, idx){
                val['link'] = '/team/'+ val.id
            })
        }).catch(function(err){
            console.log(err)
            simplestore.alertmsg = err.message
        })
    },
    methods: {
        getTeams: function(){
            const p = axios.get('/team/');
            return p.then(function(resp){
                Vue.set(this.teams, resp.data)
                //return resp.data.map(p => {return {"id": "<router-link to=\"/project/"+p.id+"\">"+p.id+"</router-link>", "name": p.name, "desc": p.desc}}) || []
                return resp.data || []
            });
        }
    }
};
Vue.component('main-team', MainTeam);

//  ------------------- Team Edit -------------------
const MainTeamEdit = {
    template: `<b-container fluid>
                <b-row>
                    <b-col sm="3">
                        <label>team name</label>
                    </b-col>
                    <b-col sm="9">
                        <b-form-input v-model="shared.currentTeam.name"> </b-form-input>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col sm="3">
                        <label>team description</label>
                    </b-col>
                    <b-col sm="9">
                        <b-form-input v-model="shared.currentTeam.desc"></b-form-input>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col sm="3">
                        <label>team project name</label>
                    </b-col>
                    <b-col sm="9">
                        <b-form-input v-model="project"></b-form-input>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col sm="3">
                        <label>team admin</label>
                    </b-col>
                    <b-col sm="9">
                        <b-form-input v-model="admin"></b-form-input>
                    </b-col>
                </b-row>
                <b-row> <b-button v-on:click="submitteam">Submit</b-button> </b-row>
            </b-container>`,
    data: function(){
        return {
            project: "",
            admin: "",
            teamid: this.$route.params.teamid,
            shared: simplestore
        }
    },
    mounted () {
        if (this.$route.params.teamid && this.$route.params.teamid != 0) {
            self = this
            axios.get('/team/'+this.$route.params.teamid).then(function(resp){
                //this.project = resp.data
                simplestore.currentTeam = resp.data
                if (simplestore.currentTeam.admins && simplestore.currentTeam.admins[0]) {
                    adminid = simplestore.currentTeam.admins[0].id
                    prjprom=axios.get('/project/'+simplestore.currentTeam.projectid)
                    userprom=axios.get('/user/'+adminid)
                    Promise.all([prjprom, userprom]).then(function(resps){
                        self.admin = resps[0].data.name
                        self.project = resps[1].data.name
                    })
                }
                //this.project = Object.assign({}, this.project, resp.data)
            }).catch(function(err){
                console.log(err)
                simplestore.alertmsg = err.message
            })
        } else {
            simplestore.currentTeam = {
                "name" : "",
                "desc" : ""
            }
        }
    },
    methods: {
        submitteam: function(){
            submitprom = null;
            self = this
            admin = this.admin
            project = this.project
            usercheck = axios.get('/user/name/'+ admin)
            projectcheck = axios.get('/project/name/'+project)
            Promise.all([usercheck, projectcheck]).then(function(resps){
                adminid = resps[0].data.id
                projectid = resps[1].data.id
                simplestore.currentTeam.projectid = projectid
                if (self.teamid != 0) {
                    submitprom = axios.put('/team/'+self.teamid, simplestore.currentTeam);
                } else {
                    submitprom = axios.post('/team/', simplestore.currentTeam)
                }
                submitprom.then(function(resp){
                    simplestore.currentTeam = resp.data
                    tmpdata = {"userid": adminid, "teamid": simplestore.currentTeam.id}
                    theprom = null
                    if (simplestore.currentTeam.admins && simplestore.currentTeam.admins.length != 0) {
                        adminid = simplestore.currentTeam.admins[0].id
                        theprom = axios.put('/team/'+simplestore.currentTeam.id+'/admin/'+adminid, tmpdata)
                    } else {
                        theprom = axios.post('/team/'+simplestore.currentTeam.id+'/admin/', tmpdata)
                    }
                    theprom.then(function(resp){
                        router.push('/team/')    
                    }).catch(function(err){
                        simplestore.alertmsg = err.message
                    })
                }).catch(function(err){
                    console.log(err)
                    simplestore.alertmsg = err.message
                });
            }).catch(function(err){
                console.log(err)
                simplestore.alertmsg = err.message
            })
        }
    }
};
Vue.component('main-team-edit', MainTeamEdit);

//  ------------------- user -------------------
const MainUser = {
    template: `<b-table-simple hover small caption-top responsive>
                <b-thead head-variant="dark">
                    <b-tr>
                        <b-th colspan="1">Id</b-th>
                        <b-th colspan="2">Name</b-th>
                        <b-th colspan="2">Desc</b-th>
                        <b-th colspan="3">Email</b-th>
                        <b-th colspan="2">Fullname</b-th>
                    </b-tr>
                </b-thead>
                <b-tbody>
                    <b-tr v-for="user in shared.userarray" :key="user.id">
                        <b-th>  <router-link :to='"/user/"+user.id'> {{user.id}} </router-link> </b-th>
                        <b-th> {{user.name}} </b-th>
                        <b-th> {{user.desc}} </b-th>
                        <b-th> {{user.email}} </b-th>
                        <b-th> {{user.fullname}} </b-th>
                    </b-tr>
                </b-tbody>
            </b-table-simple>`,
    data: function(){
        return {
            shared: simplestore
        }
    },
    mounted(){
        axios.get("/user/").then(function(resp){
            simplestore.userarray = resp.data
        }).catch(function(err){
            simplestore.alertmsg = err.message
        })
    }
};
Vue.component('main-user', MainUser);

// -------------------- profile ----------------
const MainProfile = {
    template: `<div>
                <b-list-group>
                    <b-list-group-item>Username: {{shared.user.name}} </b-list-group-item>
                    <b-list-group-item>Fullname: {{shared.user.fullname}} </b-list-group-item>
                    <b-list-group-item>Description: {{shared.user.desc}} </b-list-group-item>
                    <b-list-group-item>Email: {{shared.user.email}} </b-list-group-item>

                    <b-list-group-item>Active?: {{shared.user.active}} </b-list-group-item>
                    <b-list-group-item>CodeCommit User: {{shared.user.ccname}} </b-list-group-item>
                    <b-list-group-item>CodeCommit Password: <button class="btn btn-secondary" v-on:click="resetccpasswd(shared.user.id)">Reset</button> </b-list-group-item>
                </b-list-group>
             </div>`,
    data: function(){
        return {
            user: simplestore.user,
            shared: simplestore
        }
    },
    mounted() {
        if (this.$route.params.userid) {
            uid = this.$route.params.userid
            axios.get('/user/'+uid).then(function(resp){
                user = resp.data
            }).catch(function(err){
                simplestore.alertmsg = err.message
            })
        }
    },
    methods: {
        resetccpasswd: function(userid) {
            axios.put("/user/"+userid+'/reset').then(function(){
                cc = resp.data
                msg = "WARNING: PASSWORD ONLY SHOW ONCE, PLEASE SAVE IT NOW!!! <BR>"
                msg += cc.ccpasswd
                simplestore.alertmsg=msg
            }).catch(function(err){
                simplestore.alertmsg=err.message
            })
        }
    }
};
Vue.component('main-profile', MainProfile);

// -------------------- login ----------------
const MainLogin = {
    template: `
        <b-container fluid>
            <b-row>
                <b-col sm="3">
                    <label>Username</label>
                </b-col>
                <b-col sm="9">
                    <b-form-input v-model="user"> </b-form-input>
                </b-col>
            </b-row>
            <b-row>
                <b-col sm="3">
                    <label>Password</label>
                </b-col>
                <b-col sm="9">
                    <b-form-input v-model="passwd" type="password"></b-form-input>
                </b-col>
            </b-row>
            <b-row> <b-button v-on:click="userlogin">Submit</b-button> </b-row>
        </b-container>
    `,
    data: function(){
        return {
            user : "",
            passwd : "",
            shared: simplestore
        }
    },
    methods: {
        userlogin: function(){
            chksum = sha256(this.user+sha256(this.user)+this.passwd+sha256(this.passwd))
            axios.post("/login", {"user": this.user, "passwd": chksum}).then(function(resp){
                simplestore.user = resp.data
                router.push('/')
            }).catch(function(err){
                console.log(err)
                simplestore.alertmsg = err.message
            })
        }
    }
};
Vue.component('main-login', MainLogin);

//  ------------------- Repo -------------------
const MainRepo = {
    template: `<b-table-simple hover small caption-top responsive>
                <b-thead head-variant="dark">
                    <b-tr>
                        <b-th colspan="1">Id</b-th>
                        <b-th colspan="2">Name</b-th>
                        <b-th colspan="2">Desc</b-th>
                        <b-th colspan="3">URL</b-th>
                        <b-th colspan="2">ARN</b-th>
                        <b-th colspan="2">RepoId</b-th>
                    </b-tr>
                </b-thead>
                <b-tbody>
                    <b-tr v-for="repo in shared.repos" :key="repo.id">
                        <b-th>  <router-link :to=repo.link> {{repo.id}} </router-link> </b-th>
                        <b-th> {{repo.name}} </b-th>
                        <b-th> {{repo.desc}} </b-th>
                        <b-th> {{repo.url}} </b-th>
                        <b-th> {{repo.arn}} </b-th>
                        <b-th> {{repo.repoid}} </b-th>
                    </b-tr>
                </b-tbody>
            </b-table-simple>`,
    data: function(){
        return {
            shared: simplestore
        }
    },
    mounted () {
        axios.get('/repo/').then(function(resp){
            simplestore.repos = resp.data
            simplestore.repos.forEach(function(val, idx){
                val['link'] = '/repo/'+ val.id
            })
        }).catch(function(err){
            console.log(err)
            simplestore.alertmsg = err.message
        })
    },
};
Vue.component('main-repo', MainRepo);

const MainRepoEdit = {
    template: `<b-container fluid>
                <b-row>
                    <b-col sm="3">
                        <label>repo name</label>
                    </b-col>
                    <b-col sm="9">
                        <b-form-input v-model="shared.currentRepo.name"> </b-form-input>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col sm="3">
                        <label>repo description</label>
                    </b-col>
                    <b-col sm="9">
                        <b-form-input v-model="shared.currentRepo.desc"></b-form-input>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col sm="3">
                        <label>repo team name</label>
                    </b-col>
                    <b-col sm="9">
                        <b-form-input v-model="team"></b-form-input>
                    </b-col>
                </b-row>                
                <b-row> 
                    <b-button class="btn btn-secondary" v-on:click="editperm(repoid)">Permission</b-button> 
                    <b-button class="btn btn-danger" v-on:click="submitrepo">Submit</b-button> 
                </b-row>
            </b-container>`,
    data: function(){
        return {
            team: "",
            repoid: this.$route.params.repoid,
            shared: simplestore
        }
    },
    mounted () {
        if (this.$route.params.repoid && this.$route.params.repoid != 0) {
            self = this
            axios.get('/repo/'+this.$route.params.repoid).then(function(resp){
                //this.project = resp.data
                simplestore.currentRepo = resp.data
                axios.get('/team/'+simplestore.currentRepo.teamid).then(function(resp){
                    self.team = resp.data.name
                })
                // debugging
                axios.get('/repo/'+self.$route.params.repoid+'/writer/').then(function(resp){
                    console.log(resp)
                }).catch(function(err){
                    console.log(err)
                simplestore.alertmsg = err.message
                })
            }).catch(function(err){
                console.log(err)
                simplestore.alertmsg = err.message
            })
        } else {
            simplestore.currentTeam = {
                "name" : "",
                "desc" : ""
            }
        }
    },
    methods: {
        submitrepo: function(){
            self = this
            team = this.team
            axios.get('/team/name/'+team).then(function(resp){
                teamid = resp.data.id
                simplestore.currentRepo.teamid = teamid
                if (self.repoid != 0) {
                    submitprom = axios.put('/repo/'+self.repoid, simplestore.currentRepo);
                } else {
                    submitprom = axios.post('/repo/', simplestore.currentRepo)
                }
                submitprom.then(function(resp){
                    simplestore.currentRepo = resp.data
                    router.push('/repo/')
                }).catch(function(err){
                    console.log(err)
                    simplestore.alertmsg = err.message
                });
            }).catch(function(err){
                console.log(err)
                simplestore.alertmsg = err.message
            })
        },
        editperm: function(repoid){
            router.push('/perm/'+repoid)
        }
    }
};
Vue.component('main-repo', MainRepoEdit);


// --------------- Perm ------------------
const MainPermEdit = {
    template : `<div>
                <b-list-group>
                    <b-list-group-item> <span>Reader: </span>
                        <span v-for="r in shared.currentRepoReader" :key="r.id" class="text-bg-info"> 
                            [ {{r.name}}
                            <button type="button" class="btn-close" aria-label="Close" v-on:click="deletereader(r.name)"></button> ] ,
                        </span>
                        <button type="button" class="btn btn-link" v-on:click="addreader()"> + </button>
                    </b-list-group-item> 
                    <b-list-group-item> <span>Writer: </span>
                        <span v-for="r in shared.currentRepoWriter" :key="r.id" class="text-bg-info"> 
                            [ {{r.name}} 
                            <button type="button" class="btn-close" aria-label="Close" v-on:click="deletewriter(r.name)"></button> ],
                        </span>
                        <button type="button" class="btn btn-link" v-on:click="addwriter()"> + </button>
                    </b-list-group-item>
                </b-list-group>
            </div>`,
    data: function(){
        return {
            repo: {},
            repoid: 0,
            shared: simplestore
        }
    },
    computed: {
    },
    mounted() {
        self = this
        repoid = this.$route.params.repoid
        this.repoid = repoid
        if (repoid && repoid != 0) {
            repoprom = axios.get('/repo/'+repoid);
            readerprom = axios.get('/repo/'+repoid+"/reader");
            writerprom = axios.get('/repo/'+repoid+"/writer");
            Promise.all([repoprom, readerprom, writerprom]).then(function(resps){
                self.repo = resps[0].data
                simplestore.currentRepoReader = resps[1].data
                simplestore.currentRepoWriter = resps[2].data
            }).catch(function(err){
                simplestore.alertmsg = err.message
            })
        } else {
            shared.alertmsg = "no repoid here";
            router.push(-1)
        }

    },
    methods: {
        deletereader: function(rid){
            axios.delete('/repo/'+this.repoid+"/reader/"+rid).then(function(resp){
            })
        },
        addreader: function(){
            newuser = prompt("input the username")
            axios.post('/repo/'+this.repoid+"/reader/", {"user": newuser}).then(function(resp){
                simplestore.currentRepoReader = resp.data
            })
        },
        deletewriter: function(rid){
            axios.delete('/repo/'+this.repoid+"/writer/"+rid).then(function(resp){
            })
        },
        addwriter: function(){
            newuser = prompt("input the username")
            axios.post('/repo/'+this.repoid+"/writer/", {"user": newuser}).then(function(resp){
                simplestore.currentRepoWriter = resp.data
            })
        }

    }
};
Vue.component('main-perm', MainPermEdit);
