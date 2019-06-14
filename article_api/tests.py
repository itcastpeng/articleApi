from django.test import TestCase

# Create your tests here.

content = '微整后悔药溶解酶       玻尿酸是个好“东西”，但如果注射过量，注射到错误的部位，有解决办法吗？        玻尿酸溶解酶就是“解药”！'

content = content.replace('\r\n', '').replace('\n', '').strip().strip()
content = ''.join(content.split())

print('content----> ', content)
num = len(content)

print(num)


















