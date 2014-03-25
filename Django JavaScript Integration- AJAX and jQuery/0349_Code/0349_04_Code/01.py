#!/usr/bin/python

from django.db import models

import datetime
import tagging

OFFICE_CHOICES = (
  (u'CN', u'Chicago North Office, Illinois, USA'),
  (u'CS', u'Chicago South Office, Illinois, USA'),
  (u'WH', u'Wheaton Office, Illinois, USA'),
  (u'SY', u'Sydney Office, New South Wales, Australia'),
  )
