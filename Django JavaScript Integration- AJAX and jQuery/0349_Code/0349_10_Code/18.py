@login_required
def changelog(request):
    candidates = \
      directory.models.EditTrail.objects.filter(in_effect = True).order_by(
      u'-timestamp')
    return render_to_response(u'changelog.html',
      {
      u'candidates': candidates,
      u'format_timestamp': directory.functions.format_timestamp,
      u'settings': directory.settings,
      })
