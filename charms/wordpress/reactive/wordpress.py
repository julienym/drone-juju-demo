from charms.reactive import when, when_not, set_flag, hook
from charmhelpers.core.hookenv import status_set
import charms.apt

@when_not('apt.installed.wordpress')
def install_wordpress_apt():
    charms.apt.queue_install(['wordpress'])
    #sets the 'apt.installed.wordpress' flag when done

@when('apt.installed.wordpress')
@when_not('wordpress.ready')
def install_wordpress():
    # Do your setup here.
    #
    # If your charm has other dependencies before it can install,
    # add those as @when() clauses above., or as additional @when()
    # decorated handlers below
    #
    # See the following for information about reactive charms:
    #
    #  * https://jujucharms.com/docs/devel/developer-getting-started
    #  * https://github.com/juju-solutions/layer-basic#overview
    #
    status_set('blocked', "wordpress installed, waiting for database")
    set_flag('wordpress.ready')

@when_not('wordpress.ready')
@when_not('apt.installed.wordpress')
def waiting_for_wordpress():
    status_set('maintenance', "waiting for apt wordpress installation")

@hook('database-relation-joined')
def database_is_ready():
    status_set('blocked', 'Database is ready (joined) but not configured')
    set_flag('wordpress.database_is_ready')