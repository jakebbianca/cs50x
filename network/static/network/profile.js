document.addEventListener('DOMContentLoaded', function () {

    let username = document.querySelector('#profile-username');
    let followers = document.querySelector('#followers');
    let following = document.querySelector('#following');

    getUser(profile_id, username, followers, following);

    getPosts(profile_id);

})