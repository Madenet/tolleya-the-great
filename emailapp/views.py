from django.shortcuts import render
from .models import Customer
from .forms import CustomForm
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string, get_template 
from django.shortcuts import render, redirect
from .forms import CustomForm 


def send(request):
    return render(request,'emailapp/send.html')
    
def sendto_allcustomers(request):
    customers = Customer.objects.all()
    for customers in customers:
        print(customers.name)
        email_address = customers.email_address
    
        message = 'We have new products, check out our website'
    
        subject = 'New Products'
        context = {'name': customers.name,'message': message}
        message = get_template('emailapp/email.html').render(context)
        email = EmailMessage(subject, message,"Macrosecond Apply", [email_address])
        email.content_subtype = "html" 
        email.send()
    
    return redirect('send')


def sendto_activecustomers(request):
    customers = Customer.objects.filter(status='active')
    for customers in customers:
        print(customers.name)
        email_address = customers.email_address
        
        message = 'We have new products, check out our website'
    
        subject = 'New Products'
        context = {'name': customers.name,'message': message}
        message = get_template('emailapp/email.html').render(context)
        email = EmailMessage(subject, message,"Macrosecond Apply", [email_address])
        email.content_subtype = "html" 
        email.send()
    
    return redirect('send')


def sendto_inactivecustomers(request):
    customers = Customer.objects.filter(status='inactive')
    for customers in customers:
        print(customers.name)
        email_address = customers.email_address

        message = 'We have new products, check out our website'
    
        subject = 'New Products'
        context = {'name': customers.name,'message': message}
        message = get_template('emailapp/email.html').render(context)
        email = EmailMessage(subject, message,"Macrosecond Apply", [email_address])
        email.content_subtype = "html" 
        email.send()
    
    return redirect('send')

#send email to domain access us either.
def custom_message(request):
    if request.method == "POST":
        form = CustomForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            status = form.cleaned_data['status']
            subject = form.cleaned_data['subject']

            # Check if the user selected the option to send to macrosecond@gmail.com
            if status == 'macrosecond':
                email_address = 'macrosecond1@gmail.com'
                context = {'message': message}
                email_template = get_template('emailapp/email.html').render(context)
                email = EmailMessage(subject, email_template, "Macrosecond Apply", [email_address])
                email.content_subtype = "html"
                email.send()
            else:
                # Send emails to customers based on the selected status
                if status == 'all':
                    customers = Customer.objects.all()
                else:
                    customers = Customer.objects.filter(status=status)

                for customer in customers:
                    email_address = customer.email_address
                    context = {'name': customer.name, 'message': message}
                    email_template = get_template('emailapp/email.html').render(context)
                    email = EmailMessage(subject, email_template, "Macrosecond Apply", [email_address])
                    email.content_subtype = "html"
                    email.send()

            return redirect('custom_message')

        else:
            print(form.errors)

    return render(request, 'emailapp/message.html')

#add customer page
def add_customer(request):
    if request.method == 'POST':
        form = CustomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')  # Assuming you have a URL pattern named 'customer_list'
    else:
        form = CustomForm()

    return render(request, 'emailapp/customer_form.html', {'form': form})
