from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import get_model
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, Template
from django.template.defaultfilters import escape
from django.template.loader import get_template
from directory.functions import ajax_login_required

import directory.models
import json
import re
