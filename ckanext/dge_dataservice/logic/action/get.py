# Copyright (C) 2025 Entidad Pública Empresarial Red.es
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

import ckan.plugins.toolkit as toolkit
import ckan.lib.dictization.model_dictize as model_dictize


log = logging.getLogger(__name__)

@toolkit.side_effect_free
def dataservice_show(context, data_dict):
    '''Return the pkg_dict for a showcase (package).

    :param id: the id or name of the showcase
    :type id: string
    '''

    toolkit.check_access('dge_dataservice_dataservice_show', context, data_dict)

    pkg_dict = toolkit.get_action('package_show')(context, data_dict)

    return pkg_dict

@toolkit.side_effect_free
def dataservice_list(context, data_dict):
    '''Return a list of all dataservices in the site.'''
    log.debug(f'[dataservice_list] Init data_dict= {data_dict}')
    toolkit.check_access('dge_dataservice_dataservice_list', context, data_dict)

    model = context["model"]

    q = model.Session.query(model.Package) \
        .filter(model.Package.type == 'dataservice') \
        .filter(model.Package.state == 'active')

    dataservice_list = []
    for pkg in q.all():
        dataservice_list.append(model_dictize.package_dictize(pkg, context))
    log.debug(f'[dataservice_list] End. dataservice_list= {dataservice_list}')
    return dataservice_list

@toolkit.side_effect_free
def organization_dataservice_list(context, data_dict, organization):
    '''Return a list of all dataservices of the organizatin in the site.'''
    log.debug(f'[dataservice_list] Init data_dict= {data_dict}')
    toolkit.check_access('dge_dataservice_organization_dataservice_list', context, data_dict)

    model = context["model"]

    dataservice_list = []
    organization = data_dict.get('organization', None)
    organization_id = organization.get('id', None) if organization else None
    if organization_id is not None:
        q = model.Session.query(model.Package) \
            .filter(model.Package.type == 'dataservice') \
            .filter(model.Package.state == 'active') \
            .filter(model.Package.owner_org == organization_id)
        
        for pkg in q.all():
            dataservice_list.append(model_dictize.package_dictize(pkg, context))
    else:
        dataservice_list = dataservice_list(context, data_dict)

    log.debug(f'[dataservice_list] End. dataservice_list= {dataservice_list}')
    return dataservice_list
