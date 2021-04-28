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
    document.querySelector('#email-view').style.display = 'none';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    // Show emails within certain mailbox
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

        emails.forEach(email => {

            // Initialize html elements for each email in the mailbox
            let emailsContainer = document.createElement('div');
            let emailsSender = document.createElement('h4');
            let emailsSubject = document.createElement('p');
            let emailsTimestamp = document.createElement('p');

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
            emailsContainer.append(emailsSender, emailsSubject, emailsTimestamp);

            // Append created div container within outer #emails-view div
            document.querySelector('#emails-view').append(emailsContainer);

            // Load view of specific email on click
            emailsContainer.addEventListener('click', () => {
                load_email(email, mailbox);
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

function load_email(email, mailbox) {

    // Show the email and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    // TODO NOT WORKING -- Remove any pre-existing email information that was added to HTML
    document.querySelector('#emails-view').innerHTML = '';

    // Make API call to get info for specific email
    fetch(`/emails/${email.id}`)
    .then(response => response.json())
    .then(email => {

        // Create HTML elements to display email
        let emailHeader = document.createElement('div');
        let emailSender = document.createElement('p');
        let emailRecipients = document.createElement('p');
        let emailSubject = document.createElement('p');
        let emailsTimestamp = document.createElement('p');
        let emailBodyContainer = document.createElement('div');
        let emailBody = document.createElement('p');

        // Insert email information HTML into new elements
        emailSender.innerHTML = `<b>From:</b> ${email.sender}`;
        emailRecipients.innerHTML = `<b>To:</b> ${email.recipients}`;
        emailSubject.innerHTML = `<b>Subject:</b> ${email.subject}`;
        emailsTimestamp.innerHTML = `<b>Timestamp:</b> ${email.timestamp}`;
        emailBody.innerHTML = `<hr>\n${email.body}`;

        // Append email information within container elements
        emailHeader.append(emailSender, emailRecipients, emailSubject, emailsTimestamp);
        emailBodyContainer.append(emailBody);

        // Give container elements ids, will be useful to remove later before loading new email
        emailHeader.setAttribute('id', 'email-header')
        emailBodyContainer.setAttribute('id', 'email-body-ctn')

        // Create archive button if email is in inbox and append to header
        // If clicked, archive the email and load fresh inbox
        if (mailbox === 'inbox') {
            let archiveButton = document.createElement('button');
            archiveButton.innerHTML = 'Archive this email'
            archiveButton.addEventListener('click', () => {
                fetch(`/emails/${email.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        archived: true
                    })
                })
                load_mailbox('inbox');
            });
            emailHeader.append(archiveButton);
        }

        // Append created divs to email-view container
        document.querySelector('#email-view').append(emailHeader, emailBodyContainer);

        // Mark email as read when opening for the first time
        if (email.read === false) {
            fetch(`/emails/${email.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true
                })
            });
        }

    });

}