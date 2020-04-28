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

                    friend.needsUpdate = self.friendNeedsUpdate(friend);
                    self.friends.push(friend)


                });

                self.showSpinner = false;
                self.getFriendData();
              })
            .catch(error => console.log(error))
        },

        friendNeedsUpdate: function(friendData) {

            if (friendData.stressed != null) {
                var date = new Date(friendData.checked);
                var now = new Date();
                var sevenDays = 7 * 24 * 60 * 60 * 1000

                if (now.getTime() - date.getTime() > sevenDays) { // if the data is more than 7 days old:
                    return true;
                }
                return false;
            }
            return true;
        },

        getFriendData: async function() {
            console.log("getFriendData");
            // For each friend object, get the data, and update them
            var self = this;

            for (let i = 0; i < self.friends.length; i++) {
                request = axios.get(self.friends[i].url)
                await request.then(function (response) {
                    self.logname = response.data.logname;

                    self.friends[i].checked = response.data.checked;
                    self.friends[i].stressed = response.data.stressed;
                    self.friends[i].needsUpdate = false;
                  })
                .catch(error => console.log(error))
            }
        }

    }, // End Vue methods

    filters: {

    } // End filters
})