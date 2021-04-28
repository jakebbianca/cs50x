document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', () => compose_email(false));

    // Use submit button to send email, load sent mailbox, and prevent full form submission to Django server
    document.querySelector('#compose-form').onsubmit = () => {
        // send email
        // if successful, load sent mailbox
        // otherwise, send_email function will send alert message and maintain compose view with filled form data
        if (send_email()) {
            setTimeout(() => {load_mailbox('sent'); }, 100);
        }
        // return false to prevent Django form submission
        return false;
    }

    // Hide alert message div by default
    document.querySelector('#message').style.display = 'none';

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email(reply, recipients, subject, body) {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#message').style.display = 'none';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

    if (reply) {
        document.querySelector('#compose-recipients').value = `${recipients}`;
        document.querySelector('#compose-subject').value = `${subject}`;
        document.querySelector('#compose-body').value = `${body}`;
    }
}

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';

    if (mailbox !== 'sent') {
        document.querySelector('#message').style.display = 'none';
    }

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

// Function to validate email addresses on client side
// regex for approximate RFC2822 validation found at https://regexr.com/2rhq7
function validateEmail(emailAddress) {
    const re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
    return re.test(String(emailAddress).toLowerCase());
}

async function send_email() {

    var recipients = document.querySelector('#compose-recipients').value;
    var subject = document.querySelector('#compose-subject').value;
    var body = document.querySelector('#compose-body').value;
    var success = false;

    alertMessage = document.querySelector('#message');

    // Validate recipients
    if (recipients !== '') {

        // Get email addresses separated by commas in case multiple recipients are entered
        let recipientsSplit = recipients.split(',');

        // Check each recipient email address for validity
        var recipientsAreValid = true;

        recipientsSplit.forEach(recipient => {
            if (!validateEmail(recipient)) {
                recipientsAreValid = false;
                return;
            }
        });

        // if all recipients are valid, send the email
        if (recipientsAreValid) {

            const response = await fetch('/emails', {
                method: 'POST',
                body: JSON.stringify({
                    recipients: recipients,
                    subject: subject,
                    body: body
                })
            })

            if (!response.ok) {
                const message = `Error: ${response.status}`;
                throw new Error(message);
            } else {
                const result = await response.json()
                // Print result
                console.log(result);
                if (result['error']) {
                    // if there is any error even after validation, send alert message to user
                    compose_email(true, recipients, subject, body);
                    alertMessage.innerHTML = 'Please ensure that all provided recipient email addresses are valid, separated by commas.';
                    alertMessage.style.display = 'block';
                    alertMessage.setAttribute('class', 'alert alert-danger mt-3');
                    return success;
                } else {
                    // if POST is successful, hide the alert message and confirm with success variable
                    alertMessage.innerHTML = 'Email was sent successfully.';
                    alertMessage.style.display = 'block';
                    alertMessage.setAttribute('class', 'alert alert-success mt-3');
                    success = true;
                }

            }

        } else {
            // if any recipient is invalid, send alert message to user
            compose_email(true, recipients, subject, body);
            alertMessage.innerHTML = 'Please ensure that all provided recipient email addresses are valid, separated by commas.';
            alertMessage.style.display = 'block';
            alertMessage.setAttribute('class', 'alert alert-danger mt-3');
        }

    } else {
        // If no input in recipients field, send alert message to user
        compose_email(true, recipients, subject, body);
        alertMessage.innerHTML = 'Please enter at least one valid email address.'
        alertMessage.style.display = 'block';
        alertMessage.setAttribute('class', 'alert alert-danger mt-3');
    }

    return success;
    
}

function load_email(email, mailbox) {

    // Remove any pre-existing email information that was added to HTML
    document.querySelector('#email-view').innerHTML = '';

    // Show the email and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    // Make API call to get info for specific email
    fetch(`/emails/${email.id}`)
    .then(response => response.json())
    .then(email => {

        // Mark email as read when opening for the first time
        if (!email.read) {
            fetch(`/emails/${email.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true
                })
            });
        }

        // Create HTML elements to display email
        let emailHeader = document.createElement('div');
        let emailSender = document.createElement('p');
        let emailRecipients = document.createElement('p');
        let emailSubject = document.createElement('p');
        let emailsTimestamp = document.createElement('p');
        let emailBodyContainer = document.createElement('div');
        let emailBody = document.createElement('p');
        let replyButton = document.createElement('button');

        // Insert email information/HTML into new elements
        emailSender.innerHTML = `<b>From:</b> ${email.sender}`;
        emailRecipients.innerHTML = `<b>To:</b> ${email.recipients}`;
        emailSubject.innerHTML = `<b>Subject:</b> ${email.subject}`;
        emailsTimestamp.innerHTML = `<b>Timestamp:</b> ${email.timestamp}`;
        emailBody.innerHTML = `<hr>\n${email.body}`;
        replyButton.innerHTML = 'Reply';

        // When user clicks reply button, show them the compose view and fill in fields appropriately
        replyButton.addEventListener('click', () => {
            let reply = true;
            var subject = email.subject;
            if (subject.substring(0,3) !== 'RE:') {
                subject = `RE: ${subject}`;
            }
            let body = `\n\nOn ${email.timestamp} ${email.sender} wrote:\n\t${email.body}`;
            compose_email(reply, email.sender, subject, body);
        });

        // Append email information within container elements
        emailHeader.append(emailSender, emailRecipients, emailSubject, emailsTimestamp, replyButton);
        emailBodyContainer.append(emailBody);

        // Give container elements ids, will be useful to remove later before loading new email
        emailHeader.setAttribute('id', 'email-header')
        emailBodyContainer.setAttribute('id', 'email-body-ctn')

        // Create archive or unarchive button if email is in inbox or archive respectively
        // If clicked, archive the email and load fresh inbox
        if (mailbox !== 'sent') {
            let archiveButton = document.createElement('button');
            if (mailbox === 'inbox') {
                archiveButton.innerHTML = 'Move to Archive';
                let archivedUpdate = true;
                load_archive_button(email, archiveButton, archivedUpdate);
            } else {
                // if mailbox === 'archive'
                archiveButton.innerHTML = 'Remove from Archive';
                let archivedUpdate = false;
                load_archive_button(email, archiveButton, archivedUpdate);
            }

            // Append archive/unarchive button to email header
            emailHeader.append(archiveButton);
        }

        // Append created divs to email-view container
        document.querySelector('#email-view').append(emailHeader, emailBodyContainer);

    });

}

function load_archive_button(email, archiveButton, archivedUpdate) {

    // Make PUT request to API to update archive status on click
    archiveButton.addEventListener('click', () => {
        fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: archivedUpdate
            })
        })
        setTimeout(() => {load_mailbox('inbox'); }, 100);
    });

}