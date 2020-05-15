[Setup Domain Authentication](https://sendgrid.com/docs/ui/account-and-settings/how-to-set-up-domain-authentication/)

The setup is not too difficult. Use SendGrid, which provides 100 emails / month FREE, forever. Setup the DNS records, configure Django to use API key to send emails, then run a quick test.

## SendGrid
1.  Sign up at SendGrid
2.  Follow the **Domain Authentication** setup instructions
![image](/static/img/markdowns/sendgrid1.png)

## DigitalOcean
From the setup instructions, there will be a list of DNS records that need to be added. Although sinto-ling.ca is registered with Google Domains, the `name servers` used are Digital Ocean's. In the DO DNS page, under CNAME, add the listed records:
![image](/static/img/markdowns/sendgrid2.png)

Wait about 3-5 minutes, then click Verify in SendGrid. Wait and retry if it still doesn't work - it takes a bit of time to populate. Once verified, go back to Django app.

## PyCharm
Add a new file in same directory as `views.py`. Then have the `sample_mail()` function be called when the homepage is loaded.
`mailserver.py`
```python
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def sample_mail():
    message = Mail(
        from_email='no_reply@sinto-ling.ca',
        to_emails='sinto.005234@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('DJANGO_SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

    return
```

`views.py`
```python
# homepage
def homepage(request):

    # try to run the mailserver.py script
    print("Sending Mail...")
    sample_mail()
    print("... Sent")

    return render(request, 'pages/home.html')
```

### TERMINAL OUTPUT
```
System check identified no issues (0 silenced).
April 29, 2020 - 11:00:22
Django version 3.0.5, using settings 'djangoapps.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
Sending Mail...
202
b''
Server: nginx
Date: Wed, 29 Apr 2020 17:00:30 GMT
Content-Length: 0
Connection: close
X-Message-Id: qdUARSLtScikspRRZcZ4jw
Access-Control-Allow-Origin: https://sendgrid.api-docs.io
Access-Control-Allow-Methods: POST
Access-Control-Allow-Headers: Authorization, Content-Type, On-behalf-of, x-sg-elas-acl
Access-Control-Max-Age: 600
X-No-CORS-Reason: https://sendgrid.com/docs/Classroom/Basics/API/cors.html


... Sent
[29/Apr/2020 11:00:33] "GET /home HTTP/1.1" 200 1797
[29/Apr/2020 11:00:33] "GET /static/style.css HTTP/1.1" 404 1653
```

### EMAIL RECEIVED
![image](/static/img/markdowns/sendgrid3.png)

## Other Links
Original Tutorial: [Send Email in Django](https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html)  
Link Branding: [Link Branding](https://sendgrid.com/docs/ui/account-and-settings/how-to-set-up-link-branding/#-What-is-link-branding)