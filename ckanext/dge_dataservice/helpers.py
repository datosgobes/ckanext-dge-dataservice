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

import ckan.plugins.toolkit as tk

log = logging.getLogger(__name__)


def get_dataservice(dataservice=None):
    log.debug(f'[get_dataservice] Init. Dataservice = {dataservice}')
    if dataservice is None:
        return {}
    try:
        data = tk.get_action('dge_dataservice_dataservice_show')(
            {}, {'id': dataservice})
        log.debug()
        return data
    except (tk.NotFound, tk.ValidationError, tk.NotAuthorized) as e:
        log.error(f'[get_dataservice] Exception {type(e)}: {e}. ')
        return {}

def get_dataservice_list():
    """
    Get a list of all active dataservice
    """
    log.debug('[get_dataservice_list] Init')
    return  tk.get_action('dge_dataservice_dataservice_list')({}, {})

def get_organization_dataservice_list(organization=None):
    """
    Get a list of all active dataservice of an organization
    """
    log.debug('f[get_organization_dataservice_list] Init. Organization = {organization}')
    return  tk.get_action('dge_dataservice_organization_dataservice_list')(context={}, data_dict={'organization': organization}, organization=organization)