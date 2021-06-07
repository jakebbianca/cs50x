// What this file needs to do...

// Display all posts from all users in reverse chronological order
// Display 10 posts at a time, paginated (per spec, would rather try infinite scroll)
// Post must show username of poster, post content, date and time of post, edit date if applicable, and number of likes
// Maybe? add a refresh button that can be clicked at any time by the user -- not sure if this is redundant with browser reset button
// Clicking a username should redirect to a user's profile page -- I will do this on the back end


// Load 10 most recent posts
// --> go to next page of posts
// Load 10 next most recent posts
// With or without reloading posts? If new posts come in, don't want to redisplay some new and some old


document.addEventListener('DOMContentLoaded', function() {

    // get all posts
    getPosts()

    // On submit of new post form, send info to server
    document.querySelector('#new-post-form').onsubmit = async (e) => {

        // prevent default form submit
        e.preventDefault();
        // submit new post and refresh posts after completion
        await makePost();
        getPosts()
        // prevent Django form submission and page refresh
        return false;
    }    
});


function getPosts(poster=null) {

    // get container embedded in template to display posts and clear any existing inner content ahead of loading posts
    let container = document.querySelector('.posts-ctn');
    container.innerHTML = '';

    // initialize url variable to later use in fetch call to load posts
    var url = undefined

    // if no poster is specified, specify API url for all posts
    // if poster is specified, specify API url for only that user's posts
    if (poster === null) {
        url = 'posts'
    } else {
        url = `posts/${poster}`
    }

    // make GET call to load posts
    fetch(url)
    .then(response => response.json())
    .then(posts => {

        // if there are no posts, display a message to that end
        if (posts.length === 0) {

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
                let postPoster = document.createElement('span');
                let postDatetime = document.createElement('span');                
                let postContent = document.createElement('p');
                // let postLikes = document.createElement('h3');

                // Append inner elements to container
                container.append(postContainer);
                postContainer.append(subtitleContainer, postContent);
                subtitleContainer.append(postPoster, postDatetime);

                // Fill in elements with data from fetch call and append to container div
                postPoster.innerHTML = `${post.poster_username}`;
                postDatetime.innerHTML = `\tPosted ${post.post_datetime}`;
                postContent.innerHTML = `${post.content}`;
                // postLikes = probably fetch call, may want to change Post model so that likes counter is held there too

                // Add classes, ids, etc.
                postContainer.setAttribute('class', 'post-ctn');
                postPoster.setAttribute('class', 'poster-name');
                postDatetime.setAttribute('class', 'post-datetime')

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
    });
}

async function makePost() {

    // store content from new post form
    let content = document.querySelector('#new-post-content').value;

    const response = await fetch('new', {
        method: 'POST',
        body: JSON.stringify({
            content: content
        })
    });

    // if response is not ok, throw error, else, log the result
    if (!response.ok) {
        const message = `Error: ${response.status}`;
        throw new Error(message);
    } else {
        const result = await response.json();
        console.log(result);
        return;
    }

}