from celery.task import task

from dynamic_scraper.utils.task_utils import TaskUtils
from ebook.models import ProductWebsite, Article

@task()
def run_spiders():
    t = TaskUtils()
    t.run_spiders(ProductWebsite, 'scraper', 'scraper_runtime', 'article_spider')
    
@task()
def run_checkers():
    t = TaskUtils()
    t.run_checkers(ProductWebsite, 'news_website__scraper', 'checker_runtime', 'article_checker')