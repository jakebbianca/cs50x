function displayPosts(
    posts,
    posterID=null,
    postersIDs=null,
    prevCursor=null,
    nextCursor=null,
    userID=null) {

    // get container embedded in template to display posts and 
    // clear any existing inner content ahead of loading posts
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

            let currentPostID = post.post

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

            // Provide edit functionality for front-end for user's own posts
            if (userID == posterID) {

                // Create edit button on user's own posts
                let editButton = document.createElement('button');
                editButton.textContent = 'Edit';
                editButton.setAttribute('class', 'btn btn-secondary');

                // Create submission button for editing posts
                let editSubmitButton = document.createElement('button');
                editSubmitButton.textContent = 'Submit edited post';
                editSubmitButton.setAttribute('class', 'btn btn-secondary');
                editSubmitButton.hidden = true;
                editSubmitButton.disabled = true;

                subtitleContainer.append(editButton, editSubmitButton);

                let originalText = postContent.innerHTML
                let postContentTextarea = document.createElement('textarea')
                postContentTextarea.value = originalText
                postContentTextarea.hidden = true;
                postContainer.append(postContentTextarea);

                let editButtonClicked = false;
                let editSubmitClicked = false;


                editButton.onclick = () => {

                    // Confirm that edit button is clicked
                    editButtonClicked = true;

                    // hide original post text and show text area
                    postContent.hidden = true;
                    postContentTextarea.hidden = false;
                    
                    // hide edit button, show and enable submit button
                    editButton.hidden = true;
                    editButton.disabled = true;
                    editSubmitButton.hidden = false;
                    editSubmitButton.disabled = false;

                    // reset clicked variables
                    if (editSubmitClicked === true) {
                        editSubmitClicked = false
                    }

                }

                editSubmitButton.onclick = () => {

                    // if edit button was never clicked, refresh the page
                    if (editButtonClicked === false) {
                        location.reload()
                    }

                    // if textarea is never created, refresh the page
                    if (!(postContentTextarea) in window) {
                        location.reload()
                    }

                    // if there is no original text to reference, refresh page
                    if (!(originalText) in window) {
                        location.reload()
                    }

                    if (postContentTextarea.value != originalText) {
                        
                        editPost(postID=currentPostID, newText=postContentTextarea.value)
                        location.reload()

                    } else {

                        editButtonClicked = false;
                        postContentTextarea.hidden = true;
                        postContent.hidden = false;
                        editSubmitButton.hidden = true;
                        editSubmitButton.disabled = true;
                        editButton.hidden = false;
                        editButton.disabled = false;
                        editSubmitClicked = true;

                    }

                }


            }

            // Handle case if post was edited
            if (post.edit_bool == true) {

                // create element, fill in with timestamp, append to subtitle, set attributes, etc.
                postEditDatetime = document.createElement('span')
                postEditDatetime.innerHTML = ` and updated ${post.edit_datetime}`
                subtitleContainer.append(postEditDatetime);
                postEditDatetime.setAttribute('class', 'post-datetime')

            }

        });

        // Create elements for page buttons and store cursor values
        let buttonsContainer = document.querySelector('.posts-page-btns-ctn');
        buttonsContainer.innerHTML = '';
        let prevButton = document.createElement('button');
        let nextButton = document.createElement('button');

        // Set text content for buttons
        prevButton.textContent = 'Previous'
        nextButton.textContent = 'Next'

        // Set types to buttons
        prevButton.type = 'button'
        nextButton.type = 'button'

        // Set bootstrap button classes
        prevButton.setAttribute('class', 'btn btn-secondary')
        nextButton.setAttribute('class', 'btn btn-secondary')

        // Set values and onClick events for prev and next buttons
        // Only if matching cursor has value, otherwise not needed
        if (prevCursor != null) {
            prevButton.value = prevCursor;
            prevButton.onclick = () => {
                getPosts(
                    posterID,
                    postersIDs,
                    prevCursor,
                    nextCursor,
                    clickedPrev = true,
                    clickedNext = null
                )
            }
        } else {
            prevButton.disabled = true;
        }

        if (nextCursor != null) {
            nextButton.value = nextCursor;
            nextButton.onclick = () => {
                getPosts(
                    posterID,
                    postersIDs,
                    prevCursor,
                    nextCursor,
                    clickedPrev = null,
                    clickedNext = true
                )
            }

        } else {
            nextButton.disabled = true;
        }

        // attach buttons to container
        buttonsContainer.append(prevButton, nextButton)

    }

    window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'smooth'
    });
}


function getPosts(
    posterID=null,
    postersIDs=null,
    prevCursor=null,
    nextCursor=null,
    clickedPrev=null,
    clickedNext=null
    ) {

    // initialize url variable to later use in fetch call to load posts
    const url = 'posts'

    // create POST request providing poster ids to the server
    // run function to generate HTML for posts
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            poster_id: posterID,
            posters_ids: postersIDs,
            prev_cursor: prevCursor,
            next_cursor: nextCursor,
            clicked_prev: clickedPrev,
            clicked_next: clickedNext
        })
    })
    .then(response => response.json())
    .then(data => {
        displayPosts(
            data.posts,
            data.posterID,
            data.postersIDs,
            data.prevCursor,
            data.nextCursor,
            data.user_id)
    })
    .catch((error) => {
        console.error('Error:', error)
    })
}


async function editPost(postID, newText) {

    const response = await fetch(`post/${postID}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: newText,
        })
    });

    // if response is not ok, throw error, else, log the result
    if (!response.ok) {
        const message = `Error: ${response.status}`;
        throw new Error(message);
    } else {
        const result = await response.json();
        console.log(result);
    }
}