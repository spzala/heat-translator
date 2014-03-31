import logging
import os

logger = logging.basicConfig(level=logging.DEBUG,
                             format=('%(asctime)s %(name)-6s %(levelname)-4s'
                                     '%(message)s'),
                             datefmt='%m-%d %H:%M',
                             filename=("/tmp/tosca.log"),
                             filemode='w')

logger = logging.getLogger()
