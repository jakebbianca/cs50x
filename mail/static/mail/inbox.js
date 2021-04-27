document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // Use submit button to send email, load sent mailbox, and prevent full form submission to Django server
    document.querySelector('#compose-form').onsubmit = () => {
        send_email();
        load_mailbox('sent');
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

    // Show emails within certain mailbox, starting with most recent
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        // sort emails
        emails.sort()
        emails.forEach(email => {
            // Initialize html elements for each email in the mailbox
            var emailsContainer = document.createElement('div');
            var emailsSender = document.createElement('h4');
            var emailsSubject = document.createElement('p');

            // Update the innerHTML for each inner element and append them to the newly created div
            emailsSender.innerHTML = `${email.sender}`;
            emailsSubject.innerHTML = `${email.subject}`;
            emailsContainer.append(emailsSender)
            emailsContainer.append(emailsSubject)

            emailsContainer.addEventListener('click', () => {
                load_email(email);
                console.log('Specific email has been clicked.');
            })
            document.querySelector('#emails-view').append(emailsContainer);
        })
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
    .then(response => response.json())
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