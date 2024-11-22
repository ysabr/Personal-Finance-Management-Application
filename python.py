import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import time

def send_emails(smtp_server, smtp_port, sender_email, sender_password, recipients_file, subject, body_templates, attachments, delay, increment):
    # Read recipients from file
    try:
        with open(recipients_file, 'r') as file:
            recipients = [line.strip().split(',') for line in file if line.strip()]
    except IOError:
        print("Recipients file not found!")
        return

    # Setup SMTP connection
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
    except Exception as e:
        print("Failed to connect to SMTP server: {}".format(e))
        return

    current_delay = delay
    body_count = len(body_templates)
    body_index = 0  # To cycle through the body templates

    for recipient in recipients:
        if len(recipient) != 2:
            print("Invalid recipient format: {}".format(recipient))
            continue

        name, email = recipient
        name = name.strip()
        email = email.strip()

        # Get the current body template and increment the index
        body_template = body_templates[body_index % body_count]
        body_index += 1

        # Personalize the body
        personalized_body = body_template.replace("{name}", name)

        try:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = email
            msg.attach(MIMEText(personalized_body, 'plain'))

            for attachment in attachments:
                if os.path.isfile(attachment):
                    with open(attachment, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', "attachment; filename= {}".format(os.path.basename(attachment)))
                        msg.attach(part)
                else:
                    print("Attachment {} not found, skipping.".format(attachment))

            text = msg.as_string()
            server.sendmail(sender_email, email, text)
            print("Email sent successfully to {} ({})".format(name, email))
            time.sleep(current_delay)
            current_delay += increment  # Increment the delay
        except Exception as e:
            print("Failed to send email to {} ({}): {}".format(name, email, e))

    server.quit()

# Configuration
smtp_server = 'smtp.gmail.com'  # Correct SMTP server for Gmail
smtp_port = 587
sender_email = 'youssefsabr57@gmail.com'
sender_password = 'afqp ibac blyu gbpd'  # Replace with your app-specific password
recipients_file = 'emails.txt'  # This file should contain "Name,Email" on each line
subject = 'Application for Full Stack Developer Internship at OCP GROUP'

# List of body templates
body_templates = [
    '''
    Dear {name},

    I hope you are doing well. My name is Youssef Sabr, and I am a Software Engineering student at 1337 Coding School, Mohammed VI Polytechnic University. I am reaching out to express my interest in opportunities within your team.

    I have strong skills in Python, Java, C, C++, and JavaScript. I have worked on projects like a real-time multiplayer game backend and a high-performance HTTP web server. I believe my background matches well with your needs.

    Please find my résumé attached for your review. I would be happy to discuss how I can contribute to your projects.

    Thank you for your time.

    Best regards,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71

    ''',
    '''
    Dear {name},

    I hope this email finds you well.

    My name is Youssef Sabr, a student at 1337 Coding School, Mohammed VI Polytechnic University. I am writing to inquire about potential opportunities in your team.

    I have experience in software development, especially with Python and Django. I have developed projects involving real-time communication and containerized infrastructures using Docker. I am confident that my skills can contribute positively to your work.

    Please find my résumé attached. I am available to provide any additional information.

    Thank you for considering my application.

    Sincerely,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    ''',
    '''
    Dear {name},

    I hope this message finds you well. I am Youssef Sabr, studying Software Engineering at 1337 Coding School. I am interested in exploring opportunities within your team.

    My background includes programming in C++, C, and JavaScript. I have built a high-performance HTTP web server and worked on various software projects. I am eager to bring my skills to your team.

    Please find my résumé attached. I would appreciate the chance to discuss this with you.

    Thank you for your time.

    Best regards,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    '''
    '''
    Dear {name},
    
    I hope this email finds you well.

    My name is Youssef Sabr, and I am a Software Engineering student at 1337 Coding School. I am reaching out to express my interest in joining your team.

    I have strong skills in Python, Java, and web technologies. I have worked on projects like a real-time multiplayer game backend using WebSockets. I believe I can contribute effectively to your projects.

    Please find my résumé attached. I am happy to discuss any opportunities with you.

    Thank you for considering my application.

    Sincerely,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    '''
    '''
    Dear {name},

    I hope you are doing well. I am Youssef Sabr, a student at 1337 Coding School, Mohammed VI Polytechnic University. I am interested in opportunities within your team.

    With experience in Django and React, I have developed web applications and backend systems. I am passionate about software engineering and believe my skills align with your needs.

    Please find my résumé attached for your review. I would welcome the opportunity to discuss how I can contribute to your team.

    Thank you for your time.

    Best regards,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    '''
    '''
    Dear {name},
        
    I hope this email finds you well.

    My name is Youssef Sabr, and I am studying Software Engineering at 1337 Coding School. I am writing to express my interest in joining your team.

    I have worked on projects involving Docker, NGINX, and MariaDB. I have strong skills in containerization and backend development. I am confident that I can add value to your projects.

    Please find my résumé attached. I am available to discuss any opportunities with you.

    Thank you for considering my application.

    Sincerely,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    '''
    '''
    Dear {name},
        
    I hope this email finds you well.

    I am Youssef Sabr, a Software Engineering student at 1337 Coding School. I am reaching out to explore any opportunities within your team.

    I have experience in programming languages like Java and Python. I have developed various software projects and am eager to contribute my skills to your team.

    Please find my résumé attached for your consideration. I would be happy to discuss further.

    Thank you for your time.

    Best regards,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    '''
    '''
    Dear {name},
    
    I hope this email finds you well. My name is Youssef Sabr, and I am studying at 1337 Coding School. I am interested in potential opportunities within your team.

    My background includes working with RESTful APIs and web development frameworks. I have a strong foundation in data structures and algorithms.

    Please find my résumé attached. I look forward to the possibility of contributing to your projects.

    Thank you for considering my application.

    Sincerely,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    '''
    '''
    Dear {name},
        
    I hope this email finds you well.

    My name is Youssef Sabr, a Software Engineering student at 1337 Coding School. I am writing to express my interest in opportunities within your team.

    I have experience with Git, Docker, and software development tools. I have worked on projects involving network programming and operating systems.

    Please find my résumé attached. I would appreciate the opportunity to discuss how I can be of value to your team.

    Thank you for your time.

    Best regards,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    '''
    '''
    Dear {name},
        
    I hope this email finds you well.

    I hope you are doing well. I am Youssef Sabr, studying Software Engineering at 1337 Coding School, Mohammed VI Polytechnic University. I am reaching out to explore opportunities in your team.

    My skills include programming in Python, JavaScript, and experience with web technologies. I am eager to contribute my skills to your projects.

    Please find my résumé attached. I am happy to provide any additional information.

    Thank you for considering my application.

    Sincerely,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    '''
    '''
    Dear {name},
        
    I hope this email finds you well.

    My name is Youssef Sabr, a Software Engineering student at 1337 Coding School. I am writing to inquire about opportunities within your team.

    I have developed projects using Django and have a strong understanding of object-oriented programming. I am confident that my skills can contribute to your work.

    Please find my résumé attached for your review. I look forward to discussing this with you.

    Thank you for your time.

    Best regards,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    '''
    '''
    Dear {name},
    
    I hope this message finds you well. I am Youssef Sabr, studying at 1337 Coding School. I am interested in any opportunities within your team.

    I have experience with algorithms, data structures, and software engineering principles. I am eager to apply my knowledge and learn from your team.

    Please find my résumé attached. I would appreciate the chance to discuss this further.

    Thank you for considering my application.

    Sincerely,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    '''
    '''
    Dear {name},
        
    I hope this email finds you well.

    My name is Youssef Sabr, a Software Engineering student at 1337 Coding School. I am reaching out to express my interest in joining your team.

    I have strong skills in programming and problem-solving. I have worked on projects involving real-time systems and network programming.

    Please find my résumé attached. I am available to discuss any opportunities with you.

    Thank you for your time.

    Best regards,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    '''
        '''
    Dear {name},
    

    I hope you are doing well. I am Youssef Sabr, studying at 1337 Coding School, Mohammed VI Polytechnic University. I am interested in exploring opportunities within your team.

    I have experience in backend development and have worked with technologies like WebSockets and Docker. I believe my skills can be a good match for your projects.

    Please find my résumé attached. I would welcome the opportunity to discuss this with you.

    Thank you for considering my application.

    Sincerely,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    '''
            '''
    Dear {name},
    
    I hope this email finds you well.

    My name is Youssef Sabr, a Software Engineering student at 1337 Coding School. I am writing to inquire about potential opportunities within your team.

    I have strong programming skills in Python and Java, and experience with software development tools like Git and Visual Studio Code. I am eager to contribute to your team.

    Please find my résumé attached. I am available to discuss any opportunities at your convenience.

    Thank you for your time.

    Best regards,

    Youssef Sabr

    LinkedIn: linkedin.com/in/ysabr

    Phone: +212 6 98 87 47 71
    '''
    # Add more templates as needed
]

attachments = ['SoftwareEngineer_YoussefSabr.pdf', 'Coverletter_YoussefSabr.pdf']
delay = 120  # Initial delay in seconds
increment = 30  # Increment delay by 10 seconds after each email

# Send emails
send_emails(
    smtp_server,
    smtp_port,
    sender_email,
    sender_password,
    recipients_file,
    subject,
    body_templates,
    attachments,
    delay,
    increment
)
