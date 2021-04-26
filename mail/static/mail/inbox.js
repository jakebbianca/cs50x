document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // Use submit button to send email and prevent normal submission to Django
    document.querySelector('#compose-form').onsubmit = function() {
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

    // Get list of recipient email addresses, remove all white space, and split on commas per Project 3 spec
    var recipientsInput = document.querySelector('#compose-recipients').value.replace(/\s+/g, '');
    var recipients = recipientsInput.split(',');

    // client-side email validation check
    var message = "";
    var recipientsAreValid = false;
    recipients.forEach(recipient => {
        if (!validate_email(recipient)) {
            message += "'" + recipient + "' is NOT a valid email address.\n"
        }
    });

    // If any recipient emails are invalid, warn the user
    // Otherwise, attempt to send the email
    if (message) {
        message += "Please confirm that all email addresses are valid before sending.";
        alert(message);
    } else {
        fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
                recipients: recipients,
                subject: document.querySelector('#compose-subject').value,
                body: document.querySelector('#compose-body').value
            })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result)
        });
    }
}