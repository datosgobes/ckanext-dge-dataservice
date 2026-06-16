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
import ckanext.dge.helpers as dh

log = logging.getLogger(__name__)
    
def dataservice_delete(context, data_dict):
    '''Delete a dataservice. Dataservoce delete cascades to
    DataservicePackageAssociation objects.

    :param id: the id or name of the dataservice to delete
    :type id: string
    '''

    model = context['model']
    dataservice_id = toolkit.get_or_bust(data_dict, 'id')
    dataservice_name = toolkit.get_or_bust(data_dict, 'name')
    if dh.dge_has_datasets_served_by_dataservice(dataservice_id, dataservice_name) is True:
        h.flash_notice(toolkit._('Dataservice has Datasources associated.'))
        return False
    
    entity = model.Package.get(id)

    if entity is None:
        raise toolkit.ObjectNotFound

    toolkit.check_access('dge_dataservice_dataservice_delete', context, data_dict)

    entity.purge()
    model.repo.commit()
    return True