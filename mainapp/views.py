from django.shortcuts import render,redirect


import smtplib
import ssl
from email.message import EmailMessage

import random # it is for otp generating purpose

from decouple import config # for converting .env file

# Create your views here.

def index(request):


    # email sending logic
    if request.method=='POST':
        # email=request.POST.get('email')
        # subject=request.POST.get('subject')
        # msg_body=request.POST.get('msg_body')
        # print(email)
        # print(subject)
        # print(msg_body)

        # sender email is coming from .env file
        sender_email=config('sender_email') #company email 
        password=config('password')
        
        # ///////////////////////////////////////////////////////////////
        otp = str(random.randint(10000 , 99999))# random otp generator
        request.session['name'] = otp # otp adding to session database
        request.session.set_expiry(120) # setting session expiry time in seconds
        # ///////////////////////////////////////////////////////////////


        # /////////////////////////////////////////////////////////////////////////
        # detail enter by user window - html form
        emailfilter=request.POST.get('email') # email last area filtering
        if emailfilter.endswith('@gmail.com'):
            res = emailfilter[:-(len('@gmail.com'))]
            print(res)
        else:
            print('Email filter error')
        # //////////////////////////////////////////////////////////////////

        # //////////////////////////////////////////////////////////////////////////
        receiver_email=request.POST.get('email')  # filtering email and assiging to receiver_email
        receiver_subject='Verify Your Account'
        body='Welcome '+ res  #  # 'res' is for filtering email and sending to email body

        # message setting area
        message=EmailMessage()
        message['From']=sender_email
        message['To']=receiver_email
        message['Subject']=receiver_subject
        # message.set_content(body)

        html = f"""
        <html>
            <body>
                <h1>{receiver_subject}</h1>
                <h4>{body}</h4>
                <h4>You can confirm your account through this one time password : </h4>
                <h2>{otp}</h2>
            </body>
        </html>
        """

        message.add_alternative(html, subtype="html")

        context=ssl.create_default_context() # it securing connection

        print('Sending Email')

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email,password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print('Success')

        # return render(request,'index.html',{'send':"Message send succesfully"})
        return redirect(verification)
        # //////////////////////////////////////////////////////////////////////////////////

    return render(request,'index.html',{})

# otp verification logic    
def verification(request):
    
    # # print(str(random.randint(10000 , 99999)))
    # otp = str(random.randint(10000 , 99999))
    # print(otp)

    # data = request.session['name'] = otp

    # print(data,'hai')

    # sdata = request.session.get('name')
    # print(sdata,'sdata')
    

    print(request.session.get('name'))
    if request.method=='POST':
        number=request.POST.get('number')
        print(number)

        if request.session.get('name') == number:
            print('correct')

            request.session.flush() # delete specific user session data
            # otp = request.session.get('name')
            # request.session.clear_expired()
            return render(request,'verification_page.html',{'verified':'Account Verified Successfully'})
        else:
            print('wrong')
            # request.session.flush() # delete specific user session data
            request.session.clear_expired() # delete all expired session data
            return render(request,'verification_page.html',{'wrong':'Wrong OTP','hide_counter':'hide_counter'})

        


    return render(request,'verification_page.html',{})



