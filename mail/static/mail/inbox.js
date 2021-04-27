document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // Use submit button to send email, load sent mailbox, and prevent full form submission to Django server
    document.querySelector('#compose-form').onsubmit = () => {
        send_email();
        setTimeout(() => {load_mailbox('sent'); }, 100);
        return false;
    }

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    // Show emails within certain mailbox
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

        emails.forEach(email => {

            // Initialize html elements for each email in the mailbox
            var emailsContainer = document.createElement('div');
            var emailsSender = document.createElement('h4');
            var emailsSubject = document.createElement('p');
            var emailsTimestamp = document.createElement('p');

            // Update innerHTML of elements to include relevant email information
            emailsSender.innerHTML = `${email.sender}`;
            emailsSubject.innerHTML = `${email.subject}`;
            emailsTimestamp.innerHTML = `${email.timestamp}`;

            // Update style and classes of new elements
            emailsContainer.style.border = '1px solid black';
            if (email.read === true) {
                emailsContainer.style.backgroundColor = 'lightgrey';
            }; 

            // Append to created div container
            emailsContainer.append(emailsSender);
            emailsContainer.append(emailsSubject);
            emailsContainer.append(emailsTimestamp);

            // Append created div container within outer #emails-view div
            document.querySelector('#emails-view').append(emailsContainer);

            // Load view of specific email on click
            emailsContainer.addEventListener('click', () => {
                load_email(email);
                console.log('Specific email has been clicked.');
            });
        });
        console.log(emails);
    });
}

/* Send Mail: When a user submits the email composition form, add JavaScript code to actually send the email.
You’ll likely want to make a POST request to /emails, passing in values for recipients, subject, and body.
Once the email has been sent, load the user’s sent mailbox. */

// Create function that will send the email and then load the user's sent mailbox.
// Add event listener to 'send' button on 'compose' view

function validate_email(emailAddress) {
    // Define regex for email format and test input
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(emailAddress);
}

function send_email() {

    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: document.querySelector('#compose-recipients').value,
            subject: document.querySelector('#compose-subject').value,
            body: document.querySelector('#compose-body').value
        })
    })
    // .then(response => response.json())
    .then(response => response.text())
    .then(result => {
        // Print result
        console.log(result)
    })
    .catch(error => {
        console.log('Error:', error);
        alert(error);
    });
}

function load_email(email) {
    return;
}