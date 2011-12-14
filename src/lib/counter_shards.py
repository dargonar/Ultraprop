from google.appengine.api import memcache
from google.appengine.ext import db
import random

class GeneralCounterShardConfig(db.Model):
    """Tracks the number of shards for each named counter."""
    name = db.StringProperty(required=True)
    num_shards = db.IntegerProperty(required=True, default=20)


class GeneralCounterShard(db.Model):
    """Shards for each named counter"""
    name = db.StringProperty(required=True)
    count = db.IntegerProperty(required=True, default=0)

    
def get_count(name):
    """Retrieve the value for a given sharded counter.

    Parameters:
      name - The name of the counter
    """
    total = memcache.get(name)
    if total is None:
        total = 0
        for counter in GeneralCounterShard.all().filter('name = ', name):
            total += counter.count
        memcache.add(name, total, 60)
    return total


def increment(name):
  do_job(name, 1)

def decrement(name):
  do_job(name, -1)
  
def do_job(name, v):
    """Increment the value for a given sharded counter.

    Parameters:
      name - The name of the counter
    """
    config = GeneralCounterShardConfig.get_or_insert(name, name=name)
    def txn():
        index = random.randint(0, config.num_shards - 1)
        shard_name = name + str(index)
        counter = GeneralCounterShard.get_by_key_name(shard_name)
        if counter is None:
            counter = GeneralCounterShard(key_name=shard_name, name=name)
        counter.count += v
        counter.put()
    db.run_in_transaction(txn)
    
    # does nothing if the key does not exist
    memcache.incr(name) if v > 0 else memcache.decr(name)


def increase_shards(name, num):
    """Increase the number of shards for a given sharded counter.
    Will never decrease the number of shards.

    Parameters:
      name - The name of the counter
      num - How many shards to use

    """
    config = GeneralCounterShardConfig.get_or_insert(name, name=name)
    def txn():
        if config.num_shards < num:
            config.num_shards = num
            config.put()
    db.run_in_transaction(txn)

# =========================================================== #
# Wrappers para propiedades de RealEstate.                    #

# Fn privada para generar la key de la realestate en los counter shards.
def get_realestate_token(realestate_key):
  return 'realestate_'+realestate_key+'_published_properties_'

# Agrega propiedad publica.  
def on_public_property_added(realestate_key):
  do_job(get_realestate_token(realestate_key), 1)
  
def on_public_property_deleted(realestate_key):
  do_job(get_realestate_token(realestate_key), -1)
  
def get_realestate_public_properties(realestate_key):
  return get_count(get_realestate_token(realestate_key))
  
def init(realestate_key, value):
  do_job(get_realestate_token(realestate_key), value)

def realestate_can_add_public_property(realestate_key, max_value):
  if max_value<=0:
    return True
  return get_realestate_public_properties(realestate_key)<max_value

# =========================================================== #