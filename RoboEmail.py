import smtplib
from email.message import EmailMessage

def enviar_curriculo_email(destinatario, caminho_pdf):
    msg = EmailMessage()
    msg['Subject'] = 'Currículo - [Seu Nome] - Vaga de Emprego'
    msg['From'] = 'seu_email@gmail.com'
    msg['To'] = destinatario
    msg.set_content("Olá, segue em anexo meu currículo para a vaga mencionada.")

    # Adicionando o arquivo PDF do currículo
    with open(caminho_pdf, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename='Curriculo_SeuNome.pdf')

    # Envio seguro usando porta 465 (SSL)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('seu_email@gmail.com', 'SUA_SENHA_DE_APP') # Gere no Google Security
        smtp.send_message(msg)
    print(f"E-mail enviado para {destinatario}!")
