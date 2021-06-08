function getUser(id, username, followers, following) {
    
    fetch(`user/${id}`)
    .then(response => response.json())
    .then(user => {
        username.innerHTML = user.username
        followers.innerHTML = user.followers;
        following.innerHTML = user.following;
    })

}