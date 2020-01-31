#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 07:51:29 2020

@author: Luciano Galicki

This script will send simple text e-mails through Gmail accounts. In order for
it to work, there are a couple of steps that must be taken:

- the Gmail account must have less secure apps access activated;
- there must be, in the same folder of this script, a SQLite database named
"email.db". It must have a table named "sender" with two columns: "sender" and
"password". In the former the whole e-mail address must be stored, and in the
latter the password. There should be only one row in this table.

Storing address and password like this allows this script to be publicly shared.

"""

import smtplib
import ssl
import sqlite3

def send_email(receiver, subject, msg_body):
    """
    Creates a SSL connection to Gmail's SMTP and sends the email.

    Parameters
    ----------
    receiver : string
        E-mail address of the receiver.
    subject : TYPE
        E-mail's subject.
    msg_body : TYPE
        E-mail's body.

    Returns
    -------
    None.

    """
    port = 465  # For SSL
    sender_info = get_sender()
    sender = sender_info[0]
    password = sender_info[1]

    message = f'Subject: {subject}\n\n{msg_body}'

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Connect to the SMTP server and send the e-mail
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)


def get_sender():
    """
    Grabs the sender e-mail and password in local SQLite database.

    Returns
    -------
    email : string
        Sender's e-mail address.
    password : string
        Sender's password.

    """
    connection = sqlite3.connect('email.db')
    cursor = connection.cursor()
    sql = "SELECT sender, password FROM senders;"
    cursor.execute(sql)
    row = cursor.fetchone()
    email = row[0]
    password = row[1]
    return email, password


if __name__ == '__main__':
    RECEIVER = input('Send e-mail to: ')
    SUBJECT = input('Email subject: ')
    MESSAGE = input('E-mail body: ')

    send_email(RECEIVER, SUBJECT, MESSAGE)
    print(f"Check {RECEIVER}'s inbox.")
