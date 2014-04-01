# __*__ coding:utf-8 __*__


"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import MyProfileManager
from models import MyProfile
from django.contrib.auth.models import User
'''
test suite,test case,test/test action ,test data, assert
你可以有几种方式运行单元测试：
python manage.py test：执行所有的测试用例
python manage.py test app_name, 执行该app的所有测试用例
python manage.py test app_name.case_name: 执行指定的测试用例
1.title，description，price，image_url不能为空；
2. price必须大于零；
3. image_url必须以jpg，png，jpg结尾，并且对大小写不敏感；
4. titile必须唯一；
让我们在Django中进行这些测试。由于ProductForm包含了模型校验和表单校验规则，使用ProductForm可以很容易的实现上述测试：
'''
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class MyProfileTestCase(TestCase):
	def setUp(self):
		self.user1 = {
		'username':'test1',
		'password':'test1',
		}
		self.user2 = {
		'username':'test2',
		'password':'test2',
		}
		
		test1 = User(**self.user1)
		test2 = User(**self.user2)
		test1.save()
		test2.save()
		friendship1 = FriendShip(to_friend_id = test1.id)
		friednship2 = FriendShip(from_friend_id = test2.id)
		friendship1.save()
		friendship2.save()

	def test_fans_count(self):
		pass