from django.db.utils import IntegrityError
from scrapy import log
from scrapy.exceptions import DropItem
from dynamic_scraper.models import SchedulerRuntime
from django.contrib.auth.models import User


class DjangoWriterPipeline(object):
    
    def process_item(self, item, spider):
        try:
            item['article_website'] = spider.ref_object
            
            checker_rt = SchedulerRuntime(runtime_type='C')
            checker_rt.save()
            item['checker_runtime'] = checker_rt
            item['created_by']= User.objects.get(username='admin')

            item.save()
            spider.action_successful = True
            spider.log("Item saved.", log.INFO)
                
        except IntegrityError, e:
            spider.log(str(e), log.ERROR)
            raise DropItem("Missing attribute.")
                
        return item