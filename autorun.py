#!/usr/bin/env python
#coding=utf-8
'''
Created on 2012-9-6

@author: chine
'''

import subprocess
import os
import sys

# pkg_resources is in setuptools
from pkg_resources import parse_version

packages = (('PIL', None, 'Image'),
            ('django-grappelli', '2.4.4', 'grappelli'),
            ('django-filebrowser', '3.5.2', 'filebrowser'),
            ('django-mptt', None, 'mptt'),
            ('south', None, 'south'),
            ('pyqqweibo', None, 'qqweibo'))
blog_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ChineBlog')
print 'current_blog_dir path %s' % blog_dir
sys.path.insert(0, os.path.dirname(blog_dir))
has_mistake = False

def _call(*args, **kwargs):
    returncode = subprocess.call(*args, **kwargs)
    if returncode != 0:
        has_mistake = True
    return returncode

def deal_mistake(func):
    def inner(*args, **kwargs):
        if has_mistake:
            return
        return func(*args, **kwargs)
    return inner

def cmp_version(ver1, ver2):
    def _get_version(ver):
        if isinstance(ver, tuple):
            ver = '.'.join((str(itm) for itm in ver))
        return parse_version(str(ver))
    ver1 = _get_version(ver1)
    ver2 = _get_version(ver2)
    return cmp(ver1, ver2)

@deal_mistake
def is_django_version_suitable():
    try:
        import django
        if cmp_version('1.4', django.VERSION) <= 0 \
            and cmp_version('1.5', django.VERSION) > 0:
            # Django in version 1.3.*
            return True
        return False
    except ImportError:
        print u'Django未安装，正在安装Django 1.4.5...'
        install_package('django', '1.4.5')
        return True

def install_package(name, version):
    cmd = "easy_install %s" % name
    if version:
        cmd = cmd + "==%s" % version
    return _call(cmd, shell=True)

@deal_mistake
def setup_env():
    for (name, version, pkg_name) in packages:
        print u'正在检查包%s...' % name
        try:
            __import__(pkg_name)
            print u'已安装'
        except ImportError:
            print u'缺少%s，开始安装...' % name
            install_package(name, version)
            print u'%s安装完成' % name
    print '************************************'

@deal_mistake            
def setup_db():
    from ChineBlog.settings import DATABASES
    
    db = DATABASES['default']['ENGINE'].split('.')[-1]
    if db == 'sqlite3':
        db_dir = os.path.join(blog_dir, 'db')
        if not os.path.exists(db_dir):
            os.mkdir(db_dir)
        db_file = os.path.join(db_dir, 'chine.db')
        if os.path.exists(db_file) and os.path.getsize(db_file) > 0:
            print u'数据库已安装，将执行下一步...'
            print u'************************************'
            return
        try:
            fp = open(db_file, 'w')
        finally:
            if 'fp' in locals():
                fp.close()
    print u'将开始数据库设置...'
    print u'请务必设置超级用户（superuser），并记住超级用户名!'
    # Change dir to blog directory.
    os.chdir(blog_dir)
    _call('python manage.py syncdb', shell=True)
    _call('python manage.py migrate', shell=True)
    print u'./manage.py migrate完成'
    print u'数据库设置完成'
    print u'************************************'
  
@deal_mistake  
def setup_local_settings():
    print u'开始进行本地设置'
    local_settings_file = os.path.join(blog_dir, 'local_settings.py')
    if not os.path.exists(local_settings_file):
        admin = raw_input('Please input superuser name: ')
        admin_email = raw_input('Please input superuser email: ')
        try:
            fp = open(local_settings_file, 'w')
            lines = ["#!/usr/bin/env python\n", 
                     "#coding=utf-8\n", 
                     "\n",
                     "ADMINS = (\n",
                     "    ('%s', '%s'),\n" % (admin, admin_email),
                     ")"]
            fp.writelines(lines)
        finally:
            if 'fp' in locals():
                fp.close()   
    print u'本地设置完成'
    print u'************************************'

@deal_mistake
def run_server(port=None):
    os.chdir(blog_dir)
    print u'开始启动服务，启动完成后可以访问：http://127.0.0.1:%d/来使用博客服务...' \
        % (8000 if not port else port)
    if port:
        _call('python manage.py runserver %d' % port, shell=True)
    else:
        _call('python manage.py runserver', shell=True)

def main(port=None):
    try:
        import setuptools
    except ImportError:
        print u'请确保安装setuptools'
        print u'下载地址：http://pypi.python.org/pypi/setuptools'
        return
    
    if not is_django_version_suitable():
        print u'博客目前运行在Django 1.3版本下，您的Django版本过高或者过低'
        return
    
    setup_env()
    setup_db()
    setup_local_settings()
    run_server(port)
    
    if has_mistake:
        print u'出现错误，请检查网络后重试...'
    
if __name__ == "__main__":
    port = None
    if len(sys.argv) == 3 and sys.argv[1] == '--port':
        port = int(sys.argv[2])
    main(port)