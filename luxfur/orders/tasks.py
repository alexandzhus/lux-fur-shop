from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created(order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешном создании заказа
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order id {order_id}'
    message = (f'Уважаемый {order.first_name}, \ '
               f'Вы успешно создали заказ на нашем сайте, \ '
               f'ID вашего заказа {order_id}.')
    mail_send = send_mail(subject, message, 'mydjangotraining@yandex.ru', [order.email])

    return mail_send