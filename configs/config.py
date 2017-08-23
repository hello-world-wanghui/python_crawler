#! /usr/bin/env python
# -*- coding: utf-8 -*-

import config_default
import env

configs = config_default.configs

try:
    ONLINE = env.ENV and env.ENV == 'online'
    ONLINE_DEV = env.ENV and env.ENV == 'online_dev'

    if ONLINE:
        import config_online
        configs = config_online.configs

except ImportError:
    pass
