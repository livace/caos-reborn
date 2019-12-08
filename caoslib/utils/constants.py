import os

# important paths
CAOSLIB_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
FILES_PATH = os.path.join(CAOSLIB_DIR, 'files')
CONFIG_PATH = os.path.join(FILES_PATH, 'config.ini')
COOKIES_PATH = os.path.join(FILES_PATH, 'cookies.owo')
LINKS_PATH = os.path.join(FILES_PATH, 'links.json')
CAOS_DIR = os.path.join(os.getenv('HOME'), 'programming', 'caos')

# links
SETTINGS = 'Settings'
SUMMARY = 'Summary'
SUBMISSIONS = 'Submissions'
STANDINGS = 'User standings'
CLAR = 'Submit clar'
CLARS = 'Clars'

# submission status
OK = 'OK'
REVIEW = 'Pending review'
NOT_SUBMITTED = 'Not submitted'

COMPILATION_STRING = "gcc -O2 -Wall -Werror -Wno-unused-result -std=gnu11 -lm -fsanitize=address -fsanitize=leak -fsanitize=undefined -fno-sanitize-recover {} -o {}"
