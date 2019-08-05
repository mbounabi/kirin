# coding=utf-8

# Copyright (c) 2001-2014, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io
import celery
from flask import Request, request
import uuid
import logging


class IdFilter(logging.Filter):
    def filter(self, record):
        try:
            record.request_id = request.id
        except RuntimeError:
            # if we are outside of a application context
            pass
        return True


# http://flask.pocoo.org/docs/0.12/patterns/celery/
def make_celery(app):
    celery_app = celery.Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"])
    celery_app.conf.update(app.config)
    TaskBase = celery_app.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


class KirinRequest(Request):
    """
    override the request of flask to add an id on all request
    """

    def __init__(self, *args, **kwargs):
        super(Request, self).__init__(*args, **kwargs)
        self.id = str(uuid.uuid4())
