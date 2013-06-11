#: whether or not to re-read the bathymetry on the next run.
from datetime import timedelta
import mongoengine
mongoengine.register_connection('cera','cera', host='geocompute2.renci.org')

RECALCULATE_BATHYMETRY = False
BATHYMETRY_SOURCE_FILE = '/data1/cera/adcirc.asc'
BATHYMETRY_INDEX_FILE = '/data1/cera/'

#: path that the NetCDF output is mounted to.  no slash on the end of this one
ADCIRC_MOUNTPOINT = '/data1/cera/dap'

#: path to the model run NetCDFs
ADCIRC_NETCDF_PATH = '/ncfs/opendap/data/tc/isaac/23/nc6b/blueridge.renci.org/ncfs/nhcConsensus/'
ADCIRC_RUNID = "23"
ADCIRC_YYYYMMDD = "20120826"
DATASET_DIMENSIONS = (u'time',u'node')

#: valid run ids.  corresponds to hours of the day.
VALID_RUN_ID = ('00','06','12','18')

MAXIMUM_CACHE_SIZE = 50000
DELETE_ARRAYS_OLDER_THAN = timedelta(days=365)

#: variables to find.  uncomment any of these others once we get to wanting them.
VARIABLES = {
#    "statelev"      : "water surface elevation stations",
#    "statatmpress"  : "atmospheric pressure stations",
#    "statwvel"      : "wind velocity stations",
    "atmpress"      : "barometric pressure",
    "maxhsign"      : "maximum significant wave height",
    "dir"           : "mean wave direction",
    "maxradstress"  : "maximum wave radiation stress",
#    "dvel"          : "water current velocity",
    "maxtmm10"      : "maximum mean wave period",
    "tmm10"         : "mean wave period",
    "elev"          : "elevation",
    "maxtps"        : "maximum peak wave period",
    "tps"           : "peak wave period",
    "hsign"         : "significant wave height",
    "maxwvel"       : "maximum wind velocity",
    "wvel"          : "wave elevation",
    "maxdir"        : "maximum mean wave direction",
    "minatmpress"   : "minimum atmospheric pressure",
    "maxele"       : "maximum elevation",
}

from celery.schedules import crontab

# regular tasks to perform.
APP_CELERYBEAT_SCHEDULE = {
    'cera-append_new_run' : {
        'task' : 'cera.tasks.add_new_run',
        'schedule' : crontab(minute=5, hour=[0,6,12,18])
    },
    'cera-clean_web_cache' : {
        'task' : 'cera.tasks.clean_web_cache',
        'schedule' : crontab(minute=0, hour=[0,6,12,18])
    },
    'cera-remove_old_data' : {
        'task' : 'cera.tasks.remove_old_data',
        'schedule' : crontab(day_of_week=0, hour=1, minute=0)
    }
}

APP_LOGGING = {
    'cera.tasks' : {
        'handlers' : ['cera'],
        'propagate' : True,
        'level' : 'DEBUG'
    },
    'cera.query' : {
        'handlers' : ['cera'],
        'propagate' : True,
        'level' : 'DEBUG'
    },
    'cera.views' : {
        'handlers' : ['cera'],
        'propagate' : True,
        'level' : 'DEBUG'
    }
}
