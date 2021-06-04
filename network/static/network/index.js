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
    

    // On submit of new post form, send info to server
    document.querySelector('#new-post-form').onsubmit = async (e) => {

        e.preventDefault();
        // submitNewPost()
    }    
});
