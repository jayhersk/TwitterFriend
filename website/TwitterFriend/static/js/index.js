var app = new Vue({
    el: '#TwitterFriend',
    delimiters: ['${', '}'],

    data() {
        return {
            logname: "",
            firstLogin: true,

            friend_usernames: []
        };
    }, // End data

    mounted() {
        
    }, // End on mounted

    methods: {

        getFriendList: function() {
            var self = this;
            axios
            .get('/api/friends/')
            .then(function (response) {
                self.logname = response.data.logname;
                response.data.friends.forEach(function (friend) {
                    self.friend_usernames.push(friend.f_username)
                });
                console.log(self.friend_usernames);
              })
            .catch(error => console.log(error))
        }

    }, // End Vue methods

    filters: {

    } // End filters
})