var app = new Vue({
    el: '#TwitterFriend',
    delimiters: ['${', '}'],

    data() {
        return {
            logname: "",
            firstLogin: true,

            showWelcome: false,
            showTable: false,
            showSpinner: false,

            friends: [],
        };
    }, // End data

    mounted() {
        console.log('mounted')

        // Get first login value
        let loginString = this.$refs.login_elem.value;
        if (loginString == "True") {
            this.firstLogin = true;
        }
        else {
            this.firstLogin = false;
        }

        // Get first login name
        let userString = this.$refs.login_name.value;

        if (!this.firstLogin && userString != "") {
            this.fetchData();
        }
        else {
            this.showWelcome = true;
        }
    }, // End on mounted

    methods: {

        fetchData: function() {
            this.showWelcome = false;
            this.showTable = true;
            this.showSpinner = true;

            this.getFriendList();
        },

        getFriendList: function() {
            var self = this;
            axios
            .get('/api/friends/')
            .then(function (response) {
                self.logname = response.data.logname;
                response.data.friends.forEach(function (friend) {
                    self.friends.push(friend)
                });
                self.showSpinner = false;
              })
            .catch(error => console.log(error))
        }

    }, // End Vue methods

    filters: {

    } // End filters
})