from django.test import TestCase
from models import Anonymous, Events, News, Projects, Pictures, Feedback, Comments


# Create your tests here.
def anonymous_test():
    anonymous = Anonymous()
    anonymous.insert("zhoupan", "zhoupans_mail@163.com")


if __name__ == '__main__':
    anonymous_test()
