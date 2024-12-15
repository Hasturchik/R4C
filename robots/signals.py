from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Robot
from orders.models import Order
from customers.send_mail import send_email


@receiver(post_save, sender=Robot)
def notify_customer_when_robot_available(sender, instance, created, **kwargs):

    if created:

        orders = Order.objects.filter(robot_serial=instance.serial)
        for order in orders:

            customer = order.customer
            email = customer.email
            send_email(email, instance.model, instance.version)
