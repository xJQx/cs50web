document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', event => send_mail(event));

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails_view = document.querySelector('#emails-view');
    console.log(emails);
    for (email in emails)
    {
      const div = document.createElement('div');
      const br = document.createElement('br');

      // get info 
      sender = emails[email].sender;
      subject = emails[email].subject;
      timestamp = emails[email].timestamp;
      read = emails[email].read;
      id = parseInt(emails[email].id);

      // create event listener for div
      div.addEventListener('click', () => {
        email_id = div.getAttribute('id');
        view_email(email_id, mailbox);
      })

      // create HTML elements and apply style
      div.id = id;
      div.setAttribute('name', 'email');
      div.innerHTML = '<span style="width: 20%;"><b>' + sender + '</b></span>' + '<span style="width: 30%;">' + subject + '</span>' + '<span style="color: grey; text-align: right; width: 50%;">' + timestamp + '</span>';
      
      // if email is read, change background color to grey
      if (read === true)
      {
        div.setAttribute('style', 'background-color: lightgrey; border: solid 2px black; padding: 7px; text-align: left; display: flex;');
      }
      else
      {
        div.setAttribute('style', 'background-color: white; border: solid 2px black; padding: 7px; text-align: left; display: flex;');
      }
      
      emails_view.append(div);
      emails_view.append(br);
    }
  })

  // View email when clicked on
  document.querySelectorAll("div[name='email']").forEach(email => {
    email.addEventListener('click', () => {
      alert("hi");
      view_email(this.id);
    })
  })

}

function send_mail(event) {
  event.preventDefault();
  recipients = document.querySelector('#compose-recipients').value;
  subject = document.querySelector('#compose-subject').value;
  body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => {
    if (!response.ok)
    {
      response.json().then(result => {
        alert(result.error);
      });
        compose_email();
    }
    else
    {
      response.json();
      load_mailbox('sent');
    }
  })
  .then(result => {
    console.log(result);
  })
}

function view_email(email_id, mailbox) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      // hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      
      // show email view and clear previous email view
      document.querySelector('#email').style.display = 'block';
      document.querySelector("#email").innerHTML = "";

      // show email
      const div = document.createElement('div');
      div.innerHTML = '<h2>Subject: ' + `${email.subject}` + '</h2>' + '<p><b>Sender: </b>' + `${email.sender}` + '</p>' +
                      '<p><b>Recipient(s): </b>' + `${email.recipients}` + '</p>' + 
                      '<textarea disabled cols="40" rows="5">' + `${email.body}` + '</textarea>' +
                      '<p><b>Time Sent: </b>' + `${email.timestamp}` + '</p>';

      document.querySelector("#email").append(div);


      // reply function
      const reply_button = document.createElement('button');
      reply_button.id = 'reply';
      reply_button.innerHTML = 'Reply';
      reply_button.addEventListener('click', function () {
        reply(email);
      })

      document.querySelector('#email').append(reply_button);
      
      // enable archiving for inbox and archived sections
      const br = document.createElement('br');
      document.querySelector('#email').append(br);

      if (mailbox === 'inbox')
      {
        const form = document.createElement('form');
        document.querySelector('#email').append(br);
        form.setAttribute('onsubmit', `archive("archive", "${email_id}")`);
        form.innerHTML = '<input type= "submit" value= "Archive">';
        document.querySelector('#email').append(form);
      }
      else if (mailbox === 'archive')
      {
        const form = document.createElement('form');
        form.setAttribute('onsubmit', `archive("unarchive", "${email_id}")`);
        form.innerHTML = '<input type= "submit" value= "Unarchive">';
        document.querySelector('#email').append(form);
      }
      
      
  });

  // change email to read
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

function archive(type, email_id)
{
  if (type === 'archive')
  {
    fetch(`/emails/${email_id}`, {
      method: "PUT",
      body: JSON.stringify({
        archived: true
      })
    })
  }
  else if (type === 'unarchive')
  {
    fetch(`/emails/${email_id}`, {
      method: "PUT",
      body: JSON.stringify({
        archived: false
      })
    })
  }
}

function reply(email)
{
  // hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  
  // show email view and clear previous email view
  document.querySelector('#email').style.display = 'block';
  document.querySelector("#email").innerHTML = "";
  
  const div = document.createElement('div');
  div.innerHTML = `<h3>Reply Email</h3>
                      <form id="reply-form">
                          <div class="form-group">
                              From: <input disabled class="form-control" value="${email.recipients}">
                          </div>
                          <div class="form-group">
                              To: <input id="compose-recipients" class="form-control" value="${email.sender}">
                          </div>
                          <div class="form-group">
                              <input class="form-control" id="compose-subject" placeholder="Subject" value="Re: ${email.subject}">
                          </div>
                          <textarea class="form-control" id="compose-body" placeholder="Body">**"On ${email.timestamp} ${email.sender} wrote: ${email.body}"** \n ----- \n</textarea>
                          <input type="submit" class="btn btn-primary"/>
                      </form>`;

  div.addEventListener('submit', event => send_mail(event));                
  
  document.querySelector('#email').append(div);                
}