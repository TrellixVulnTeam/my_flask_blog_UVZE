# -*- coding: utf-8 -*-
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from src import mail



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Сбросить пароль', 
                    sender='adv31337@gmail.com', 
                    recipients=[user.email])
    msg.body = f'''Для восстановления пароля перейдите по ссылке ниже:
{url_for('users.reset_token', token=token, _external=True)}

Если вы не меняли пароль, просто проигнорируйте это сообщение.
'''
    mail.send(msg)