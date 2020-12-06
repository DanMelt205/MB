from django import template
import decimal

register = template.Library()


@register.filter()
def subtract(value, arg):
    return value - arg


@register.filter()
def addfloats(value, arg):
    return value + arg


# class first:
    # x = 0
    # y = 0

    # @register.filter()
    # def firsttime(self, value):

    #     if "Left" == value:
    #         if self.x == 0:
    #             self.x = self.x+1
    #             return True
    #         else:
    #             return False
    #     if "Right" == value:
    #         if self.y == 0:
    #             self.y = self.y + 1
    #             return True
    #         else:
    #             return False
