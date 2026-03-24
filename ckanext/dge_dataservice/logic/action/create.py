# Copyright (C) 2026 Entidad Pública Empresarial Red.es
#
# This file is part of "dge-dataservice (datos.gob.es)".
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-
import logging

import ckan.lib.helpers as h
import ckan.plugins.toolkit as toolkit
import ckanext.dge_dataservice.utils as utils


log = logging.getLogger(__name__)


def dataservice_create(context, data_dict):
    # force type
    data_dict[u'type'] = utils.DATASERVICE_TYPE_NAME
    context[u'message'] = data_dict.get(u'log_message', u'')
    pkg = toolkit.get_action('package_create')(context, data_dict)
    return pkg


