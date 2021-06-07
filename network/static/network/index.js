// What this file needs to do...

// At the top of the page, load a form to submit a new post
// If submitted, make a fetch POST call to submit the post to the server

// Display all posts from all users in reverse chronological order
// Display 10 posts at a time, paginated (per spec, would rather try infinite scroll)
// Post must show username of poster, post content, date and time of post, edit date if applicable, and number of likes
// Maybe? refresh posts when user submits a new post
// Maybe? add a refresh button that can be clicked at any time by the user -- not sure if this is redundant with browser reset button
// Clicking a username should redirect to a user's profile page -- I will do this on the back end


// Load 10 most recent posts
// --> go to next page of posts
// Load 10 next most recent posts
// With or without reloading posts? If new posts come in, don't want to redisplay some new and some old


document.addEventListener('DOMContentLoaded', function() {

    // get all posts
    get_posts()

    // On submit of new post form, send info to server
    document.querySelector('#new-post-form').onsubmit = async (e) => {

        // prevent Django form submission
        e.preventDefault();
        // submitNewPost()
    }    
});


function get_posts(poster=null) {

    var url = undefined

    // if no poster is specified, load all posts
    if (poster === null) {
        url = 'posts/'
    } else {
        url = `posts/${poster}`
    }

    fetch(url)
    .then(response => response.json())
    .catch(error => console.error('Error:', error))
    .then(posts => {

        console.log(posts)

        // if there are no posts, display a message to confirm that
        // if there are posts, display each in its own container
        if (posts.length === 0) {

            let message = document.createElement('h4');
            message.innerHTML = "There are no posts available.";

            let container = document.querySelector('.posts-ctn');
            container.append(message);
        
        } else {

            posts.forEach(post => {

                // Create html elements for each post
                let postContainer = document.createElement('div');
                let postPoster = document.createElement('h3');
                let postContent = document.createElement('p');
                let postDatetime = document.createElement('h3');
                // let postLikes = document.createElement('h3');

                // Append inner elements to container
                container.append(postContainer);
                postContainer.append(postPoster, postContent, postDatetime);

                // Fill in elements with data from fetch call and append to container div
                postPoster.innerHTML = `${post.poster}`;
                postContent.innerHTML = `${post.content}`;
                // postLikes = probably fetch call, may want to change Post model so that likes counter is held there too

                // check if post has been edited and update html elements to show if yes
                if (post.edit_bool == true) {
                    let postEditDatetime = document.createElement('h3');
                    postEditDatetime.innerHTML = `Updated on ${post.edit_datetime}`;
                    postDatetime.innerHTML = `Originally posted on ${post.post_datetime}`;
                    postContainer.append(postDatetime, postEditDateimte);
                } else {
                    postDatetime.innerHTML = `Posted on ${post.post_datetime}`;
                    postContainer.append(postDatetime);
                }
                
            });

        }
   
    });
}