        directory.functions.log_message(u'EntityEmail for Entity ' +
          str(model) + u') added by: ' + request.user.username + u', value: ' +
          value + u'\n')
        return HttpResponse(
          u'<a class="edit_rightclick" id="EntityEmail_email_' + str(email.id)          + u'" href="mailto:' + value + u'">' + value + u'</a>' +
          u'''<span class="edit" id="EntityEmail_new_%s">Click to add
email.</span>
<script language="JavaScript" type="text/javascript">
<!--
register_editables();
// -->
</script>''' % str(email.id))
