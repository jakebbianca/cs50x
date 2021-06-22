function displayPosts(posts) {

    // get container embedded in template to display posts and clear any existing inner content ahead of loading posts
    let container = document.querySelector('.posts-ctn');
    container.innerHTML = '';

    // if there are no posts, display a message to that end
    if (posts === null || posts.length === 0) {

        let message = document.createElement('h4');
        message.innerHTML = "There are no posts available.";

        container.append(message);
    
    } else {

        // create elements and styling for each post being fetched
        posts.forEach(post => {

            // Create the elements for each post
            let postContainer = document.createElement('div');
            let subtitleContainer = document.createElement('div');
            let postPosterLink = document.createElement('a');
            let postDatetime = document.createElement('span');                
            let postContent = document.createElement('p');
            // let postLikes = document.createElement('h3');

            // Append inner elements to container
            container.append(postContainer);
            postContainer.append(subtitleContainer, postContent);
            subtitleContainer.append(postPosterLink, postDatetime);

            // Fill in elements with data from fetch call and append to container div
            postPosterLink.innerHTML = `${post.poster_username}`;
            postDatetime.innerHTML = `\tPosted ${post.post_datetime}`;
            postContent.innerHTML = `${post.content}`;
            // postLikes = probably fetch call, may want to change Post model so that likes counter is held there too

            // Add core attributes -- classes, ids, etc.
            postContainer.setAttribute('class', 'post-ctn');
            postPosterLink.setAttribute('class', 'poster-name');
            postDatetime.setAttribute('class', 'post-datetime')

            // Add link which redirects to user's profile page
            postPosterLink.setAttribute('href', `${post.poster_url}`)

            // Handle case if post was edited
            if (post.edit_bool == true) {

                // create element, fill in with timestamp, append to subtitle, set attributes, etc.
                postEditDatetime = document.createElement('span')
                postEditDatetime.innerHTML = ` and updated ${post.edit_datetime}`
                subtitleContainer.append(postEditDatetime);
                postEditDatetime.setAttribute('class', 'post-datetime')

            }

        });
    }
}

function getPosts(posterID=null, postersIDs=null) {

    // initialize url variable to later use in fetch call to load posts
    var url = undefined

    // if multiple posters' IDs are not specified, GET posts for one or all users
    // if specified, run POST request to send IDs to allow retrieval
    if (postersIDs === null) {

        // if no poster is specified, specify API url for all posts
        // if poster is specified, specify API url for only that user's posts
        if (posterID === null) {
            url = 'posts'
        } else {
            url = `posts/${posterID}`
        }

        // make GET call to load posts
        // run function to generate HTML for posts
        fetch(url)
        .then(response => response.json())
        .then(posts => {
            displayPosts(posts)
        });

    } else {

        url = 'posts'
        // create POST request providing poster ids to the server
        // run function to generate HTML for posts
        fetch(url, {
            method: 'POST',
            body: JSON.stringify({
                posters_ids: postersIDs
            })
        })
        .then(response => response.json())
        .then(posts => {
            displayPosts(posts)
        })
        .catch((error) => {
            console.error('Error:', error)
        })

    }

}
