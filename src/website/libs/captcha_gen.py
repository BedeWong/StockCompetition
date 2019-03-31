#coding=utf-8

from captcha import image
from io import BytesIO

import random
import string

class CaptchaGen(object):
    """
    """
    def __init__(self, text=None):
        self._text = text if text else ''.join( random.sample(string.ascii_lowercase + string.ascii_lowercase + '3456789', 5) )
        self.gen = image.ImageCaptcha()

    def createNew(self):
        name = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase + "3456789", 24))

        img = self.gen.generate_image(self._text)

        out = BytesIO()
        img.save(out, format='jpeg')

        return name, self._text, out.getvalue()


def main():
    obj = CaptchaGen(text='Test7')

    for i in range(10):
        name, txt, data = obj.createNew()

        print(name, txt, data)

if __name__ == '__main__':
    main()