document.addEventListener('DOMContentLoaded', function() {

    // get all posts
    // function defined in getposts.js
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
    }

    content.value = ''

}