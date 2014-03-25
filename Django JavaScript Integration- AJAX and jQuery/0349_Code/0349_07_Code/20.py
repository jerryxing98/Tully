    if html_id.startswith(u'Entity_department_'):
        value = dictionary[u'department']
    elif html_id.startswith(u'Entity_location_'):
        value = dictionary[u'location']
    elif html_id.startswith(u'Entity_reports_to_'):
        value = dictionary[u'reports_to']
    else:
        value = dictionary[u'value']
    if not re.match(ur'^\w+$', html_id):
        raise Exception("Invalid HTML id.")
    match = re.match(ur'EntityEmail_new_(\d+)', html_id)
    if match: 
        model = int(match.group(1))
        email = directory.models.EntityEmail(email = value, entity =
          directory.models.Entity.objects.get(pk = model))
        email.save()
        directory.functions.log_message(u'EntityEmail for Entity ' +
          str(model) + u') added by: ' + request.user.username + u', value: ' +
          value + u'\n')
        return HttpResponse(
          u'<a class="edit_rightclick" id="EntityEmail_email_' + str(email.id)
          + u'" href="mailto:' + value + u'">' + value + u'</a>' + 
          u'''<span class="edit" id="EntityEmail_new_%s">Click to add
email.</span>
<script language="JavaScript" type="text/javascript">
<!--
register_editables();
// -->
</script>''' % str(email.id))
