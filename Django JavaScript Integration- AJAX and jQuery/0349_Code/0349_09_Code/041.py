DEBUG = True
TEMPLATE_DEBUG = DEBUG

DIRNAME = os.path.dirname(__file__)

# These are constants used in the template.
DELAY_BETWEEN_RETRIES = 1
INITIAL_RESULTS = 10
INITIAL_STATI = 5
SHOULD_DOWNLOAD_DIRECTORY = 1 # 1 or 0, BUT NOT True or False
SHOULD_TURN_OFF_HIJAXING = 0 # 1 or 0, BUT NOT True or False
# These are weightings used to determine importance in searches.
# The values provided are integer clean, but the code should work for the most
# part with floating point values.
DEPARTMENT_WEIGHT = 30
DESCRIPTION_WEIGHT = 30
LOCATION_WEIGHT = 10
NAME_WEIGHT = 70
STATUS_WEIGHT = 1
TAG_WEIGHT = 50
TITLE_WEIGHT = 50
